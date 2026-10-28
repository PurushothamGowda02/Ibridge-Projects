@echo off
REM RFM Analysis Project - Quick Start Script for Windows
REM This script sets up and runs both backend and frontend

echo.
echo ========================================
echo RFM Analysis Project - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✓ Python found: 
python --version
echo ✓ Node.js found: 
node --version
echo.

REM Setup Backend
echo ========================================
echo Setting up Backend...
echo ========================================
cd backend

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)

echo ✓ Backend setup complete
echo.

REM Setup Frontend
echo ========================================
echo Setting up Frontend...
echo ========================================
cd ..\frontend

if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Failed to install frontend dependencies
        pause
        exit /b 1
    )
)

echo ✓ Frontend setup complete
echo.

REM Start servers
echo ========================================
echo Starting Servers...
echo ========================================
echo.
echo Backend will start on: http://localhost:8000
echo Frontend will start on: http://localhost:3000
echo.
echo Press Ctrl+C to stop the servers
echo.

REM Start backend in new window
cd ..\backend
call .venv\Scripts\activate.bat
start "RFM Backend" cmd /k "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start frontend in new window
cd ..\frontend
start "RFM Frontend" cmd /k "npm start"

echo.
echo ========================================
echo ✓ Project Started Successfully!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Close this window or press Ctrl+C to stop
echo.

pause
