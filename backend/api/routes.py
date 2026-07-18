from fastapi import APIRouter
import traceback
import logging
import sys

router = APIRouter()

logging.basicConfig(level=logging.ERROR)

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