@echo off
echo ========================================
echo   Python Engine - Direct Path Method
echo ========================================
echo.

REM Common Python paths - EDIT THIS if Python is in different location
set PYTHON_DIR=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312
set PYTHON_EXE=%PYTHON_DIR%\python.exe
set PIP_EXE=%PYTHON_DIR%\Scripts\pip.exe

echo [1] Checking Python at: %PYTHON_DIR%
if not exist "%PYTHON_EXE%" (
    echo [X] Python not found at: %PYTHON_DIR%
    echo.
    echo Please edit this file and set PYTHON_DIR to your Python location.
    echo Common locations:
    echo   C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312
    echo   C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312-64
    echo   C:\Python312
    echo.
    pause
    exit /b 1
)

echo [OK] Python found!
"%PYTHON_EXE%" --version

echo.
echo [2] Creating virtual environment...
if not exist "venv\Scripts\activate.bat" (
    "%PYTHON_EXE%" -m venv venv
    if %errorlevel% neq 0 (
        echo [X] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)

echo.
echo [3] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [X] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

echo.
echo [4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [X] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

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


