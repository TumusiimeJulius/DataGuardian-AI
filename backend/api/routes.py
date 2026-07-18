from fastapi import APIRouter
import traceback
import logging

router = APIRouter()

logging.basicConfig(level=logging.ERROR)

@router.get("/investigate")
def investigate(question: str):
    try:
        return {
            "status": "PENDING",
            "question": question,
            "message": "Investigation endpoint active"
        }
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