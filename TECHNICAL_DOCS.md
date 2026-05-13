# 🛡️ SV ExamShield - AI Powered Online Exam Proctoring System

SV ExamShield is a full-stack AI-powered online exam proctoring system designed to maintain academic integrity during remote examinations using real-time monitoring, face detection, object detection, and automated violation tracking.

The system combines computer vision, browser activity monitoring, and intelligent violation analysis to provide a secure online examination environment for educational institutions.

---

# 🚀 Features

## 🎥 AI-Based Proctoring

### 👤 Face Detection (MediaPipe)
- Real-time face tracking
- Multiple face detection
- No-face detection
- Looking-away detection
- Progressive warning system

### 📱 Object Detection (Simplified Mode)
Current implementation uses simplified detection for stability:
- **Mock Detection Mode**: Prevents dependency conflicts
- **Suspicious Objects Database**: Cell phones, tablets, books, laptops, remotes
- **Severity Classification**: High (phones, tablets, laptops), Medium (books, remotes), Low (peripherals)
- **Real YOLO Ready**: Can be enabled when ultralytics/torch dependencies are resolved

### 🛑 Browser Monitoring
- Tab switching detection
- Window focus tracking
- Copy/paste prevention
- Keyboard shortcut blocking
- Right-click prevention

---

# 📝 Smart Exam System

## 📚 Preloaded Question Bank

The system uses a preloaded database of questions.

### Question Generation System
- **Hybrid Approach**: Groq AI API + 120 Pre-loaded Questions
- **Groq API**: Generates questions on-demand when API key is available
- **Fallback Mode**: Uses pre-loaded question bank if Groq is unavailable
- **Pre-loaded Bank**: 120 curated questions (10 per subject × 3 difficulty levels)
- **Random Selection**: Questions are shuffled during exam to prevent pattern memorization

### Supported Categories
- Mathematics
- Data Science
- Machine Learning
- Science
- Programming

### Features
- Random question selection
- Difficulty categorization
- Subject-based filtering
- Instant evaluation
- Auto scoring

---

# ⚖️ Progressive Violation System

Violations are categorized into severity levels:

| Severity | Examples |
|---|---|
| 🔴 High | Multiple faces, phone detection, tab switching |
| 🟡 Medium | Looking away, books detected |
| 🟢 Low | Minor distractions |

The system provides warnings before terminating the exam session.

---

# 📊 Audit & Logging

- Timestamped violation logs
- User-specific tracking
- Detailed exam reports
- Exam history storage
- Result analytics

---

# 👨‍💻 Admin Features

- Manage question bank
- View exam results
- Monitor violations
- Configure exam settings
- Review student activity

---

### API Endpoints

#### User Management
- `POST /api/register` - Register new user
- `POST /api/login` - User login

#### Question Management
- `GET /api/questions` - Get random questions (max 20)
- `POST /api/questions` - Create question (admin)
- `GET /api/questions/all` - Get all questions (admin)
- `POST /api/questions/generate` - Generate AI questions (requires Groq API)

#### Exam Management
- `POST /api/exam/start` - Start new exam
- `POST /api/exam/submit` - Submit answer
- `POST /api/exam/finish` - End exam and calculate score
- `GET /api/exam/results/{exam_id}` - Get detailed results

#### Proctoring
- `POST /api/proctor/analyze` - Analyze frame for violations
- `POST /api/proctor/violation` - Log violation
- `GET /api/proctor/violations/{exam_id}` - Get exam violations

#### Statistics
- `GET /api/stats/user/{user_id}` - Get user performance stats

---

# 👨‍🎓 Student Features

- Simple exam interface
- Live timer
- Real-time warnings
- Instant result generation
- Progress tracking

---

# 🛠️ Tech Stack

## Backend
- FastAPI
- Python
- MySQL
- OpenCV

## AI/ML
- MediaPipe
- Groq API (for question generation)
- Simplified Object Detection (YOLO integration available)
- Computer Vision

## Frontend
- HTML5
- CSS3
- JavaScript (ES6)
- Bootstrap 5
- Alertify.js

---

# 🧠 AI Proctoring Workflow

```text
Camera Feed
     ↓
Face Detection (MediaPipe)
     ↓
Object Detection (Simplified Mode)
     ↓
Violation Analysis
     ↓
Warning System
     ↓
Violation Logging
```

---

# 📂 Project Structure

```text
proctoring-system/
│
├── backend/
│   ├── main.py
│   ├── test_api.py
│   ├── requirements.txt
│   ├── .env
│   └── ...
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   ├── vendor/
│   └── ...
│
└── README.md
```

---

# ⚡ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/gethubvikas123/SV-ExamShield---AI-Powered-Exam-Proctoring-System-.git
```

---

## 2️⃣ Navigate to Project

```bash
cd SV-ExamShield---AI-Powered-Exam-Proctoring-System-
```

---

## 3️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5️⃣ Configure Database

Update database credentials inside:

```text
backend/.env
```

Example:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=examshield
```

---

## 6️⃣ Run Backend

```bash
cd backend
python main.py
```

---

## 7️⃣ Run Frontend

```bash
cd frontend
python -m http.server 3000
```

Open:

```text
http://localhost:3000
```

---

# 🔒 Security Notes

Current version is for educational/demo purposes.

Recommended production improvements:
- JWT Authentication
- Password hashing
- HTTPS deployment
- Role-based authorization
- Rate limiting

---

# 📈 Future Enhancements

- Eye tracking
- Audio monitoring
- LMS integration
- Mobile support
- Advanced analytics
- Browser lockdown mode

---

# 🤝 Contributing

Pull requests are welcome.

Steps:
1. Fork repository
2. Create feature branch
3. Commit changes
4. Open pull request

---

# 📄 License

This project is for educational purposes only.

---

# 👨‍💻 Author

Vikas
