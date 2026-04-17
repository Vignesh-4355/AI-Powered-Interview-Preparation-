@echo off
echo ====================================
echo AI Interview Portal - Initial Setup
echo ====================================
echo.

echo [1/4] Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

echo Running database migrations...
python manage.py migrate

echo.
echo [2/4] Creating superuser for admin access...
python manage.py createsuperuser

echo.
echo [3/4] Setting up Frontend...
cd ..\frontend

echo Installing Node dependencies...
call npm install

echo.
echo [4/4] Setup Complete!
echo.
echo ====================================
echo Next Steps:
echo 1. Run 'start-servers.bat' to start both servers
echo 2. Access frontend at http://localhost:5173
echo 3. Access admin panel at http://localhost:8000/admin
echo ====================================
echo.
pause
