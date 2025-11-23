@echo off
echo ========================================
echo   Python Installation Checker (Simple)
echo ========================================
echo.

echo [1] Testing 'py' launcher...
py --version
if %errorlevel% equ 0 (
    echo [OK] 'py' launcher works!
    set PYTHON_CMD=py
    goto :create_venv
)

echo.
echo [2] Testing 'python' command...
python --version
if %errorlevel% equ 0 (
    echo [OK] 'python' command works!
    set PYTHON_CMD=python
    goto :create_venv
)

echo.
echo [X] ERROR: Python not found!
echo.
echo Please install Python 3.11 or 3.12 from:
echo https://www.python.org/downloads/
echo.
echo IMPORTANT: Check "Add Python to PATH" during installation
echo.
pause
exit /b 1

:create_venv
echo.
echo [3] Creating virtual environment...
if exist "venv\Scripts\activate.bat" (
    echo [OK] Virtual environment already exists
) else (
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo [X] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

echo.
echo [4] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [X] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

echo.
echo [5] Checking dependencies...
if exist "venv\Lib\site-packages\fastapi" (
    echo [OK] Dependencies already installed
) else (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [X] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
)

echo.
echo ========================================
echo   All checks passed! Python is ready.
echo ========================================
echo.
echo You can now run:
echo   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
echo.
echo Or use: start_engine_py.bat
echo.
pause


