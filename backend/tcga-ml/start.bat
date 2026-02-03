@echo off
echo Starting TCGA Uterine Cancer ML API...
echo ===================================================
echo.

cd /d "%~dp0"

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate

REM Install requirements
echo Installing/Checking dependencies...
pip install -r requirements.txt

REM Run Application
echo.
echo Starting Flask Server on port 5000...
echo API documentation will be available at http://localhost:5000/
echo.
python api/app.py

pause
