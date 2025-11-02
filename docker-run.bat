@echo off
echo Building Docker image...
docker build -f Dockerfile.simple -t writeup-ai-simple .

echo Stopping existing container...
docker stop writeup-ai-simple 2>nul
docker rm writeup-ai-simple 2>nul

echo Starting container...
docker run -d --name writeup-ai-simple -p 5005:5005 writeup-ai-simple

echo Container started! App running on http://localhost:5005
echo.
echo To make it live with ngrok, run:
echo ngrok http 5005
pause