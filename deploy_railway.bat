@echo off
echo ========================================
echo Railway Deployment - One Click Deploy
echo Enhanced Writeup Automation AI Tool v2.0
echo ========================================
echo.

echo Step 1: Installing Railway CLI...
npm install -g @railway/cli
if %errorlevel% neq 0 (
    echo Failed to install Railway CLI
    echo Please install Node.js first: https://nodejs.org/
    pause
    exit /b 1
)

echo.
echo Step 2: Login to Railway...
railway login

echo.
echo Step 3: Initialize Railway project...
railway init

echo.
echo Step 4: Deploy to Railway...
railway up

echo.
echo ========================================
echo Deployment Complete!
echo Your app will be available at the URL shown above
echo ========================================
pause