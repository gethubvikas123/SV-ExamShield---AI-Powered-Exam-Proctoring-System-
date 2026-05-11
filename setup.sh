#!/bin/bash

echo "🎓 AI Proctoring System - Quick Start Script"
echo "=============================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Python 3 not found. Please install Python 3.8+"; exit 1; }

# Check MySQL
echo "Checking MySQL..."
which mysql || { echo "MySQL not found. Please install MySQL 8.0+"; exit 1; }

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || { echo "Failed to activate venv"; exit 1; }

# Install dependencies
echo ""
echo "Installing Python dependencies (this may take a few minutes)..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your MySQL credentials!"
    echo "   Run: nano .env"
fi

# Setup database
echo ""
read -p "Do you want to setup the database now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Setting up database..."
    read -p "MySQL root password: " -s mysql_password
    echo ""
    mysql -u root -p$mysql_password < schema.sql
    echo "✅ Database created successfully!"
fi

# Download YOLO model (optional - will auto-download on first run)
echo ""
echo "YOLO model will be downloaded automatically on first run."

echo ""
echo "=============================================="
echo "✅ Setup Complete!"
echo ""
echo "To start the application:"
echo "1. Edit .env with your settings: nano .env"
echo "2. Start backend: cd backend && python main.py"
echo "3. Open frontend: Open frontend/index.html in browser"
echo ""
echo "Default admin credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "=============================================="
