from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from datetime import datetime


from services.repair_service import repair_dataset
from services.data_analysis_service import analyze_dataset
from services.agent_activity_service import update_agent


# Database
from database import SessionLocal
from models import DatasetHistory





router = APIRouter(
    prefix="",
    tags=["Dataset Upload"]
)





UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)





ALLOWED_FILES = [
    ".csv",
    ".xlsx",
    ".xls"
]









# =====================================
# Upload Status
# =====================================


@router.get("/upload")
def upload_info():

    return {

        "service":
        "Dataset Upload API",

        "status":
        "online",

        "endpoint":
        "/upload",

        "method":
        "POST"

    }









# =====================================
# Dataset Upload Pipeline
# =====================================


@router.post("/upload")
async def upload_dataset(

    file: UploadFile = File(...)

):


    start_time = datetime.now()



    # -------------------------------
    # Validate file
    # -------------------------------


    extension = os.path.splitext(
        file.filename
    )[1].lower()



    if extension not in ALLOWED_FILES:

        raise HTTPException(

            status_code=400,

            detail="Unsupported file type"

        )








    # -------------------------------
    # Investigator Agent
    # -------------------------------


    update_agent(

        "Data Investigator Agent",

        "Running",

        "Inspecting uploaded dataset"

    )







    # -------------------------------
    # Save Dataset
    # -------------------------------


    file_path = os.path.join(

        UPLOAD_FOLDER,

        file.filename

    )



    with open(

        file_path,

        "wb"

    ) as buffer:


        shutil.copyfileobj(

            file.file,

            buffer

        )









    # -------------------------------
    # Data Quality Analysis
    # -------------------------------


    update_agent(

        "Data Quality Agent",

        "Running",

        "Calculating quality metrics"

    )




    analysis = analyze_dataset(

        file_path

    )




    if "error" in analysis:


        update_agent(

            "Data Quality Agent",

            "Failed",

            analysis["error"]

        )


        return {

            "status":"FAILED",

            "error":analysis["error"]

        }







    quality = analysis.get(

        "quality_score",

        0

    )


    missing = analysis.get(

        "missing_values",

        0

    )


    duplicates = analysis.get(

        "duplicates",

        0

    )


    anomalies = analysis.get(

        "anomalies",

        0

    )









    # -------------------------------
    # Repair Agent
    # -------------------------------


    update_agent(

        "Repair Agent",

        "Running",

        "Cleaning dataset"

    )




    repair_result = repair_dataset(

        file_path

    )




    clean_file = repair_result.get(

        "file",

        ""

    )





    update_agent(

        "Repair Agent",

        "Completed",

        f"Generated {clean_file}"

    )









    execution_time = (

        datetime.now()

        -

        start_time

    ).total_seconds()







    # -------------------------------
    # Save Investigation History
    # -------------------------------


    db = SessionLocal()



    try:


        history = DatasetHistory(


            filename=file.filename,


            original_file=file_path,


            clean_file=clean_file,


            quality_score=quality,


            missing_values=missing,


            duplicates=duplicates,


            anomalies=anomalies,


            recommendations=str(

                analysis.get(

                    "recommendations",

                    []

                )

            ),



            root_cause=str(

                analysis.get(

                    "root_cause",

                    "No root cause detected"

                )

            ),



            repair_summary=str(

                repair_result

            ),



            execution_time=execution_time,


            agents_completed=8,


            status="COMPLETED"


        )





        db.add(history)


        db.commit()


        db.refresh(history)



    finally:


        db.close()











    # -------------------------------
    # Complete Agents
    # -------------------------------



    update_agent(

        "Data Quality Agent",

        "Completed",

        f"Quality score {quality}%"

    )



    update_agent(

        "Anomaly Detection Agent",

        "Completed",

        f"{anomalies} anomalies detected"

    )



    update_agent(

        "Root Cause Agent",

        "Completed",

        "Root cause analysis completed"

    )



    update_agent(

        "Recommendation Agent",

        "Completed",

        "Recommendations generated"

    )



    update_agent(

        "Prediction Agent",

        "Completed",

        "Future risks predicted"

    )



    update_agent(

        "Memory Agent",

        "Completed",

        "History stored in SQLite"

    )



    update_agent(

        "Data Investigator Agent",

        "Completed",

        "Investigation finished"

    )









    return {



        "status":

        "COMPLETED",



        "history_id":

        history.id,



        "filename":

        file.filename,



        "execution_time":

        execution_time,



        "analysis":analysis,



        "repair":{


            "clean_file":

            clean_file,



            "download":

            f"/download/{clean_file}"


        },



        "summary":{


            "quality_score":

            quality,


            "missing_values":

            missing,


            "duplicates":

            duplicates,


            "anomalies":

            anomalies


        }



    }