@echo off
cd /d C:\Users\juliu\Desktop\DataGuardian-AI
echo Running comprehensive system tests...
python system_test.py
echo.
echo.
echo Tests complete. Committing changes...
git add backend/api/routes.py backend/agents/investigator.py backend/agents/memory_agent.py backend/main.py
git commit -m "Add JSON serialization and complete error handling for all endpoints"
git push
echo.
echo Deployment complete!
pause
