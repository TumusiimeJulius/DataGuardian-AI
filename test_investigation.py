import sys
sys.path.insert(0, 'c:/Users/juliu/Desktop/DataGuardian-AI/backend')

from agents.investigator import DataInvestigatorAgent

print("Creating agent...")
agent = DataInvestigatorAgent()
print(f"Initialization errors: {agent.initialization_errors}")

print("\nRunning investigation...")
result = agent.investigate('test')

print(f"\nStatus: {result.get('status')}")
print(f"Question: {result.get('question')}")
print(f"Result keys: {list(result.keys())[:8]}")

if result.get('status') == 'COMPLETED':
    print("\n✓ Investigation completed successfully!")
else:
    print(f"\n✗ Investigation failed: {result.get('error')}")
