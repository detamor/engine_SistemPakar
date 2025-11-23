@echo off
echo ========================================
echo   Starting Python Engine Server
echo ========================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [X] Virtual environment not found!
    echo Please run SETUP_NOW.bat first
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting FastAPI server...
echo.
echo Server will run on: http://localhost:8001
echo API docs: http://localhost:8001/docs
echo Press Ctrl+C to stop
echo.
echo ========================================
echo.

uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

pause

