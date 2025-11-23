@echo off
echo ========================================
echo   Find Python and Add to PATH
echo ========================================
echo.

echo Searching for Python installation...
echo.

REM Common Python installation paths
set PYTHON_PATHS[0]=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312
set PYTHON_PATHS[1]=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312-64
set PYTHON_PATHS[2]=C:\Python312
set PYTHON_PATHS[3]=C:\Program Files\Python312
set PYTHON_PATHS[4]=C:\Program Files (x86)\Python312

set FOUND_PATH=

REM Check each path
for /L %%i in (0,1,4) do (
    call set CURRENT_PATH=%%PYTHON_PATHS[%%i]%%
    if exist "!CURRENT_PATH!\python.exe" (
        set FOUND_PATH=!CURRENT_PATH!
        echo [FOUND] Python found at: !CURRENT_PATH!
        goto :found
    )
)

REM Try to find via registry
echo Checking registry...
for /f "tokens=2*" %%a in ('reg query "HKLM\SOFTWARE\Python\PythonCore\3.12\InstallPath" /ve 2^>nul') do (
    if "%%b" neq "" (
        set FOUND_PATH=%%b
        echo [FOUND] Python found at: %%b
        goto :found
    )
)

echo [ERROR] Python not found automatically.
echo.
echo Please find Python manually:
echo 1. Open Start Menu
echo 2. Right-click "Python 3.12 (64-bit)"
echo 3. Select "Open file location"
echo 4. Note the folder path
echo.
echo Then add these paths to PATH manually:
echo   - Python folder (e.g., C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312)
echo   - Scripts folder (e.g., C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\Scripts)
echo.
pause
exit /b 1

:found
echo.
echo Python installation found!
echo Path: %FOUND_PATH%
echo.
echo To add to PATH manually:
echo 1. Press Windows + R
echo 2. Type: sysdm.cpl
echo 3. Go to Advanced tab
echo 4. Click Environment Variables
echo 5. Edit Path variable
echo 6. Add these two paths:
echo    %FOUND_PATH%
echo    %FOUND_PATH%\Scripts
echo.
echo Or reinstall Python with "Add Python to PATH" checked.
echo.
pause


