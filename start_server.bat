@echo off
echo Starting OctoFit Tracker Django Server...
echo.

cd /d "%~dp0"
cd octofit-tracker\backend

call venv\Scripts\activate.bat

echo Django server starting on http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

pause
