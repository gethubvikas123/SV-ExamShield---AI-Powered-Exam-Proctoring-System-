# 🎓 AI-Powered Proctoring System

A complete end-to-end online examination system with AI-powered proctoring capabilities using MediaPipe for face detection and YOLO for object detection.

## ✨ Features

### Core Features
- ✅ **Real-time Proctoring**: MediaPipe face detection + YOLO object detection
- ✅ **AI Question Generation**: DeepSeek API integration for automatic question creation
- ✅ **MySQL Database**: Store questions, answers, users, and violations
- ✅ **FastAPI Backend**: High-performance REST API
- ✅ **Bootstrap Frontend**: Responsive and modern UI
- ✅ **Alertify Notifications**: User-friendly alerts and notifications

### Proctoring Capabilities
- **Face Detection**: Multiple faces, no face detected, looking away detection
- **Object Detection**: Detects suspicious objects (phones, books, laptops, tablets)
- **Violation Logging**: All violations stored in database with timestamps
- **Real-time Monitoring**: Live video feed with instant violation alerts

### Exam Features
- Maximum 20 questions per exam
- Multiple-choice questions (A, B, C, D)
- User answers and correct answers stored
- Automatic scoring
- Progress tracking
- Timer for exam duration
- Detailed results with question-by-question breakdown

### Admin Features
- AI question generation using DeepSeek
- Manual question creation
- View all questions with answers
- Generate questions by subject and difficulty

## 🏗️ Architecture

```
proctoring-system/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # MySQL connection
│   ├── face_proctoring.py      # MediaPipe face detection
│   ├── object_detection.py     # YOLO object detection
│   └── question_generator.py   # DeepSeek AI integration
├── frontend/
│   ├── index.html              # Main HTML interface
│   └── app.js                  # JavaScript application
├── models/                     # YOLO models (auto-downloaded)
├── schema.sql                  # Database schema
├── requirements.txt            # Python dependencies
└── .env.example               # Environment variables template
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Webcam (for proctoring)
- Modern web browser (Chrome/Firefox/Edge)

### Step 1: Clone or Create Project

```bash
# Create project directory
mkdir proctoring-system
cd proctoring-system
```

### Step 2: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Setup MySQL Database

```bash
# Login to MySQL
mysql -u root -p

# Create database and import schema
mysql -u root -p < schema.sql
```

Or manually:
```sql
CREATE DATABASE proctoring_db;
USE proctoring_db;
-- Then copy and paste the contents of schema.sql
```

### Step 4: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
nano .env
```

Update the following:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=proctoring_db
DEEPSEEK_API_KEY=your_api_key  # Optional
```

### Step 5: Run the Application

```bash
# Start FastAPI backend
cd backend
python main.py

# Or using uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### Step 6: Open Frontend

```bash
# Option 1: Using Python's HTTP server
cd frontend
python -m http.server 3000

# Option 2: Open index.html directly in browser
# Just double-click index.html or open it with your browser
```

Frontend will be available at: `http://localhost:3000` (if using http.server)

## 📖 Usage Guide

### For Students

1. **Login/Register**
   - Open the application
   - Use default credentials: `admin` / `admin123` (or register new account)
   - Non-admin users automatically start exam

2. **Take Exam**
   - Allow camera access when prompted
   - Answer questions one by one
   - System monitors for violations:
     - Multiple faces in frame
     - No face detected
     - Looking away from screen
     - Suspicious objects (phone, books, etc.)
   - Navigate using Previous/Next buttons
   - Submit when finished

3. **View Results**
   - See final score and correct/incorrect answers
   - View violation log
   - Review each question with correct answers

### For Admins

1. **Login**
   - Username: `admin`
   - Password: `admin123`

2. **Generate Questions (AI)**
   - Click "Generate Questions" tab
   - Enter subject (e.g., "Python Programming")
   - Select difficulty level
   - Choose number of questions
   - Click "Generate"

3. **Add Manual Questions**
   - Click "Add Manual Question" tab
   - Fill in question and all four options
   - Select correct answer
   - Click "Add Question"

4. **View All Questions**
   - Click "View All Questions" tab
   - See all questions with correct answers
   - Review and manage question bank

5. **Start Student Exam**
   - Click "Start Student Exam" button to test the exam interface

## 🔧 Configuration

### Camera Settings
Edit `frontend/app.js`:
```javascript
videoStream = await navigator.mediaDevices.getUserMedia({ 
    video: { 
        width: 640, 
        height: 480,
        facingMode: 'user'  // Use front camera
    } 
});
```

