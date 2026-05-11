# Technical Documentation - AI Proctoring System

## System Overview

The AI Proctoring System is a comprehensive online examination platform that combines real-time AI-powered monitoring with automated question management.

### Technology Stack

**Backend:**
- FastAPI 0.109.0 - Modern Python web framework
- MySQL 8.0 - Relational database
- MediaPipe 0.10.9 - Face detection and mesh
- Ultralytics YOLOv8 - Object detection
- OpenCV 4.9.0 - Image processing

**Frontend:**
- HTML5 + CSS3
- Bootstrap 5.3.0 - UI framework
- Vanilla JavaScript (ES6+)
- Alertify.js 1.13.1 - Notifications

**AI Integration:**
- DeepSeek API - Question generation
- MediaPipe Face Detection - Proctoring
- YOLO v8 - Object recognition

## Architecture

### System Flow

```
User → Browser → Frontend (HTML/JS)
                     ↓
                 REST API
                     ↓
              FastAPI Backend
                     ↓
         ┌───────────┼───────────┐
         ↓           ↓           ↓
    MySQL DB   MediaPipe    YOLO Model
                     ↓           ↓
                Proctoring Analysis
                     ↓
               Violation Logs
```

### Database Design

#### Entity Relationship Diagram

```
users (1) ──→ (N) exams (1) ──→ (N) user_answers
   ↓                  ↓
   └──→ questions    violations
```

#### Table Details

**users**
- Primary key: `id`
- Stores: username, password (plain text - should be hashed in production)
- Admin flag for role management

**questions**
- Primary key: `id`
- Four options (A, B, C, D)
- Correct answer stored
- Subject and difficulty categorization

**exams**
- Links user to exam session
- Tracks start/end time
- Stores final score
- Status: in_progress, completed

**user_answers**
- Junction table
- Links exam → question → answer
- Boolean flag for correctness

**violations**
- Logs all proctoring violations
- Severity levels: low, medium, high
- Timestamped entries

## API Documentation

### Authentication Endpoints

#### POST /api/register
Register a new user.

**Request Body:**
```json
{
  "username": "string",
  "password": "string",
  "email": "string (optional)"
}
```

**Response:**
```json
{
  "message": "User registered successfully"
}
```

#### POST /api/login
Authenticate user.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user_id": 1,
  "username": "string",
  "is_admin": false
}
```

### Question Management Endpoints

#### GET /api/questions
Get random questions for exam.

**Query Parameters:**
- `limit` (int, default: 20): Number of questions
- `subject` (string, optional): Filter by subject

**Response:**
```json
{
  "questions": [
    {
      "id": 1,
      "question_text": "string",
      "option_a": "string",
      "option_b": "string",
      "option_c": "string",
      "option_d": "string"
    }
  ],
  "total": 20
}
```

#### POST /api/questions
Create new question (Admin only).

**Request Body:**
```json
{
  "question_text": "string",
  "option_a": "string",
  "option_b": "string",
  "option_c": "string",
  "option_d": "string",
  "correct_answer": "A",
  "subject": "string",
  "difficulty": "easy"
}
```

#### POST /api/questions/generate
Generate questions using AI (Admin only).

**Request Body:**
```json
{
  "subject": "Python Programming",
  "difficulty": "easy",
  "count": 5
}
```

**Response:**
```json
{
  "questions": [...],
  "count": 5
}
```

### Exam Management Endpoints

#### POST /api/exam/start
Start a new exam session.

**Request Body:**
```json
{
  "user_id": 1,
  "exam_name": "General Exam"
}
```

**Response:**
```json
{
  "message": "Exam started",
  "exam_id": 123
}
```

#### POST /api/exam/submit
Submit answer to a question.

**Request Body:**
```json
{
  "exam_id": 123,
  "question_id": 45,
  "user_answer": "B"
}
```

**Response:**
```json
{
  "message": "Answer submitted",
  "is_correct": true
}
```

#### POST /api/exam/finish
Complete exam and calculate score.

**Request Body:**
```json
{
  "exam_id": 123
}
```

**Response:**
```json
{
  "message": "Exam completed",
  "score": 85.5,
  "correct": 17,
  "total": 20
}
```

#### GET /api/exam/results/{exam_id}
Get detailed exam results.

**Response:**
```json
{
  "exam": {...},
  "answers": [...],
  "violations": [...]
}
```

### Proctoring Endpoints

#### POST /api/proctor/analyze
Analyze video frame for violations.

**Request Body:**
- Multipart form data with image file

**Response:**
```json
{
  "violations": [
    {
      "type": "multiple_faces",
      "severity": "high",
      "message": "Multiple faces detected: 2"
    }
  ],
  "face_analysis": {
    "face_count": 2,
    "multiple_faces": true,
    "no_face": false,
    "looking_away": false
  },
  "object_analysis": {
    "suspicious_objects": [
      {
        "object": "cell phone",
        "confidence": 0.89,
        "severity": "high"
      }
    ],
    "severity": "high"
  }
}
```

#### POST /api/proctor/violation
Log a violation to database.

**Request Body (Form Data):**
- exam_id: int
- violation_type: string
- severity: string
- description: string

#### GET /api/proctor/violations/{exam_id}
Get all violations for an exam.

## Proctoring Logic

### Face Detection (MediaPipe)

**Detection Process:**
1. Convert frame BGR → RGB
2. Run MediaPipe face detection
3. Count detected faces
4. Analyze face mesh for gaze direction

**Violation Types:**
- **No Face**: No face detected in frame
- **Multiple Faces**: More than one face detected
- **Looking Away**: Eye gaze deviates from center

**Configuration:**
```python
# Confidence threshold
min_detection_confidence=0.5

