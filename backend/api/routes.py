from fastapi import APIRouter
import traceback
import logging
import sys
import json
import threading
import os
from datetime import datetime

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
        # Emit lightweight environment debug info to stderr for Render logs
        print(f"[INVESTIGATE] timestamp={datetime.utcnow().isoformat()}Z", file=sys.stderr)
        print(f"[INVESTIGATE] python_version={sys.version.splitlines()[0]}", file=sys.stderr)
        # Log a short snapshot of relevant env vars
        env_keys = [k for k in os.environ.keys() if k.upper().startswith(('RENDER','GITHUB','RAILS','VCAP'))]
        for k in env_keys[:20]:
            try:
                print(f"[INVESTIGATE] ENV {k}={os.environ.get(k)}", file=sys.stderr)
            except Exception:
                pass
        print(f"[INVESTIGATE] sys.path_len={len(sys.path)}", file=sys.stderr)
        # Import here to catch initialization errors
        from agents.investigator import DataInvestigatorAgent
        
        # Log import success
        print(f"[INVESTIGATE] Agent import successful", file=sys.stderr)
        
        # Create agent instance
        agent = DataInvestigatorAgent()
        print(f"[INVESTIGATE] Agent instance created", file=sys.stderr)
        
        # Run investigation with timeout to avoid gateway timeouts
        result_container = {}

        def _run():
            try:
                result_container['value'] = agent.investigate(question)
            except Exception as ex:
                result_container['error'] = ex

        thread = threading.Thread(target=_run)
        thread.start()
        thread.join(timeout=12)

        if thread.is_alive():
            print(f"[INVESTIGATE] Investigation timed out after 12s", file=sys.stderr)
            return {
                "status": "TIMED_OUT",
                "message": "Investigation did not complete within timeout",
            }

        if 'error' in result_container:
            raise result_container['error']

        result = result_container.get('value')
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