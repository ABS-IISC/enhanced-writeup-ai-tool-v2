@echo off
echo ========================================
echo Universal Deployment Script
echo ========================================
echo.

echo [1/5] Copying universal files...
copy requirements_universal.txt requirements.txt
copy Procfile_universal Procfile
copy universal_app.py app.py

echo [2/5] Installing dependencies...
pip install -r requirements.txt

echo [3/5] Testing locally...
echo Starting local test server...
echo Open http://localhost:5005 in your browser
echo Press Ctrl+C to stop and continue with deployment
python universal_app.py

echo.
echo [4/5] Ready for deployment!
echo.
echo Choose your deployment platform:
echo 1. Railway (Recommended)
echo 2. Ngrok (Quick sharing)
echo 3. Manual deployment
echo.

set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Railway Deployment Instructions:
    echo 1. Go to https://railway.app
    echo 2. Sign up/Login with GitHub
    echo 3. Click "New Project" > "Deploy from GitHub repo"
    echo 4. Select this repository
    echo 5. Railway will auto-deploy using railway.toml
    echo.
    echo Your app will be available at: https://your-app-name.railway.app
    pause
) else if "%choice%"=="2" (
    echo.
    echo Installing ngrok...
    if not exist ngrok.exe (
        echo Downloading ngrok...
        curl -o ngrok.zip https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip
        tar -xf ngrok.zip
        del ngrok.zip
    )
    echo.
    echo Starting ngrok tunnel...
    start /B python universal_app.py
    timeout /t 3
    ngrok http 5005
) else (
    echo.
    echo Manual Deployment:
    echo 1. Upload all files to your server
    echo 2. Install Python and pip
    echo 3. Run: pip install -r requirements.txt
    echo 4. Run: python universal_app.py
    echo.
    pause
)

echo.
echo [5/5] Deployment complete!
pause