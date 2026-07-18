from fastapi import APIRouter
from agents.investigator import DataInvestigatorAgent
import traceback
import logging

router = APIRouter()

agent = DataInvestigatorAgent()

logging.basicConfig(level=logging.ERROR)

@router.get("/investigate")
def investigate(question: str):
    try:
        return agent.investigate(question)

    except Exception as e:
        error = traceback.format_exc()

        print("========== INVESTIGATION ERROR ==========")
        print(error)

        logging.exception("Investigation failed")

        return {
            "status": "FAILED",
            "error": str(e),
            "traceback": error,
        }