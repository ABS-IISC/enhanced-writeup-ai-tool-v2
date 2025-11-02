@echo off
echo ========================================
echo Docker + Ngrok Live Deployment
echo Enhanced Writeup AI Tool
echo ========================================
echo.

echo Step 1: Building Docker image...
docker build -f Dockerfile.simple -t writeup-ai-simple .
if %errorlevel% neq 0 (
    echo Docker build failed! Make sure Docker is running.
    pause
    exit /b 1
)

echo.
echo Step 2: Starting Docker container...
docker stop writeup-ai-simple 2>nul
docker rm writeup-ai-simple 2>nul
docker run -d --name writeup-ai-simple -p 5005:5005 writeup-ai-simple

echo.
echo Step 3: Checking if container is running...
docker ps | findstr writeup-ai-simple
if %errorlevel% neq 0 (
    echo Container failed to start!
    docker logs writeup-ai-simple
    pause
    exit /b 1
)

echo.
echo Step 4: Starting ngrok tunnel...
echo Your app is running on http://localhost:5005
echo Starting ngrok to make it live...
echo.
echo ========================================
echo LIVE URL will appear below:
echo ========================================
ngrok http 5005