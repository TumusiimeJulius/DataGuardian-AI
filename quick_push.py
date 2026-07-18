import subprocess
import os

os.chdir('C:\\Users\\juliu\\Desktop\\DataGuardian-AI')

print("Adding files...")
subprocess.call('git add -A', shell=True)

print("Committing...")
subprocess.call('git commit -m "Production deploy: JSON serialization and error handling fixes"', shell=True)

print("Pushing...")
result = subprocess.call('git push', shell=True)

if result == 0:
    print("\n✓ Successfully pushed to GitHub!")
    print("Render deployment initiated - check back in 2-5 minutes")
else:
    print("\n✗ Push failed")
