from fastapi import APIRouter
from agents.investigator import DataInvestigatorAgent


router = APIRouter()

agent = DataInvestigatorAgent()


import traceback

@router.get("/investigate")
def investigate(question:str):
    try:
        result = agent.investigate(question)
        return result
    except Exception as e:
        return {
            "status": "FAILED",
            "error": str(e),
            "traceback": traceback.format_exc()
        }