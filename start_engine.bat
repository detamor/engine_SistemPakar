@echo off
echo ========================================
echo   STARTING PYTHON ENGINE SERVER
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.11 or 3.12
    pause
    exit /b 1
)

echo.
echo [2/3] Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated!
) else (
    echo WARNING: Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo [3/3] Starting FastAPI server...
echo.
echo Server will run on: http://localhost:8001
echo Health check: http://localhost:8001/health
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

pause