# Gaze deviation threshold
if deviation > 0.05:  # 5% deviation
    looking_away = True
```

### Object Detection (YOLO)

**Detection Process:**
1. Load YOLOv8 nano model
2. Run inference on frame
3. Filter for suspicious objects
4. Classify by severity

**Suspicious Objects:**
```python
{
    'cell phone': 'high',
    'laptop': 'high', 
    'tablet': 'high',
    'book': 'medium',
    'remote': 'medium',
    'backpack': 'low'
}
```

**Confidence Threshold:** 0.5 (50%)

### Violation Severity Levels

- **High**: Immediate attention required
  - Multiple faces
  - No face detected
  - Cell phone/laptop/tablet present
  
- **Medium**: Warning level
  - Looking away consistently
  - Books visible
  
- **Low**: Informational
  - Minor movements
  - Background objects

## Frontend Implementation

### State Management

Global variables track exam state:
```javascript
currentUser: null          // User info
currentExam: null          // Exam session
questions: []              // Question array
currentQuestionIndex: 0    // Current position
userAnswers: {}            // Selected answers
violations: []             // Violation log
```

### Camera Integration

```javascript
// Request camera access
videoStream = await navigator.mediaDevices.getUserMedia({ 
    video: { width: 640, height: 480 } 
});

// Capture frame every 3 seconds
setInterval(() => {
    captureAndAnalyze();
}, 3000);
```

### Real-time Updates

- Progress bar updates on answer selection
- Timer updates every second
- Violations displayed immediately
- Questions navigate with state preservation

## Security Considerations

### Current Implementation

⚠️ **WARNING**: This is a demonstration system. For production use:

1. **Password Security**
   - Currently: Plain text storage
   - Required: Hash with bcrypt/argon2
   ```python
   from passlib.hash import bcrypt
   hashed = bcrypt.hash(password)
   ```

2. **Authentication**
   - Currently: No session management
   - Required: JWT tokens or sessions
   ```python
   from fastapi import Depends, HTTPException
   from jose import JWTError, jwt
   ```

3. **CORS Configuration**
   - Currently: Allow all origins (`*`)
   - Required: Restrict to specific domains
   ```python
   allow_origins=["https://yoursite.com"]
   ```

4. **SQL Injection**
   - Currently: Parameterized queries (✓ Good)
   - MySQL connector handles escaping

5. **Input Validation**
   - Currently: Basic Pydantic validation
   - Required: Additional sanitization

### Recommended Improvements

```python
# Add authentication dependency
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id

# Use in endpoints
@app.post("/api/exam/start")
async def start_exam(
    user_id: int = Depends(get_current_user)
):
    ...
