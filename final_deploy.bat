@echo off
echo DataGuardian AI - Production Deployment
echo ========================================
echo.

cd /d C:\Users\juliu\Desktop\DataGuardian-AI

echo [1] Checking git status...
git status

echo.
echo [2] Staging changes...
git add -A

echo.
echo [3] Committing...
git commit -m "Production: JSON serialization, mock data fallback, and comprehensive error handling"

echo.
echo [4] Pushing to GitHub...
git push

echo.
echo ========================================
echo Deployment complete!
echo Render will auto-deploy within 2-5 minutes
echo ========================================
echo.
echo Test at: https://dataguardianai.onrender.com/investigate?question=test
echo Health at: https://dataguardianai.onrender.com/health
echo.
pause
