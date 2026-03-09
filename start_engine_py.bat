@echo off
echo ========================================
echo   System Pakar Python Engine
echo   (Using py launcher)
echo ========================================
echo.

echo [1/4] Checking Python...
set PYTHON_CMD=py
py --version >nul 2>&1
if errorlevel 1 (
    echo [!] 'py' launcher not found, trying 'python'...
    python --version >nul 2>&1
    if errorlevel 1 (
        echo [X] ERROR: Python not found!
        echo.
        echo Please install Python 3.11 or 3.12 from:
        echo https://www.python.org/downloads/
        echo.
        echo IMPORTANT: Check "Add Python to PATH" during installation
        echo.
        echo After installation, restart this script.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python
    )
)
echo [OK] Python found
%PYTHON_CMD% --version

echo.
echo [2/4] Checking virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo [!] Virtual environment not found, creating...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo [X] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)

echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [X] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

echo.
echo [4/4] Checking dependencies...
if not exist "venv\Lib\site-packages\fastapi" (
    echo [!] Dependencies not installed, installing...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [X] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies installed
)

echo.
echo ========================================
echo   Starting FastAPI server...
echo ========================================
echo.
echo Server will run on: http://localhost:8001
echo API docs: http://localhost:8001/docs
echo Press Ctrl+C to stop
echo.
echo ========================================
echo.

uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

pause



