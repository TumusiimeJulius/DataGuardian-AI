#!/usr/bin/env python3
"""Comprehensive DataGuardian AI Deployment Script"""
import subprocess
import os
import sys

def run_command(cmd, description):
    """Run a shell command and report results"""
    print(f"\n{'='*70}")
    print(f"{description}")
    print('='*70)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        if result.stdout:
            print(result.stdout)
        if result.stderr and "warning" not in result.stderr.lower():
            print(f"STDERR: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

os.chdir('c:/Users/juliu/Desktop/DataGuardian-AI')

# Step 1: Check status
print("\n" + "="*70)
print("DataGuardian AI - Production Deployment")
print("="*70)

result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
if result.stdout.strip():
    print(f"\nPending changes:\n{result.stdout}")
else:
    print("\nNo changes pending - checking if latest commit deployed...")
    result = subprocess.run(['git', 'log', '-1', '--oneline'], capture_output=True, text=True)
    print(f"Latest commit: {result.stdout}")

# Step 2: Add all changes
print("\nStaging all changes...")
subprocess.run(['git', 'add', '-A'], capture_output=True)

# Step 3: Commit with description
commit_msg = "Implement comprehensive JSON serialization and error handling for investigate endpoint"
print(f"Committing: {commit_msg}")
result = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True)
if "nothing to commit" in result.stdout:
    print("✓ No new changes to commit")
elif result.returncode == 0:
    print("✓ Commit successful")
    print(result.stdout)
else:
    print(f"✗ Commit failed: {result.stdout}")

# Step 4: Push to GitHub
print("\nPushing to GitHub (triggering Render auto-deploy)...")
result = subprocess.run(['git', 'push'], capture_output=True, text=True)
if result.returncode == 0:
    print("✓ Push successful!")
    print("Render deployment initiated - changes should be live in 2-5 minutes")
else:
    print(f"✗ Push failed: {result.stdout}")
    
print("\n" + "="*70)
print("Deployment process complete!")
print("="*70)
