@echo off
echo ========================================
echo Enhanced Writeup Automation AI Tool v2.0
echo Web Deployment Script
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Creating upload directory...
if not exist "uploads" mkdir uploads

echo.
echo Starting web server...
echo Access the application at: http://localhost:5005
echo Press Ctrl+C to stop the server
echo.

python web_deploy.py

pause