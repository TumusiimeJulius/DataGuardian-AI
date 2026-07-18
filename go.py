import os
os.chdir(r'C:\Users\juliu\Desktop\DataGuardian-AI')
os.system('git add -A && git commit -m "Production: JSON serialization, error handling, mock data fallback" && git push')
print("\nDeploy complete! Render will update within 2-5 minutes.")
