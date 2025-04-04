@echo off
REM MibiTech Local Development Setup Script for Windows
REM This script helps set up the local development environment

echo MibiTech Local Development Setup

REM Check if Python is installed
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.9 or later from https://www.python.org/downloads/
    exit /b 1
)

REM Check if Node.js is installed
node --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Node.js is not installed or not in PATH.
    echo Please install Node.js 18 or later from https://nodejs.org/
    exit /b 1
)

REM Check if Git is installed
git --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Git is not installed or not in PATH.
    echo Please install Git from https://git-scm.com/downloads
    exit /b 1
)

echo All required tools are installed.

REM Setup Backend
echo Setting up backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

REM Apply migrations
echo Applying database migrations...
python manage.py migrate

REM Create superuser if needed
echo Do you want to create a superuser? (y/n)
set /p create_superuser=
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

REM Deactivate virtual environment
call venv\Scripts\deactivate

REM Return to root directory
cd ..

REM Setup Frontend
echo Setting up frontend...
cd frontend

REM Install Node.js dependencies
echo Installing Node.js dependencies...
npm install

REM Return to root directory
cd ..

echo Setup complete!
echo.
echo To start the backend server:
echo   cd backend
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo To start the frontend server:
echo   cd frontend
echo   node server.js
echo.
echo Or use Docker Compose:
echo   deploy.bat --build --up
echo.
echo For more information, see LOCAL_DEVELOPMENT.md

pause