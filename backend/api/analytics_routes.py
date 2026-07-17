from fastapi import APIRouter

from database import SessionLocal

from models import DatasetHistory



router = APIRouter(
    prefix="",
    tags=["Analytics"]
)





@router.get("/analytics")
def analytics():


    db = SessionLocal()


    try:


        datasets = db.query(
            DatasetHistory
        ).all()



        total = len(datasets)



        if total == 0:

            return {

                "total_datasets":0,

                "average_quality":0,

                "missing_values":0,

                "duplicates":0,

                "anomalies":0,

                "repairs":0

            }





        average_quality = sum(

            item.quality_score or 0

            for item in datasets

        ) / total





        missing = sum(

            item.missing_values or 0

            for item in datasets

        )



        duplicates = sum(

            item.duplicates or 0

            for item in datasets

        )



        anomalies = sum(

            item.anomalies or 0

            for item in datasets

        )




        repairs = sum(

            1

            for item in datasets

            if item.clean_file

        )






        return {


            "total_datasets":

            total,



            "average_quality":

            round(
                average_quality,
                2
            ),



            "missing_values":

            missing,



            "duplicates":

            duplicates,



            "anomalies":

            anomalies,



            "repairs":

            repairs



        }



    finally:

        db.close()