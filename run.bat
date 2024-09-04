@echo off
REM Change to the directory where your virtual environment is located
cd .venv\Scripts

REM Activate the virtual environment
call activate

REM Change to the directory where your main.py is located
cd ..\..\

REM Run the main.py script
python main.py