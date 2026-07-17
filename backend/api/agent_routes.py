from fastapi import APIRouter

from services.agent_activity_service import get_agents


router = APIRouter(
    prefix="/dashboard",
    tags=["AI Agents"]
)



@router.get("/agents")
def agents():

    return {

        "agents":
        get_agents()

    }