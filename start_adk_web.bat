@echo off
REM Start ADK Web Interface for IGotYou Agent (Windows)
REM This launches Google's ADK built-in web chat UI for your agent

echo ==================================================
echo 🚀 Starting ADK Web Interface for IGotYou Agent
echo ==================================================
echo.
echo 📍 Loading agent from: IGotYou/agent.py
echo 🌐 Web interface will be available at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ==================================================
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Run the ADK web interface pointing to your agent
adk web IGotYou/agent.py

echo.
echo 👋 ADK Web Interface stopped
pause
