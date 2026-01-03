@echo off
REM Python Script Scheduler - Windows Batch File
REM This batch file runs the scheduler on Windows

echo ============================================
echo Python Script Scheduler for Windows 11
echo ============================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if schedule library is installed
python -c "import schedule" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Run the scheduler
echo Starting scheduler...
echo Press Ctrl+C to stop
echo.
python scheduler.py

pause
