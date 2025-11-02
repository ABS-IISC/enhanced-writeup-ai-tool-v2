@echo off
echo ========================================
echo GitHub Repository Setup
echo Enhanced Writeup Automation AI Tool v2.0
echo ========================================
echo.

echo Step 1: Create GitHub Repository
echo Please follow these steps:
echo 1. Go to https://github.com/new
echo 2. Repository name: enhanced-writeup-ai-tool-v2
echo 3. Description: Enhanced Writeup Automation AI Tool v2.0 - Advanced Split View, AI Analysis, and Production Ready Deployment
echo 4. Set to Public (recommended) or Private
echo 5. DO NOT initialize with README, .gitignore, or license (we already have them)
echo 6. Click "Create repository"
echo.

pause

echo Step 2: Copy the repository URL
set /p REPO_URL="Enter your GitHub repository URL (https://github.com/username/repo-name.git): "

echo.
echo Step 3: Adding remote origin...
git remote add origin %REPO_URL%

echo.
echo Step 4: Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ========================================
echo SUCCESS! Your code is now on GitHub!
echo Repository URL: %REPO_URL%
echo ========================================
echo.
echo Next steps:
echo 1. Your code is now on GitHub
echo 2. You can deploy to Railway, Render, or Heroku
echo 3. Use the deployment guides in the repository
echo.
pause