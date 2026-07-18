@echo off
cd /d C:\Users\juliu\Desktop\DataGuardian-AI
git add backend/api/routes.py backend/agents/investigator.py backend/agents/memory_agent.py backend/main.py
git commit -m "Add comprehensive agent error tracking and graceful initialization"
git push
pause
