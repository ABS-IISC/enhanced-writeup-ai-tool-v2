@echo off
echo Installing ngrok...
echo.
echo Option 1: Download from https://ngrok.com/download
echo Option 2: Install via Chocolatey: choco install ngrok
echo Option 3: Install via Scoop: scoop install ngrok
echo.
echo After installation, run: ngrok http 5005
echo.
echo Your Docker app is running on http://localhost:5005
echo Container status:
docker ps | findstr writeup-ai-simple
pause