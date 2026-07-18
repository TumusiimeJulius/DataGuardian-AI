from fastapi import APIRouter
import traceback
import logging
import os

router = APIRouter()

logging.basicConfig(level=logging.ERROR)

@router.get("/investigate")
def investigate(question: str):
    try:
        # Check if we're in debug/test mode
        if os.getenv("DEBUG_MODE") == "true":
            return {
                "status": "debug_mode",
                "question": question,
                "message": "Debug mode active - returning mock response"
            }
        
        from agents.investigator import DataInvestigatorAgent
        agent = DataInvestigatorAgent()
        return agent.investigate(question)

    except Exception as e:
        error = traceback.format_exc()

        print("========== INVESTIGATION ERROR ==========")
        print(error)

        logging.exception("Investigation failed")

        return {
            "status": "FAILED",
            "error": str(e),
            "type": type(e).__name__,
            "traceback": error,
        }