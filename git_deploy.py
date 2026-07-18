#!/usr/bin/env python3
"""Git operations for DataGuardian AI deployment"""
import subprocess
import os

os.chdir('c:/Users/juliu/Desktop/DataGuardian-AI')

print("Checking git status...")
result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
print(result.stdout)

if result.stdout.strip():
    print("\nStaging changes...")
    subprocess.run(['git', 'add', '-A'], capture_output=True)
    
    print("Committing...")
    result = subprocess.run(
        ['git', 'commit', '-m', 'Fix JSON serialization and complete error handling'],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    
    print("Pushing to GitHub...")
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    print(result.stdout)
    print("✓ Deployment initiated!")
else:
    print("No changes to commit")
