from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import cv2
import numpy as np
import base64
from datetime import datetime
import io
from PIL import Image

from database import db
from face_proctoring import FaceProctoring
from object_detection import ObjectDetection
from question_generator import QuestionGenerator

app = FastAPI(title="AI Proctoring System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize proctoring modules
face_proctoring = FaceProctoring()
object_detection = ObjectDetection()
question_gen = QuestionGenerator()  # Now includes both pre-loaded bank and AI

# Pydantic models
class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class QuestionCreate(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    subject: Optional[str] = None
    difficulty: Optional[str] = None

class AnswerSubmit(BaseModel):
    exam_id: int
    question_id: int
    user_answer: str

class GenerateQuestionsRequest(BaseModel):
    subject: str
    difficulty: str
    count: int = 5

# Database connection on startup
@app.on_event("startup")
async def startup():
    db.connect()

@app.on_event("shutdown")
async def shutdown():
    db.disconnect()

# Root endpoint
@app.get("/")
async def root():
    return {"message": "AI Proctoring System API", "status": "running"}

# ==================== USER MANAGEMENT ====================

@app.post("/api/register")
async def register(user: UserCreate):
    """Register a new user"""
    try:
        query = """
        INSERT INTO users (username, password, email) 
        VALUES (%s, %s, %s)
        """
        db.execute_query(query, (user.username, user.password, user.email))
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")

@app.post("/api/login")
async def login(user: UserLogin):
    """User login"""
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    result = db.fetch_one(query, (user.username, user.password))
    
    if result:
        return {
            "message": "Login successful",
            "user_id": result['id'],
            "username": result['username'],
            "is_admin": result['is_admin']
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# ==================== QUESTION MANAGEMENT ====================

# @app.post("/api/questions/generate")
# async def generate_questions(request: GenerateQuestionsRequest):
#     """Generate questions using AI (Admin only)"""
#     questions = question_gen.generate_questions(
#         request.subject, 
#         request.difficulty, 
#         request.count
#     )
@app.post("/api/questions/generate")
async def generate_questions(request: GenerateQuestionsRequest):
    questions = question_gen.generate_questions(
        request.subject, 
        request.difficulty, 
        request.count
    )
    
    # VALIDATE before storing
    for q in questions:
        if not q.get('question') or len(q['question']) < 5:
            raise HTTPException(400, "Invalid question generated")
        if not all([q.get('option_a'), q.get('option_b'), 
                    q.get('option_c'), q.get('option_d')]):
            raise HTTPException(400, "Missing options")

    # Store generated questions in database
    stored_questions = []
    for q in questions:
        query = """
        INSERT INTO questions 
        (question_text, option_a, option_b, option_c, option_d, correct_answer, subject, difficulty) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor = db.execute_query(query, (
            q['question'],
            q['option_a'],
            q['option_b'],
            q['option_c'],
            q['option_d'],
            q['correct_answer'],
            q.get('subject', request.subject),
            q.get('difficulty', request.difficulty)
        ))
        
        if cursor:
            stored_questions.append({
                'id': cursor.lastrowid,
                **q
            })
    
    return {"questions": stored_questions, "count": len(stored_questions)}

@app.post("/api/questions")
async def create_question(question: QuestionCreate):
    """Create a new question (Admin only)"""
    query = """
    INSERT INTO questions 
    (question_text, option_a, option_b, option_c, option_d, correct_answer, subject, difficulty) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor = db.execute_query(query, (
        question.question_text,
        question.option_a,
        question.option_b,
        question.option_c,
        question.option_d,
        question.correct_answer,
        question.subject,
        question.difficulty
    ))
    
    if cursor:
        return {"message": "Question created", "id": cursor.lastrowid}
    raise HTTPException(status_code=500, detail="Failed to create question")

@app.get("/api/questions")
async def get_questions(limit: int = 20, subject: Optional[str] = None):
    """Get random questions for exam (max 20)"""
    # FIX: Enforce maximum limit
    limit = min(limit, 20)
    
    if subject:
        query = "SELECT * FROM questions WHERE subject = %s ORDER BY RAND() LIMIT %s"
        questions = db.fetch_all(query, (subject, limit))
    else:
        query = "SELECT * FROM questions ORDER BY RAND() LIMIT %s"
        questions = db.fetch_all(query, (limit,))
    
    # Remove correct answers from response
    for q in questions:
        q.pop('correct_answer', None)
    
    return {"questions": questions, "total": len(questions)}

@app.get("/api/questions/all")
async def get_all_questions():
    """Get all questions with answers (Admin only)"""
    query = "SELECT * FROM questions ORDER BY created_at DESC"
    questions = db.fetch_all(query)
    return {"questions": questions, "total": len(questions)}

@app.get("/api/questions/debug")
async def debug_questions():
    """Debug endpoint to see what's in database"""
    query = "SELECT id, question_text, subject, difficulty FROM questions"
    questions = db.fetch_all(query)
    
    # Group by subject
    subjects = {}
    for q in questions:
        subject = q.get('subject', 'Unknown')
        if subject not in subjects:
            subjects[subject] = {'easy': 0, 'medium': 0, 'hard': 0, 'total': 0}
        
        difficulty = q.get('difficulty', 'unknown')
        if difficulty in subjects[subject]:
            subjects[subject][difficulty] += 1
        subjects[subject]['total'] += 1
    
    return {
        "total_questions": len(questions),
        "subjects": subjects,
        "sample_questions": questions[:5]
    }

# ==================== EXAM MANAGEMENT ====================

@app.post("/api/exam/start")
async def start_exam(user_id: int, exam_name: str = "General Exam"):
    """Start a new exam"""
    query = """
    INSERT INTO exams (user_id, exam_name, status) 
    VALUES (%s, %s, 'in_progress')
    """
    cursor = db.execute_query(query, (user_id, exam_name))
    
    if cursor:
        return {"message": "Exam started", "exam_id": cursor.lastrowid}
    raise HTTPException(status_code=500, detail="Failed to start exam")

@app.post("/api/exam/submit")
async def submit_answer(answer: AnswerSubmit):
    """Submit an answer"""
    # Get correct answer
    query = "SELECT correct_answer FROM questions WHERE id = %s"
    result = db.fetch_one(query, (answer.question_id,))
    
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    
    is_correct = result['correct_answer'] == answer.user_answer
    
    # Store user answer
    query = """
    INSERT INTO user_answers (exam_id, question_id, user_answer, is_correct) 
    VALUES (%s, %s, %s, %s)
    """
    db.execute_query(query, (
        answer.exam_id,
        answer.question_id,
        answer.user_answer,
        is_correct
    ))
    
    return {"message": "Answer submitted", "is_correct": is_correct}

@app.post("/api/exam/finish")
async def finish_exam(exam_id: int):
    """Finish exam and calculate score"""
    # Calculate score
    query = """
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct
    FROM user_answers 
    WHERE exam_id = %s
    """
    result = db.fetch_one(query, (exam_id,))
    
    if result and result['total'] > 0:
        score = (result['correct'] / result['total']) * 100
    else:
        score = 0
    
    # Update exam
    query = """
    UPDATE exams 
    SET end_time = NOW(), score = %s, status = 'completed' 
    WHERE id = %s
    """
    db.execute_query(query, (score, exam_id))
    
    return {
        "message": "Exam completed",
        "score": score,
        "correct": result['correct'] if result else 0,
        "total": result['total'] if result else 0
    }

@app.get("/api/exam/results/{exam_id}")
async def get_exam_results(exam_id: int):
    """Get detailed exam results"""
    # Get exam info
    exam_query = "SELECT * FROM exams WHERE id = %s"
    exam = db.fetch_one(exam_query, (exam_id,))
    
    # Get all answers
    answers_query = """
    SELECT 
        ua.*, 
        q.question_text, 
        q.option_a, q.option_b, q.option_c, q.option_d,
        q.correct_answer
    FROM user_answers ua
    JOIN questions q ON ua.question_id = q.id
    WHERE ua.exam_id = %s
    ORDER BY ua.answered_at
    """
    answers = db.fetch_all(answers_query, (exam_id,))
    
    # Get violations
    violations_query = "SELECT * FROM violations WHERE exam_id = %s ORDER BY timestamp"
    violations = db.fetch_all(violations_query, (exam_id,))
    
    return {
        "exam": exam,
        "answers": answers,
        "violations": violations
    }

# ==================== PROCTORING ====================

@app.post("/api/proctor/analyze")
async def analyze_frame(file: UploadFile = File(...)):
    """Analyze a frame for proctoring violations"""
    try:
        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            raise HTTPException(status_code=400, detail="Invalid image")
        
        # Analyze with both modules
        face_violations = face_proctoring.analyze_frame(frame)
        object_violations = object_detection.detect_objects(frame)
        
        # Combine results
        all_violations = []
        
        # Add face violations
        face_summary = face_proctoring.get_violation_summary(face_violations)
        if face_summary:
            all_violations.append(face_summary)
        
        # Add object violations
        object_summary = object_detection.get_violation_message(object_violations)
        if object_summary:
            all_violations.append(object_summary)
        
        return {
            "violations": all_violations,
            "face_analysis": {
                "face_count": face_violations['face_count'],
                "multiple_faces": face_violations['multiple_faces'],
                "no_face": face_violations['no_face'],
                "looking_away": face_violations['looking_away']
            },
            "object_analysis": {
                "suspicious_objects": object_violations['suspicious_objects'],
                "severity": object_violations['severity']
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/proctor/violation")
async def log_violation(
    exam_id: int = Form(...),
    violation_type: str = Form(...),
    severity: str = Form(...),
    description: str = Form(...)
):
    """Log a proctoring violation"""
    query = """
    INSERT INTO violations (exam_id, violation_type, severity, description) 
    VALUES (%s, %s, %s, %s)
    """
    cursor = db.execute_query(query, (exam_id, violation_type, severity, description))
    
    if cursor:
        return {"message": "Violation logged", "id": cursor.lastrowid}
    raise HTTPException(status_code=500, detail="Failed to log violation")

@app.get("/api/proctor/violations/{exam_id}")
async def get_violations(exam_id: int):
    """Get all violations for an exam"""
    query = "SELECT * FROM violations WHERE exam_id = %s ORDER BY timestamp DESC"
    violations = db.fetch_all(query, (exam_id,))
    return {"violations": violations, "count": len(violations)}

# ==================== STATISTICS ====================

@app.get("/api/stats/user/{user_id}")
async def get_user_stats(user_id: int):
    """Get user statistics"""
    query = """
    SELECT 
        COUNT(*) as total_exams,
        AVG(score) as average_score,
        MAX(score) as best_score,
        MIN(score) as worst_score
    FROM exams 
    WHERE user_id = %s AND status = 'completed'
    """
    stats = db.fetch_one(query, (user_id,))
    
    # Get recent exams
    exams_query = """
    SELECT * FROM exams 
    WHERE user_id = %s 
    ORDER BY start_time DESC 
    LIMIT 10
    """
    recent_exams = db.fetch_all(exams_query, (user_id,))
    
    return {
        "statistics": stats,
        "recent_exams": recent_exams
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)