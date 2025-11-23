@echo off
echo ========================================
echo   Setup Python Engine - Quick Start
echo ========================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [X] Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment created

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [X] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo You should see (venv) in your prompt now

echo.
echo [3/4] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [X] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

echo.
echo [4/4] Setup complete!
echo.
echo ========================================
echo   To start the engine, run:
echo   start_server.bat
echo.
echo   Or manually:
echo   venv\Scripts\activate
echo   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
echo ========================================
echo.
pause

