@echo off
REM I Got You - Startup Script (Windows)
REM This script starts both the frontend and backend servers

echo.
echo ================================================================
echo            Starting I Got You Application
echo ================================================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please create a .env file with your API keys.
    echo See SETUP_GUIDE.md for details.
    echo.
    exit /b 1
)

echo Checking prerequisites...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    exit /b 1
)

REM Check Node
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed
    exit /b 1
)

echo All prerequisites met
echo.

echo ================================================================
echo Starting Backend Server (Python/FastAPI)...
echo ================================================================
echo.

REM Start backend in new window
start "I Got You - Backend" cmd /k "cd backend && python main.py"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

echo.
echo ================================================================
echo Starting Frontend Server (Next.js)...
echo ================================================================
echo.

REM Start frontend in new window
start "I Got You - Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ================================================================
echo              Servers Starting!
echo ================================================================
echo.
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the servers.
echo.

pause
