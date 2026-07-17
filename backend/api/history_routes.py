from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import DatasetHistory


router = APIRouter(
    prefix="",
    tags=["History"]
)



# =====================================
# Get All Dataset History
# =====================================

@router.get("/history")
def get_history():

    db = SessionLocal()

    try:

        records = db.query(
            DatasetHistory
        ).order_by(
            DatasetHistory.id.desc()
        ).all()


        history = []


        for item in records:

            history.append({

                "id":
                item.id,


                "filename":
                item.filename,


                "clean_file":
                item.clean_file,


                "quality_score":
                item.quality_score,


                "missing_values":
                item.missing_values,


                "duplicates":
                item.duplicates,


                "anomalies":
                item.anomalies,


                "status":
                item.status,


                "execution_time":
                item.execution_time,


                "uploaded_at":
                item.uploaded_at

            })


        return {

            "status":
            "success",


            "count":
            len(history),


            "history":
            history

        }


    finally:

        db.close()





# =====================================
# Get Single Dataset History
# =====================================

@router.get("/history/{dataset_id}")
def get_single_history(dataset_id:int):


    db = SessionLocal()


    try:


        record = db.query(
            DatasetHistory
        ).filter(
            DatasetHistory.id == dataset_id
        ).first()



        if not record:


            raise HTTPException(

                status_code=404,

                detail="Dataset history not found"

            )



        return {


            "id":
            record.id,


            "filename":
            record.filename,


            "clean_file":
            record.clean_file,


            "quality_score":
            record.quality_score,


            "missing_values":
            record.missing_values,


            "duplicates":
            record.duplicates,


            "anomalies":
            record.anomalies,


            "status":
            record.status,


            "execution_time":
            record.execution_time,


            "uploaded_at":
            record.uploaded_at

        }


    finally:

        db.close()