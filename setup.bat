@echo off
echo ============================================
echo AI Proctoring System - Quick Start (Windows)
echo ============================================
echo.

REM Check Python
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file
if not exist .env (
    echo.
    echo Creating .env file...
    copy .env.example .env
    echo WARNING: Please edit .env file with your MySQL credentials!
)

REM Setup database
echo.
set /p setup_db="Do you want to setup the database now? (y/n): "
if /i "%setup_db%"=="y" (
    echo Setting up database...
    set /p mysql_password="MySQL root password: "
    mysql -u root -p%mysql_password% < schema.sql
    echo Database created successfully!
)

echo.
echo ============================================
echo Setup Complete!
echo.
echo To start the application:
echo 1. Edit .env with your settings
echo 2. Start backend: cd backend && python main.py
echo 3. Open frontend: Open frontend\index.html in browser
echo.
echo Default admin credentials:
echo Username: admin
echo Password: admin123
echo.
echo ============================================
pause
