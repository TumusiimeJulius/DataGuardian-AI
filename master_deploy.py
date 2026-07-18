#!/usr/bin/env python3
"""Master deployment orchestrator for DataGuardian AI"""
import subprocess
import os
import sys
import json
from datetime import datetime

def run_step(step_num, description, command):
    """Execute a deployment step"""
    print(f"\n[STEP {step_num}] {description}")
    print("-" * 70)
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✓ Success")
            if result.stdout and len(result.stdout) < 200:
                print(f"  {result.stdout.strip()}")
            return True
        else:
            print(f"✗ Failed")
            if result.stderr:
                print(f"  Error: {result.stderr[:500]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ Timeout")
        return False
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False

def main():
    os.chdir('C:\\Users\\juliu\\Desktop\\DataGuardian-AI')
    
    print("\n" + "=" * 70)
    print("DataGuardian AI - MASTER DEPLOYMENT ORCHESTRATOR")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    steps_completed = []
    
    # Step 1: Validate Python files
    if run_step(1, "Validate Python syntax", ['python', '-m', 'py_compile', 'backend/agents/investigator.py']):
        steps_completed.append("Syntax validation")
    else:
        print("\n✗ Syntax validation failed - aborting deployment")
        return False
    
    # Step 2: Check git status
    print(f"\n[STEP 2] Check Git Status")
    print("-" * 70)
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    modified_files = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    print(f"✓ Modified files: {modified_files}")
    
    # Step 3: Stage changes
    if run_step(3, "Stage all changes", ['git', 'add', '-A']):
        steps_completed.append("Git add")
    else:
        print("Warning: Git add may have failed")
    
    # Step 4: Commit changes
    if run_step(4, "Create commit", ['git', 'commit', '-m', 'Production deployment: JSON serialization and comprehensive error handling']):
        steps_completed.append("Git commit")
    else:
        print("Note: Nothing new to commit")
    
    # Step 5: Push to GitHub
    if run_step(5, "Push to GitHub", ['git', 'push']):
        steps_completed.append("Git push")
    else:
        print("\n✗ Push to GitHub failed - deployment aborted")
        return False
    
    # Step 6: Verify latest commit
    print(f"\n[STEP 6] Verify Latest Commit")
    print("-" * 70)
    result = subprocess.run(['git', 'log', '-1', '--pretty=format:%h %s'], capture_output=True, text=True)
    print(f"✓ {result.stdout}")
    
    print("\n" + "=" * 70)
    print("✓ DEPLOYMENT SUCCESSFUL!")
    print("=" * 70)
    print("\nCompleted steps:")
    for step in steps_completed:
        print(f"  ✓ {step}")
    
    print("\nRender will auto-deploy within 2-5 minutes.")
    print("Monitor at: https://dataguardianai.onrender.com/health")
    print("\nNext actions:")
    print("  1. Wait 2-5 minutes for Render deployment")
    print("  2. Test /investigate endpoint")
    print("  3. Test other endpoints if investigation works")
    
    print("=" * 70)
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
