@echo off
echo Setting up virtual environment and running simple database test...

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install only required packages for the test
echo Installing required packages...
pip install psycopg2 python-dotenv

REM Run the simple database connection test
echo Running simple database connection test...
python simple_db_test.py

REM Deactivate virtual environment
echo Deactivating virtual environment...
deactivate

echo Done!
pause