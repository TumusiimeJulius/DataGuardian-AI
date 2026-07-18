try:
    import pandas as pd
except Exception:  # pragma: no cover - allows missing dependency
    pd = None


class DataQualityAgent:

    def __init__(self):
        self.name = "Data Quality Agent"


    def analyze(self, data):

        if isinstance(data, dict):
            columns = list(data.keys())
        elif hasattr(data, 'columns'):
            columns = list(data.columns)
        else:
            columns = []

        report = {
            "agent": self.name,
            "dataset_rows": len(data) if hasattr(data, '__len__') else 0,
            "columns": columns,
            "issues": [],
            "recommendations": [],
            "quality_score": 100
        }


        # Empty dataset check

        if len(data) == 0:

            report["issues"].append(
                {
                    "type": "Empty Dataset"
                }
            )

            report["quality_score"] -= 50



        # Missing values

        if pd is not None:
            missing = data.isnull().sum()


            for column, count in missing.items():

                if count > 0:

                    report["issues"].append(
                        {
                            "type": "Missing Values",
                            "column": column,
                            "count": int(count)
                        }
                    )

                    report["recommendations"].append(
                        f"Fill missing values in {column}"
                    )

                    report["quality_score"] -= 10



        # Duplicate rows
        if pd is not None:
            duplicates = data.duplicated().sum()


            if duplicates > 0:
                report["issues"].append(
                    {
                        "type": "Duplicate Records",
                        "count": int(duplicates)
                    }
                )


                report["recommendations"].append(
                    "Remove duplicate records"
                )


                report["quality_score"] -= 10




        # Invalid dates

        if pd is not None and "created_at" in data.columns:


            invalid_dates = pd.to_datetime(
                data["created_at"],
                errors="coerce"
            ).isna().sum()



            if invalid_dates > 0:

                report["issues"].append(
                    {
                        "type":"Invalid Dates",
                        "count":int(invalid_dates)
                    }
                )


                report["recommendations"].append(
                    "Fix invalid date formats"
                )


                report["quality_score"] -= 10




        # Negative revenue check

        if pd is not None and "amount" in data.columns:


            negative_amounts = (
                data["amount"] < 0
            ).sum()



            if negative_amounts > 0:


                report["issues"].append(
                    {
                        "type":"Negative Revenue",
                        "count":int(negative_amounts)
                    }
                )


                report["recommendations"].append(
                    "Review negative transaction values"
                )


                report["quality_score"] -= 10




        # Limit score

        if report["quality_score"] < 0:

            report["quality_score"] = 0



        return report