```

## Performance Optimization

### Database Optimization

1. **Indexing**
```sql
CREATE INDEX idx_exam_user ON exams(user_id);
CREATE INDEX idx_answer_exam ON user_answers(exam_id);
CREATE INDEX idx_violation_exam ON violations(exam_id);
```

2. **Query Optimization**
- Use `LIMIT` for question selection
- Join tables efficiently in results query
- Consider caching frequently accessed data

### Frontend Optimization

1. **Lazy Loading**
- Load questions on demand
- Cache answered questions

2. **Image Compression**
```javascript
canvas.toBlob(async (blob) => {
    await analyzeFrame(blob);
}, 'image/jpeg', 0.8);  // 80% quality
```

3. **Reduce API Calls**
- Batch violation logs
- Debounce camera captures

### Backend Optimization

1. **Async Processing**
```python
import asyncio

async def process_frame_async(frame):
    face_task = asyncio.create_task(analyze_face(frame))
    object_task = asyncio.create_task(detect_objects(frame))
    return await asyncio.gather(face_task, object_task)
```

2. **Model Caching**
- Load models once at startup
- Reuse model instances

3. **Connection Pooling**
```python
from sqlalchemy import create_engine
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
)
```

## Deployment Guide

### Development

```bash
# Backend
cd backend
python main.py

# Frontend
cd frontend
python -m http.server 3000
```

### Production with Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop
docker-compose down
```

### Production Manual

1. **Setup Reverse Proxy (Nginx)**
```nginx
upstream backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name example.com;
    
    location /api {
        proxy_pass http://backend;
    }
    
    location / {
        root /var/www/proctoring/frontend;
    }
}
```

2. **Use Process Manager**
```bash
# Install PM2
npm install -g pm2

# Start backend
pm2 start backend/main.py --name proctoring-api

# Auto-restart on reboot
pm2 startup
pm2 save
```

3. **Enable HTTPS**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d example.com
```

## Testing

### Unit Tests

```python
# test_backend.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_login():
    response = client.post("/api/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "user_id" in response.json()
```

### Integration Tests

Run the provided test script:
```bash
python test_api.py
```

### Load Testing

```bash
# Install locust
pip install locust

# Create locustfile.py
from locust import HttpUser, task

class ProctoringUser(HttpUser):
    @task
    def login(self):
        self.client.post("/api/login", json={
            "username": "admin",
            "password": "admin123"
        })
    
    @task
    def get_questions(self):
        self.client.get("/api/questions?limit=20")

# Run load test
locust -f locustfile.py
```

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'mediapipe'"**
   ```bash
   pip install mediapipe
   ```

2. **"Can't connect to MySQL server"**
   - Check MySQL is running: `sudo systemctl status mysql`
   - Verify credentials in `.env`
   - Check port 3306 is not blocked

3. **Camera not working**
   - Use HTTPS or localhost
   - Check browser permissions
   - Try different browser

4. **YOLO model download fails**
   ```bash
   # Manual download
   wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
   mkdir -p models
   mv yolov8n.pt models/
   ```

5. **High CPU usage**
   - Reduce frame analysis frequency
   - Use smaller YOLO model
   - Limit concurrent exams

## Future Enhancements

### Planned Features

1. **Advanced Proctoring**
   - Screen recording
   - Browser lock-down mode
   - Audio detection
   - Eye tracking
   - Keystroke analysis

2. **Question Management**
   - Import from CSV/Excel
   - Question categories/tags
   - Difficulty auto-adjustment
   - Question pools

3. **Analytics**
   - Student performance dashboards
   - Violation heat maps
   - Question difficulty analysis
   - Cheating pattern detection

4. **User Experience**
   - Mobile app
   - Offline mode
   - Multi-language support
   - Accessibility features

5. **Security**
   - JWT authentication
   - Password hashing
   - Rate limiting
   - CAPTCHA integration
   - IP whitelisting

6. **Integration**
   - LMS integration (Moodle, Canvas)
   - Email notifications
   - Calendar scheduling
   - Video conferencing

### Contribution Guidelines

1. Fork the repository
2. Create feature branch
3. Write tests
4. Submit pull request

## License

This project is provided as-is for educational purposes.

## Support

For technical support:
- GitHub Issues
- Documentation: This file
- API Tests: `test_api.py`

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Authors:** AI Development Team