### Proctoring Sensitivity
Edit `backend/face_proctoring.py`:
```python
# Adjust detection confidence
self.face_detection = self.mp_face_detection.FaceDetection(
    model_selection=1, 
    min_detection_confidence=0.5  # Lower = more sensitive
)

# Adjust looking away threshold
if deviation > 0.05:  # Adjust this value (0.01 - 0.1)
    violations['looking_away'] = True
```

### Proctoring Frequency
Edit `frontend/app.js`:
```javascript
// Capture frame every 3 seconds (3000ms)
proctoringInterval = setInterval(() => {
    captureAndAnalyze();
}, 3000);  // Change this value
```

### Suspicious Objects
Edit `backend/object_detection.py`:
```python
self.suspicious_objects = {
    'cell phone': 'high',
    'book': 'medium',
    'laptop': 'high',
    'tablet': 'high',
    # Add more objects...
}
```

## 📊 Database Schema

### Tables
- **users**: User accounts (students and admins)
- **questions**: Question bank with options and answers
- **exams**: Exam sessions and scores
- **user_answers**: Student responses to questions
- **violations**: Proctoring violation logs

### Default Admin Account
- Username: `admin`
- Password: `admin123`
- Email: `admin@proctoring.com`

## 🔌 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - User login

### Questions
- `GET /api/questions?limit=20` - Get random questions
- `GET /api/questions/all` - Get all questions (admin)
- `POST /api/questions` - Create question (admin)
- `POST /api/questions/generate` - Generate questions with AI (admin)

### Exam
- `POST /api/exam/start` - Start new exam
- `POST /api/exam/submit` - Submit answer
- `POST /api/exam/finish` - Finish exam
- `GET /api/exam/results/{exam_id}` - Get exam results

### Proctoring
- `POST /api/proctor/analyze` - Analyze frame for violations
- `POST /api/proctor/violation` - Log violation
- `GET /api/proctor/violations/{exam_id}` - Get all violations

### Statistics
- `GET /api/stats/user/{user_id}` - Get user statistics

## 🤖 AI Question Generation

### Using DeepSeek API

1. Get API key from [https://platform.deepseek.com/](https://platform.deepseek.com/)
2. Add to `.env` file:
   ```env
   DEEPSEEK_API_KEY=your_api_key_here
   ```
3. Update `backend/main.py`:
   ```python
   # Change from LocalQuestionGenerator to QuestionGenerator
   question_gen = QuestionGenerator()
   ```

### Using Local Generation
The system includes a fallback `LocalQuestionGenerator` with predefined templates for:
- Python Programming
- Mathematics
- General topics

Add more subjects in `backend/question_generator.py`.

## 🎨 Customization

### Theme Colors
Edit `frontend/index.html` CSS:
```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Exam Settings
Edit `frontend/app.js`:
```javascript
// Maximum questions per exam
await loadQuestions(20);  // Change to any number

// Timer display format
document.getElementById('timer').textContent = 
    `${minutes}:${seconds}`;
```

## 🐛 Troubleshooting

### Camera Not Working
- Ensure you're using HTTPS or localhost
- Check browser permissions
- Try different browser
- Check if camera is already in use

### Database Connection Failed
```bash
# Check MySQL is running
sudo systemctl status mysql

# Verify credentials in .env
# Test connection manually:
mysql -h localhost -u root -p
```

### YOLO Model Download Issues
```python
# The model downloads automatically on first run
# If it fails, download manually from:
# https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
# Place in: /models/yolov8n.pt
```

### CORS Errors
- Ensure backend is running on `localhost:8000`
- Update `API_URL` in `frontend/app.js` if needed
- Check CORS middleware in `backend/main.py`

## 📝 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Support

For issues or questions, please open an issue on the repository.

## 🎯 Roadmap

- [ ] Advanced face recognition
- [ ] Audio proctoring
- [ ] Screen recording
- [ ] Browser lock-down
- [ ] Multi-language support
- [ ] Export results to PDF
- [ ] Email notifications
- [ ] Question import/export
- [ ] Bulk question upload
- [ ] Advanced analytics dashboard

## 🌟 Acknowledgments

- **MediaPipe** - Face detection and tracking
- **Ultralytics YOLOv8** - Object detection
- **FastAPI** - Modern web framework
- **Bootstrap 5** - Frontend framework
- **Alertify.js** - Beautiful notifications
- **DeepSeek** - AI question generation

---

Made with ❤️ for online education
