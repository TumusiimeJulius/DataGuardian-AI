import pandas as pd



class AnomalyDetectionAgent:


    def __init__(self):

        self.name = "Data Anomaly Detection Agent"



    def analyze(self, data):


        report = {

            "agent": self.name,

            "anomalies": [],

            "anomaly_score": 100

        }



        # --------------------------------
        # 1. Detect missing values
        # --------------------------------

        missing = data.isnull().sum()


        for column, count in missing.items():

            if count > 0:

                report["anomalies"].append(

                    {

                        "type":
                        "Missing Data Anomaly",


                        "column":
                        column,


                        "count":
                        int(count),


                        "severity":
                        "MEDIUM"

                    }

                )


                report["anomaly_score"] -= 10





        # --------------------------------
        # 2. Detect duplicate transactions
        # --------------------------------

        duplicates = data.duplicated().sum()


        if duplicates > 0:


            report["anomalies"].append(

                {


                    "type":
                    "Duplicate Transaction Anomaly",


                    "count":
                    int(duplicates),


                    "severity":
                    "HIGH"

                }

            )


            report["anomaly_score"] -= 15





        # --------------------------------
        # 3. Detect abnormal amounts
        # --------------------------------

        if "amount" in data.columns:


            try:


                mean_amount = data["amount"].mean()


                std_amount = data["amount"].std()



                if std_amount > 0:


                    outliers = data[

                        abs(
                            data["amount"] - mean_amount
                        )

                        >

                        2 * std_amount

                    ]



                    if len(outliers) > 0:


                        report["anomalies"].append(

                            {


                                "type":
                                "Revenue Outlier Detection",


                                "count":
                                int(len(outliers)),


                                "description":
                                "Transactions with unusual revenue values detected",


                                "severity":
                                "HIGH"


                            }

                        )


                        report["anomaly_score"] -= 20



            except Exception as e:


                report["anomalies"].append(

                    {

                        "type":
                        "Amount Analysis Error",

                        "error":
                        str(e)

                    }

                )






        # --------------------------------
        # 4. Detect invalid dates
        # --------------------------------

        if "created_at" in data.columns:


            invalid_dates = pd.to_datetime(

                data["created_at"],

                errors="coerce"

            ).isna().sum()



            if invalid_dates > 0:


                report["anomalies"].append(

                    {


                        "type":
                        "Invalid Date Anomaly",


                        "count":
                        int(invalid_dates),


                        "severity":
                        "MEDIUM"


                    }

                )


                report["anomaly_score"] -= 10





        # Keep score between 0-100

        if report["anomaly_score"] < 0:

            report["anomaly_score"] = 0



        return report