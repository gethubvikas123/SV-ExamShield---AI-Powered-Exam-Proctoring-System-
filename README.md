# 🛡️ SV ExamShield - AI-Powered Online Exam Proctoring System

An intelligent, full-stack exam proctoring solution that leverages AI and computer vision to ensure academic integrity in remote assessments. Monitor exams in real-time, detect violations automatically, and maintain fairness with progressive warnings.

https://github.com/user-attachments/assets/4b1792fc-c8d0-4f7b-a526-9fd5b615b8e4

## 🎯 Overview

SV ExamShield is a comprehensive proctoring system designed for educational institutions conducting remote exams. It uses artificial intelligence to monitor students in real-time while maintaining fairness through a progressive warning system.

### **Why SV ExamShield?**

- 🎓 **Built for Education** - Designed specifically for academic integrity
- 🤖 **AI-Powered** - Advanced face and object detection
- ⚖️ **Fair & Ethical** - Progressive warnings before termination
- 🆓 **Cost-Effective** - No expensive hardware required
- 📊 **Complete Audit Trail** - Detailed violation logs for review
- 🌐 **Remote-Ready** - Perfect for online education

## ✨ Features

### 🔍 **Intelligent Monitoring**

#### **Face Detection (MediaPipe)**
- ✅ Real-time face tracking
- ✅ Multiple face detection (catches impersonation)
- ✅ No face detection (student left seat)
- ✅ Gaze direction tracking (looking away)
- ✅ 95%+ accuracy in various lighting conditions

#### **Object Recognition (YOLO v8)**
- ✅ Unauthorized device detection (phones, tablets)
- ✅ Study material detection (books, notes)
- ✅ Secondary screen detection (laptops)
- ✅ Confidence-based filtering (reduces false positives)
- ✅ Custom severity levels (High/Medium/Low)

#### **Behavior Monitoring**
- ✅ Tab switching detection
- ✅ Window focus tracking
- ✅ Keyboard shortcut blocking (Ctrl+C, F12, etc.)
- ✅ Right-click prevention
- ✅ Copy/paste prevention

### 📝 **Exam Management**

### **Smart Question System**
- 📚 120 pre-loaded questions (Math, Data Science, ML, Science)
- 🎲 Random question selection (prevents cheating)
- 🏷️ Subject and difficulty categorization
- ♾️ Template-based unlimited question generation
- 🚫 No AI dependency for basic questions (fast & reliable)

### **Automated Assessment**
- ⚡ Instant grading (100% accuracy)
- 📊 Detailed score breakdowns
- ✅ Question-by-question analysis
- 📈 Performance metrics
- 📄 Exportable results

### **Progressive Violation System**
Violation Count → Action
─────────────────────────────────────
1-2 violations  → Warning notification
3 violations    → Final warning popup
4 violations    → Critical alert
5 violations    → Auto-terminate exam
```

### **Violation Classification**
- 🔴 **High Severity** - Multiple faces, phones, tab switching
- 🟡 **Medium Severity** - Looking away, blocked shortcuts
- 🟢 **Low Severity** - Brief distractions, minor infractions

### **Complete Audit Trail**
- 📝 Timestamped violation logs
- 🎥 Frame-by-frame analysis records
- 📊 Severity classifications
- 👤 User-specific violation history
- 📄 Exportable reports for disputes

## 👥 **User Management**

### **Admin Panel**
- 🎛️ Question generation and management
- 👀 View all exams and results
- 📊 Analytics dashboard
- 🔧 System configuration
- 📋 Violation review interface

### **Student Interface**
- 📱 Clean, intuitive exam UI
- ⏱️ Real-time timer
- 📊 Progress tracking
- ⚠️ Violation warnings
- 📝 Instant results

---

## 🛠️ Tech Stack

### **Backend**
python
Framework:       FastAPI 0.104+
Language:        Python 3.8+
Database:        MySQL 8.0+
ORM:             MySQL Connector Python
Environment:     python-dotenv

### **AI/ML Components**
python
Face Detection:  MediaPipe 0.10.0
Object Detection: YOLOv8 (Ultralytics 8.0.200)
Computer Vision: OpenCV 4.8+
Image Processing: NumPy, PIL

### **Frontend**
javascript
HTML5:           Semantic markup
CSS3:            Custom styling + Bootstrap 5
JavaScript:      ES6+ (Vanilla)
UI Framework:    Bootstrap 5.3
Notifications:   Alertify.js


## 📂 Project Structure
<img width="529" height="255" alt="image" src="https://github.com/user-attachments/assets/b9636db0-7c70-43da-8bd9-8c58816d3fa9" />

### **Detailed File Breakdown**

| Component | Files | Lines | Purpose |
|-----------|-------|-------|---------|
| Backend API | 5 Python files | ~1,400 | REST API, business logic |
| Database | 1 SQL file | ~150 | Schema, default data |
| AI/ML | 2 Python files | ~350 | Face & object detection |
| Frontend UI | 1 HTML + 1 CSS + 1 JS | ~2,000 | User interface |
| Documentation | 6 Markdown files | ~3,000 | Guides, API docs |
| **Total** | **20+ files** | **~7,000** | Complete system |

### **Exam Flow**
┌─────────────────────────────────────────────┐
│ 1. LOGIN                                    │
│    - Enter username & password              │
│    - System loads your profile              │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ 2. CAMERA PERMISSION                        │
│    - Browser requests webcam access         │
│    - Click "Allow"                          │
│    - System initializes proctoring          │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ 3. ANTI-CHEATING WARNING                    │
│    - Read monitored behaviors               │
│    - Understand violation consequences      │
│    - Click "OK" to acknowledge              │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ 4. START EXAM                               │
│    - Questions load                         │
│    - Timer starts                           │
│    - Proctoring begins                      │
│    - Tab detection active                   │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ 5. ANSWER QUESTIONS                         │
│    - Read question carefully                │
│    - Select answer (A/B/C/D)                │
│    - Answer auto-saves                      │
│    - Navigate: Previous / Next              │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ 6. SUBMIT EXAM                              │
│    - Review answered questions              │
│    - Click "Submit Exam"                    │
│    - Confirm submission                     │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ 7. VIEW RESULTS                             │
│    - See score (%)                          │
│    - Correct vs Total answers               │
│    - Violation count                        │
│    - Question-by-question breakdown         │
└─────────────────────────────────────────────┘

### **Do's and Don'ts**

✅ **DO:**
- Keep your face visible in the camera
- Look at the screen during the exam
- Stay in your seat
- Have good lighting
- Use a quiet environment
- Keep exam window focused

❌ **DON'T:**
- Leave your seat during exam
- Have other people in the room
- Use phones or tablets
- Open other tabs/windows
- Use books or notes
- Try to copy/paste
- Attempt to open developer tools

### **Violation Warnings**

<img width="418" height="196" alt="image" src="https://github.com/user-attachments/assets/4bb01c33-558c-4bca-b32e-0a4f0ec90f53" />


