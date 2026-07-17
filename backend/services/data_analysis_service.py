import pandas as pd
import os


def analyze_dataset(file_path):

    try:

        # Load dataset

        if file_path.endswith(".csv"):

            df = pd.read_csv(file_path)


        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):

            df = pd.read_excel(file_path)


        else:

            return {

                "error":
                "Unsupported file format"

            }





        # Basic statistics

        rows = len(df)

        columns = len(df.columns)



        # Missing values

        missing_values = int(
            df.isnull()
            .sum()
            .sum()
        )



        # Duplicate records

        duplicates = int(
            df.duplicated()
            .sum()
        )





        # Data quality calculation

        total_cells = rows * columns


        if total_cells > 0:

            quality_score = round(

                (
                    1 -
                    (
                        missing_values + duplicates
                    )
                    /
                    total_cells

                )
                *
                100,

                2

            )

        else:

            quality_score = 0





        # Simple anomaly detection

        anomalies = 0


        numeric_columns = df.select_dtypes(
            include="number"
        )



        for column in numeric_columns:


            mean = numeric_columns[column].mean()

            std = numeric_columns[column].std()



            if std != 0:


                outliers = df[

                    abs(
                        df[column]-mean
                    )
                    >
                    3*std

                ]

                anomalies += len(outliers)





        recommendations=[]



        if missing_values > 0:

            recommendations.append(

                "Fill missing values using appropriate methods"

            )



        if duplicates > 0:

            recommendations.append(

                "Remove duplicate records"

            )



        if anomalies > 0:

            recommendations.append(

                "Investigate detected abnormal records"

            )



        if quality_score > 90:

            recommendations.append(

                "Dataset quality is excellent"

            )





        return {


            "dataset":

            os.path.basename(file_path),



            "rows":

            rows,



            "columns":

            columns,



            "missing_values":

            missing_values,



            "duplicates":

            duplicates,



            "anomalies":

            anomalies,



            "quality_score":

            quality_score,



            "recommendations":

            recommendations

        }





    except Exception as e:


        return {

            "error":
            str(e)

        }