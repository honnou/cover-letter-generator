@echo off
echo ==========================================
echo    Cover Letter Generator - Startup
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [WARNING] Installation failed. Please check your Python installation.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo    Starting Server and Opening Browser
echo ==========================================
echo.

echo [START] Starting backend server on http://localhost:8080
echo.
echo Tips:
echo    - Set ANTHROPIC_API_KEY for AI-powered generation
echo    - Press Ctrl+C to stop the server
echo.

REM Open browser after a short delay
start "" index.html

REM Start the server
python server.py
