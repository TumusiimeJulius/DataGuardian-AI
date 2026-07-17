import pandas as pd
import os



CLEAN_FOLDER = "cleaned"


os.makedirs(
    CLEAN_FOLDER,
    exist_ok=True
)



def repair_dataset(file_path):


    df = pd.read_csv(file_path)



    original_rows = len(df)



    # Remove duplicate rows

    duplicates = df.duplicated().sum()

    df = df.drop_duplicates()



    # Fill missing values

    for column in df.columns:

        if df[column].dtype == "object":

            df[column] = df[column].fillna(
                "Unknown"
            )

        else:

            df[column] = df[column].fillna(
                df[column].median()
            )



    cleaned_rows = len(df)



    filename = os.path.basename(
        file_path
    )



    clean_filename = (

        filename.replace(
            ".csv",
            "_cleaned.csv"
        )

    )



    output_path = os.path.join(

        CLEAN_FOLDER,

        clean_filename

    )



    df.to_csv(

        output_path,

        index=False

    )



    return {


        "clean_file":
        clean_filename,


        "removed_duplicates":
        int(duplicates),


        "original_rows":
        original_rows,


        "cleaned_rows":
        cleaned_rows,


        "path":
        output_path

    }