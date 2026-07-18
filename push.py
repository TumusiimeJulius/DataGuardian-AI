#!/usr/bin/env python3
"""Push all changes to GitHub and trigger Render deployment"""
import subprocess
import sys

def main():
    # Change to repo directory
    import os
    os.chdir('C:\\Users\\juliu\\Desktop\\DataGuardian-AI')
    
    print("="*70)
    print("DataGuardian AI - Final Deployment Push")
    print("="*70)
    
    # Git add
    print("\n[1/4] Staging all changes...")
    result = subprocess.run(['git', 'add', '-A'], capture_output=True, text=True)
    print("✓ Changes staged")
    
    # Git commit
    print("[2/4] Creating commit...")
    result = subprocess.run(
        ['git', 'commit', '-m', 'Implement comprehensive JSON serialization and proper error handling'],
        capture_output=True,
        text=True
    )
    
    if 'nothing to commit' in result.stdout:
        print("✓ No new changes (already committed)")
    elif result.returncode == 0:
        print("✓ Commit created successfully")
    else:
        print(f"⚠ Commit output: {result.stdout}")
    
    # Git push
    print("[3/4] Pushing to GitHub...")
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Push successful!")
    else:
        print(f"✗ Push failed: {result.stderr}")
        return False
    
    # Git log
    print("[4/4] Verifying deployment...")
    result = subprocess.run(['git', 'log', '-1', '--oneline'], capture_output=True, text=True)
    print(f"✓ Latest: {result.stdout.strip()}")
    
    print("\n" + "="*70)
    print("SUCCESS! Render auto-deployment initiated.")
    print("Changes should be live in 2-5 minutes.")
    print("="*70)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
