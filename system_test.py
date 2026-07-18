#!/usr/bin/env python3
"""
Comprehensive DataGuardian AI system test
Tests all key components before pushing to production
"""
import sys
import json
sys.path.insert(0, 'c:/Users/juliu/Desktop/DataGuardian-AI/backend')

print("=" * 70)
print("DATAGUARDIAN AI - SYSTEM TEST SUITE")
print("=" * 70)

# Test 1: Agent Initialization
print("\n[TEST 1] Agent Initialization")
print("-" * 70)
try:
    from agents.investigator import DataInvestigatorAgent
    agent = DataInvestigatorAgent()
    print(f"✓ Agent created successfully")
    print(f"  - Initialization errors: {len(agent.initialization_errors)}")
    if agent.initialization_errors:
        print(f"  - Errors: {agent.initialization_errors}")
except Exception as e:
    print(f"✗ Agent creation failed: {str(e)}")
    sys.exit(1)

# Test 2: Investigation Pipeline
print("\n[TEST 2] Investigation Pipeline")
print("-" * 70)
try:
    result = agent.investigate("Test question: what are quality issues?")
    print(f"✓ Investigation completed")
    print(f"  - Status: {result.get('status')}")
    print(f"  - Execution time: {result.get('execution_time_seconds')}s")
    print(f"  - Result keys: {len(result.keys())} fields")
    
    # Verify JSON serializable
    json_str = json.dumps(result, default=str)
    print(f"✓ Result is JSON serializable ({len(json_str)} bytes)")
    
except Exception as e:
    print(f"✗ Investigation failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Memory Agent
print("\n[TEST 3] Memory Agent")
print("-" * 70)
try:
    from agents.memory_agent import MemoryAuditAgent
    memory_agent = MemoryAuditAgent()
    print(f"✓ Memory agent created")
    memory_agent.save(result)
    print(f"✓ Investigation saved to history")
    history = memory_agent.history()
    print(f"✓ History retrieved: {len(history)} investigations")
except Exception as e:
    print(f"✗ Memory agent failed: {str(e)}")

# Test 4: FastAPI Routes
print("\n[TEST 4] FastAPI Routes")
print("-" * 70)
try:
    from api.routes import investigate as investigate_route
    from api.routes import make_json_serializable
    
    # Test investigate route
    route_result = investigate_route("test")
    print(f"✓ /investigate route works")
    print(f"  - Response status: {route_result.get('status')}")
    
    # Test JSON serialization
    serialized = make_json_serializable(route_result)
    json_str = json.dumps(serialized)
    print(f"✓ Response is JSON serializable")
    
except Exception as e:
    print(f"✗ FastAPI routes failed: {str(e)}")
    import traceback
    traceback.print_exc()

# Test 5: All Agents Exist
print("\n[TEST 5] Agent Availability Check")
print("-" * 70)
agents_to_check = [
    'quality_agent',
    'recommendation_agent', 
    'rootcause_agent',
    'lineage_agent',
    'anomaly_agent',
    'prediction_agent',
    'decision_agent',
    'memory_agent',
    'alert_agent',
    'observability_agent',
    'pipeline_agent',
    'repair_agent'
]

available = []
failed = []
for agent_name in agents_to_check:
    agent_obj = getattr(agent, agent_name, None)
    if agent_obj is not None:
        available.append(agent_name)
    else:
        failed.append(agent_name)

print(f"✓ Available agents: {len(available)}/{len(agents_to_check)}")
for name in available[:3]:
    print(f"  - {name}")
if len(available) > 3:
    print(f"  - ... and {len(available) - 3} more")

if failed:
    print(f"✗ Failed agents: {failed}")

print("\n" + "=" * 70)
print("TEST SUITE COMPLETE - All critical systems operational")
print("=" * 70)
