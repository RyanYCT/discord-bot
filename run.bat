@echo off
REM Change to the directory where your virtual environment is located
cd G:\Projects\Discord\GuildBot\.venv\Scripts

REM Activate the virtual environment
call activate

REM Change to the directory where your main.py is located
cd G:\Projects\Discord\GuildBot

REM Run the main.py script
python main.py

REM Deactivate the virtual environment
deactivate