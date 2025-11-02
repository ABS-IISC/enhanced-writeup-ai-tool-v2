@echo off
echo ========================================
echo Push to GitHub - Enhanced Writeup AI Tool v2.0
echo ========================================
echo.

echo STEP 1: Create GitHub Repository First!
echo 1. Go to: https://github.com/new
echo 2. Repository name: enhanced-writeup-ai-tool-v2
echo 3. Description: Enhanced Writeup Automation AI Tool v2.0
echo 4. Set to Public
echo 5. DO NOT initialize with README/gitignore
echo 6. Click Create repository
echo.

set /p CONTINUE="Have you created the GitHub repository? (y/n): "
if /i "%CONTINUE%" neq "y" (
    echo Please create the repository first, then run this script again.
    pause
    exit /b 1
)

echo.
set /p REPO_URL="Enter your GitHub repository URL (https://github.com/username/repo-name.git): "

echo.
echo Adding remote origin...
git remote add origin %REPO_URL%

echo.
echo Pushing to GitHub...
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! Code pushed to GitHub!
    echo ========================================
    echo Repository: %REPO_URL%
    echo.
    echo Next steps:
    echo 1. Visit your GitHub repository
    echo 2. Deploy to Railway/Render/Heroku
    echo 3. Share your live tool!
    echo.
) else (
    echo.
    echo ========================================
    echo Push failed! Troubleshooting:
    echo ========================================
    echo 1. Check repository URL is correct
    echo 2. Ensure you have push permissions
    echo 3. Try: git remote set-url origin YOUR_REPO_URL
    echo 4. Then: git push -u origin main
    echo.
)

pause