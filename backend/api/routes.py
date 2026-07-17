from fastapi import APIRouter
from agents.investigator import DataInvestigatorAgent


router = APIRouter()

agent = DataInvestigatorAgent()


@router.get("/investigate")
def investigate(question:str):

    result = agent.investigate(question)

    return result