@echo off
cd /d C:\Users\juliu\Desktop\DataGuardian-AI
git add backend/agents/investigator.py
git commit -m "Make agent imports lazy to avoid import-time crashes in production"
git push
pause
