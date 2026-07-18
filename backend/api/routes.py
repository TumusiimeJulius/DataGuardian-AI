from fastapi import APIRouter
import traceback
import logging

router = APIRouter()

logging.basicConfig(level=logging.ERROR)

@router.get("/investigate")
def investigate(question: str):
    # Temporary mock response to test if route is working
    # TODO: Debug why agent initialization fails in production
    return {
        "status": "PENDING",
        "question": question,
        "message": "Investigation queue received. Processing...",
        "agents_involved": [
            "Data Investigator",
            "Quality Analyzer",
            "Anomaly Detector",
            "Root Cause Analyzer",
            "Repair Engine",
            "Recommender"
        ]
    }
    
    # Original implementation below - currently causing 502 in production
    # try:
    #     from agents.investigator import DataInvestigatorAgent
    #     agent = DataInvestigatorAgent()
    #     return agent.investigate(question)
    # except Exception as e:
    #     error = traceback.format_exc()
    #     print("========== INVESTIGATION ERROR ==========")
    #     print(error)
    #     logging.exception("Investigation failed")
    #     return {
    #         "status": "FAILED",
    #         "error": str(e),
    #         "type": type(e).__name__,
    #         "traceback": error,
    #     }