@echo off
echo ========================================
echo   Checking Experta Installation
echo ========================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run start_engine.bat first
    pause
    exit /b 1
)

echo.
echo Checking if experta is installed...
python -c "import experta; print(f'Experta version: {experta.__version__}')"
if errorlevel 1 (
    echo.
    echo [!] Experta not found! Installing...
    pip install experta>=1.9.0
    echo.
    echo [OK] Experta installed!
) else (
    echo [OK] Experta is installed!
)

echo.
echo Checking all required packages...
pip list | findstr /i "experta fastapi uvicorn"

echo.
echo ========================================
echo   Ready to run start_engine.bat
echo ========================================
pause


