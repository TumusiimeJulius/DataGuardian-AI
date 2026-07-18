@echo off
cd /d C:\Users\juliu\Desktop\DataGuardian-AI
git add backend/agents/investigator.py
git commit -m "Add mock data fallback when test_sales.csv is missing"
git push
pause
