@echo off
echo Setting up virtual environment and running database test...

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Run the database connection test
echo Running database connection test...
python test_db_connection.py

REM Deactivate virtual environment
echo Deactivating virtual environment...
deactivate

echo Done!
pause