from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os


router = APIRouter(
    tags=["Dataset Download"]
)



CLEAN_FOLDER = "cleaned"


os.makedirs(
    CLEAN_FOLDER,
    exist_ok=True
)




# =====================================
# Download Clean Dataset
# =====================================

@router.get("/download/{filename}")
def download_clean_dataset(
    filename: str
):


    file_path = os.path.join(
        CLEAN_FOLDER,
        filename
    )



    # Security check
    if not os.path.abspath(file_path).startswith(
        os.path.abspath(CLEAN_FOLDER)
    ):

        raise HTTPException(

            status_code=403,

            detail="Invalid file path"

        )




    # Check file exists

    if not os.path.exists(file_path):

        raise HTTPException(

            status_code=404,

            detail="Clean dataset not found"

        )




    extension = os.path.splitext(
        filename
    )[1].lower()



    if extension == ".csv":

        media_type = "text/csv"


    elif extension in [".xlsx",".xls"]:

        media_type = (
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )


    else:

        media_type = "application/octet-stream"





    return FileResponse(

        path=file_path,

        filename=filename,

        media_type=media_type

    )





# =====================================
# List Available Clean Files
# =====================================

@router.get("/downloads")
def list_clean_files():


    files = []


    for file in os.listdir(CLEAN_FOLDER):

        files.append({

            "filename": file,

            "download_url":
            f"/download/{file}"

        })



    return {


        "folder":
        CLEAN_FOLDER,


        "files":
        files


    }