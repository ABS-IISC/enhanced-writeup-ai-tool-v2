@echo off
echo ========================================
echo Docker Deployment - One Click Deploy
echo Enhanced Writeup Automation AI Tool v2.0
echo ========================================
echo.

echo Step 1: Building Docker image...
docker build -t writeup-ai-tool-v2 .
if %errorlevel% neq 0 (
    echo Failed to build Docker image
    echo Please install Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo.
echo Step 2: Stopping existing container (if any)...
docker stop writeup-ai-tool-v2 2>nul
docker rm writeup-ai-tool-v2 2>nul

echo.
echo Step 3: Starting new container...
docker run -d --name writeup-ai-tool-v2 -p 5005:5005 writeup-ai-tool-v2

echo.
echo Step 4: Checking container status...
docker ps | findstr writeup-ai-tool-v2

echo.
echo ========================================
echo Deployment Complete!
echo Access your app at: http://localhost:5005
echo ========================================
echo.
echo Container logs:
docker logs writeup-ai-tool-v2
pause