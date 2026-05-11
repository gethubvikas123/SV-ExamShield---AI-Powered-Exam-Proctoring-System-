# 🚀 QUICK START GUIDE

## Get Up and Running in 5 Minutes

### Prerequisites Check
- ✅ Python 3.8+ installed
- ✅ MySQL 8.0+ installed and running
- ✅ Webcam connected
- ✅ Modern browser (Chrome/Firefox/Edge)

### Step 1: Extract Files
```bash
# Extract the project to a folder
cd proctoring-system
```

### Step 2: Install Dependencies

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
setup.bat
```

**Manual Installation:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 3: Setup Database

```bash
# Login to MySQL
mysql -u root -p

# Run the schema
mysql -u root -p < schema.sql

# Or copy-paste schema.sql contents in MySQL
```

### Step 4: Configure Environment

```bash
# Copy example env
cp .env.example .env

# Edit with your MySQL password
nano .env
```

Update this line:
```
DB_PASSWORD=your_mysql_password
```

### Step 5: Start Backend

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 6: Open Frontend

**Option 1 - Direct (Easiest):**
- Just double-click `frontend/index.html`
- Or drag it into your browser

**Option 2 - HTTP Server:**
```bash
cd frontend
python -m http.server 3000
```
Then open: http://localhost:3000

### Step 7: Login and Test

**Admin Login:**
- Username: `admin`
- Password: `admin123`

**Test the System:**
1. Allow camera access when prompted
2. Generate some questions (Admin Panel → Generate Questions)
3. Start Student Exam
4. Answer questions while being monitored
5. Check violations log in real-time
6. Submit and view results

## 🎯 Quick Test Commands

### Test Backend is Running
```bash
curl http://localhost:8000/
```

### Run API Tests
```bash
python test_api.py
```

## 🐛 Quick Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### MySQL Connection Failed
```bash
# Check MySQL is running
sudo systemctl status mysql

# Restart MySQL
sudo systemctl restart mysql
```

### Camera Not Working
- Use Chrome or Firefox
- Must be HTTPS or localhost
- Check browser camera permissions
- Close other apps using camera

### Module Not Found
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

## 📁 Project Structure

```
proctoring-system/
├── backend/              # FastAPI backend
│   ├── main.py          # Main API application
│   ├── database.py      # MySQL connection
│   ├── face_proctoring.py
│   ├── object_detection.py
│   └── question_generator.py
├── frontend/            # HTML/JS frontend
│   ├── index.html       # Main interface
│   └── app.js          # JavaScript logic
├── schema.sql          # Database schema
├── requirements.txt    # Python packages
└── README.md          # Full documentation
```

## 🎓 Usage Tips

### For Students:
- Ensure good lighting for face detection
- Keep phone and books away from view
- Look at the screen (not away)
- Don't have other people in frame

### For Admins:
- Generate questions before exams
- Monitor violation logs
- Review exam results regularly
- Adjust proctoring sensitivity as needed

## 📞 Need Help?

1. Check `README.md` for full documentation
2. Check `TECHNICAL_DOCS.md` for technical details
3. Run `python test_api.py` to test all endpoints
4. Check browser console for JavaScript errors
5. Check terminal for Python errors

## 🎉 You're Ready!

The system is now running. Start taking exams with AI proctoring!

**Default Features Active:**
- ✅ Face detection
- ✅ Object detection
- ✅ Violation logging
- ✅ Automatic scoring
- ✅ Real-time monitoring

**Happy Testing! 🚀**
