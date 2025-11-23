@echo off
echo ========================================
echo   Python Installation Checker
echo ========================================
echo.

echo [1/5] Checking Python...
echo Trying 'py' launcher first...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 'py' launcher not found, trying 'python'...
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [X] Python NOT FOUND!
        echo.
        echo Please install Python 3.11 or 3.12 from:
        echo https://www.python.org/downloads/
        echo.
        echo IMPORTANT: Check "Add Python to PATH" during installation
        echo.
        echo Or add Python to PATH manually (see ADD_PYTHON_TO_PATH.md)
        echo.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python
        echo [OK] Python found (using 'python'):
        python --version
    )
) else (
    set PYTHON_CMD=py
    echo [OK] Python found (using 'py' launcher):
    py --version
)

echo.
echo [2/5] Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] pip NOT FOUND!
    echo.
    echo Try: python -m ensurepip --upgrade
    pause
    exit /b 1
) else (
    echo [OK] pip found:
    pip --version
)

echo.
echo [3/5] Checking virtual environment...
if exist "venv\Scripts\activate.bat" (
    echo [OK] Virtual environment exists
) else (
    echo [!] Virtual environment not found
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo [X] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

echo.
echo [4/5] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [X] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

echo.
echo [5/5] Checking dependencies...
if exist "venv\Lib\site-packages\fastapi" (
    echo [OK] Dependencies installed
) else (
    echo [!] Dependencies not installed
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
echo Or use: start_engine.bat
echo.
pause

