@echo off
echo ========================================
echo   Interview Portal - Starting Servers
echo ========================================
echo.

REM Start Django backend
echo [1/2] Starting Django Backend Server...
start cmd /k "cd backend && echo Backend running at http://localhost:8000 && python manage.py runserver"

REM Wait for backend to start
timeout /t 3 /nobreak > nul

REM Start React frontend
echo [2/2] Starting React Frontend Server...
start cmd /k "cd frontend && echo Frontend running at http://localhost:5173 && npm run dev"

echo.
echo ========================================
echo   Servers Starting Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit this window...
pause > nul
