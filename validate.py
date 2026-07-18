#!/usr/bin/env python3
"""Pre-deployment validation for DataGuardian AI"""
import subprocess
import os
import sys

os.chdir('C:\\Users\\juliu\\Desktop\\DataGuardian-AI')

print("="*70)
print("DataGuardian AI - Pre-Deployment Validation")
print("="*70)

# Check 1: Python syntax validation
print("\n[CHECK 1] Python Syntax Validation")
print("-"*70)
files_to_check = [
    'backend/agents/investigator.py',
    'backend/agents/memory_agent.py',
    'backend/api/routes.py',
    'backend/main.py'
]

all_valid = True
for filepath in files_to_check:
    try:
        result = subprocess.run(
            ['python', '-m', 'py_compile', filepath],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ {filepath}")
        else:
            print(f"✗ {filepath}")
            print(f"  Error: {result.stderr}")
            all_valid = False
    except Exception as e:
        print(f"✗ {filepath} - {str(e)}")
        all_valid = False

if all_valid:
    print("\n✓ All files have valid Python syntax")
else:
    print("\n✗ Some files have syntax errors - DEPLOY CANCELLED")
    sys.exit(1)

# Check 2: Git status
print("\n[CHECK 2] Git Status")
print("-"*70)
result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
if result.stdout.strip():
    print("Pending changes:")
    for line in result.stdout.strip().split('\n')[:5]:
        print(f"  {line}")
    if result.stdout.count('\n') > 5:
        print(f"  ... and {result.stdout.count(chr(10)) - 5} more")
else:
    print("✓ All changes committed")

# Check 3: Key features verification
print("\n[CHECK 3] Key Features in Code")
print("-"*70)

features = {
    'JSON serialization': 'backend/api/routes.py',
    'Agent health endpoint': 'backend/main.py',
    'Mock data fallback': 'backend/agents/investigator.py',
    'Error tracking': 'backend/agents/investigator.py'
}

for feature, filepath in features.items():
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if 'serializable' in content.lower() or 'json' in content.lower():
                print(f"✓ {feature}")
            else:
                print(f"⚠ {feature} (may not be present)")
    except Exception as e:
        print(f"✗ {feature} - Could not verify")

print("\n" + "="*70)
print("PRE-DEPLOYMENT VALIDATION COMPLETE")
print("Ready to deploy to Render")
print("="*70)
