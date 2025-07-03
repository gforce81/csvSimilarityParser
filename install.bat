@echo off
REM CSV Similarity Parser Installation Script for Windows

echo === CSV Similarity Parser Installation ===
echo.

REM Check if Python 3 is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✓ Python %python_version% detected

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo ✓ pip detected

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo === Installation Complete ===
echo.
echo To run the CSV Similarity Parser:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the application: python csv_similarity_parser.py
echo.
echo Or use the quick start script: run.bat
echo.

echo Installation completed successfully!
pause 