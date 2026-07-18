from fastapi import APIRouter
import traceback
import logging
import sys
import json

router = APIRouter()

logging.basicConfig(level=logging.ERROR)

def make_json_serializable(obj):
    """Convert non-JSON-serializable objects to strings"""
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_json_serializable(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return str(obj)
    else:
        return obj

@router.get("/investigate")
def investigate(question: str):
    try:
        # Import here to catch initialization errors
        from agents.investigator import DataInvestigatorAgent
        
        # Log import success
        print(f"[INVESTIGATE] Agent import successful", file=sys.stderr)
        
        # Create agent instance
        agent = DataInvestigatorAgent()
        print(f"[INVESTIGATE] Agent instance created", file=sys.stderr)
        
        # Run investigation
        result = agent.investigate(question)
        print(f"[INVESTIGATE] Investigation completed successfully", file=sys.stderr)
        
        # Ensure result is JSON serializable
        result = make_json_serializable(result)
        return result

    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        error_trace = traceback.format_exc()
        
        print(f"[INVESTIGATE ERROR] Type: {error_type}", file=sys.stderr)
        print(f"[INVESTIGATE ERROR] Message: {error_msg}", file=sys.stderr)
        print(f"[INVESTIGATE ERROR] Trace: {error_trace}", file=sys.stderr)
        
        logging.exception("Investigation failed")

        return {
            "status": "FAILED",
            "error": error_msg,
            "error_type": error_type,
            "traceback": error_trace[:1000],  # Limit size
        }