from fastapi import APIRouter

router = APIRouter()

@router.get("/investigate")
def investigate(question: str):
    return {"status": "ok", "question": question}