@echo off
REM CSV Similarity Parser Quick Start Script for Windows

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Running installation...
    call install.bat
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Run the application
echo Starting CSV Similarity Parser...
python csv_similarity_parser.py 