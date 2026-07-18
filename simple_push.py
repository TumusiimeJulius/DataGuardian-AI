#!/usr/bin/env python3
"""
Simple script to check what needs to be pushed and then push it
Run this from the DataGuardian-AI directory
"""
import subprocess
import os
import sys

def main():
    os.chdir('C:\\Users\\juliu\\Desktop\\DataGuardian-AI')
    
    print("DataGuardian AI - Ready for Production Deployment")
    print("=" * 70)
    
    # Check what's changed
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, shell=False)
    
    if result.returncode != 0:
        print("ERROR: Could not access git")
        return False
    
    changes = result.stdout.strip()
    if not changes:
        print("✓ All changes already committed!")
        result = subprocess.run(['git', 'log', '-1', '--oneline'], capture_output=True, text=True, shell=False)
        print(f"Latest: {result.stdout}")
        return True
    
    print("\nModified files:")
    for line in changes.split('\n'):
        print(f"  {line}")
    
    print("\n" + "=" * 70)
    print("READY TO DEPLOY")
    print("=" * 70)
    
    # Push
    print("\nExecuting git operations...")
    
    print("1. Adding files...")
    subprocess.run(['git', 'add', '-A'], shell=False, capture_output=True)
    
    print("2. Committing...")
    result = subprocess.run(
        ['git', 'commit', '-m', 'Production deploy: Comprehensive error handling and JSON serialization'],
        shell=False,
        capture_output=True,
        text=True
    )
    print(f"   {result.stdout.strip() if result.stdout else 'No new commits'}")
    
    print("3. Pushing...")
    result = subprocess.run(['git', 'push'], shell=False, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("   ✓ Push successful!")
        result = subprocess.run(['git', 'log', '-1', '--oneline'], capture_output=True, text=True, shell=False)
        print(f"\nDeployed: {result.stdout}")
        return True
    else:
        print(f"   ✗ Push failed: {result.stderr}")
        return False

if __name__ == '__main__':
    try:
        success = main()
        if success:
            print("\n" + "=" * 70)
            print("✓ DEPLOYMENT COMPLETE")
            print("Render will auto-deploy within 2-5 minutes")
            print("=" * 70)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
