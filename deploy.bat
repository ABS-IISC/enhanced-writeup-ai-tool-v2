@echo off
echo ========================================
echo  ENHANCED WRITEUP AI TOOL - DEPLOY
echo ========================================
echo.

REM Stop existing container
docker stop writeup-ai-tool-v9 2>nul
docker rm writeup-ai-tool-v9 2>nul

echo Building Docker image...
docker build -t writeup-ai-tool-v9:latest .

if errorlevel 1 (
    echo ERROR: Docker build failed
    pause
    exit /b 1
)

echo Starting container...
docker run -d --name writeup-ai-tool-v9 -p 5005:5005 -p 4040:4040 -v "%cd%/uploads:/app/uploads" writeup-ai-tool-v9:latest

if errorlevel 1 (
    echo ERROR: Container start failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo  DEPLOYMENT SUCCESSFUL!
echo ========================================
echo.
echo Local Access: http://localhost:5005
echo.
echo Container: writeup-ai-tool-v9
echo Status: Running
echo.
echo Management Commands:
echo   docker logs -f writeup-ai-tool-v9
echo   docker stop writeup-ai-tool-v9
echo   docker restart writeup-ai-tool-v9
echo.

REM Open browser
start http://localhost:5005

pause