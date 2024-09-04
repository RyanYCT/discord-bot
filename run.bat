@echo off
REM Check if the virtual environment directory exists
if not exist ".venv\Scripts" (
    echo Virtual environment not found. Creating a new one...
    python -m venv .venv
)

REM Change to the directory where your virtual environment is located
cd .venv\Scripts

REM Activate the virtual environment
call activate

REM Change to the root directory of your project
cd ..\..\

REM Check if requirements.txt exists
if exist "requirements.txt" (
    echo Installing requirements from requirements.txt...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found.
)

REM Check if main.py exists
if exist "main.py" (
    echo Running main.py...
    python main.py
) else (
    echo main.py not found.
)
