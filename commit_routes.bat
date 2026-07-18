@echo off
cd /d C:\Users\juliu\Desktop\DataGuardian-AI
git add backend/api/routes.py
git commit -m "Add timeout wrapper for /investigate to avoid gateway 502s"
git push
pause
