@echo off
echo Starting AI Interview Preparation Portal...
echo.
echo Starting Django Backend Server...
cd backend
start cmd /k "python manage.py runserver"
timeout /t 3 /nobreak >nul
echo.
echo Starting React Frontend Server...
cd ..\frontend
start cmd /k "npm run dev"
echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit this window...
pause >nul
