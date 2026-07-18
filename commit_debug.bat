@echo off
cd /d C:\Users\juliu\Desktop\DataGuardian-AI\backend
git add api/routes.py
git commit -m "Add extra debug logs for /investigate (env, python version, sys.path)"
git push
pause
