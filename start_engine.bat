@echo off
echo ========================================
echo   STARTING PYTHON ENGINE SERVER
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python...

REM Try different python commands
where python >nul 2>&1
if errorlevel 1 (
    where python3 >nul 2>&1
    if errorlevel 1 (
        where py >nul 2>&1
        if errorlevel 1 (
            echo ERROR: Python not found in PATH!
            echo Please install Python and add it to PATH
            pause
            exit /b 1
        ) else (
            set PYTHON_CMD=py
        )
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

%PYTHON_CMD% --version
echo Python found OK!

echo.
echo [2/3] Setting up virtual environment...
if exist "venv\Scripts\activate.bat" (
    echo Virtual environment found, activating...
    call venv\Scripts\activate.bat
    echo Virtual environment activated!
) else (
    echo Creating new virtual environment...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
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
