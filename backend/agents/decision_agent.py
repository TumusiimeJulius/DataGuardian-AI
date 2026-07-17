class DecisionAgent:


    def __init__(self):

        self.name = "Data Decision Agent"



    def decide(
        self,
        quality_report,
        anomaly_report,
        prediction_report,
        root_cause_report,
        recommendation_report
    ):


        decision = {


            "agent":
            self.name,


            "priority":
            "LOW",


            "decisions":
            [],


            "business_action":
            ""

        }



        # -------------------------------
        # Check data quality problems
        # -------------------------------

        quality_score = quality_report.get(
            "quality_score",
            100
        )


        if quality_score < 80:


            decision["priority"] = "HIGH"


            decision["decisions"].append(

                {

                    "issue":
                    "Poor data quality",


                    "action":
                    "Clean and validate sales data before dashboard refresh"

                }

            )




        # -------------------------------
        # Check anomalies
        # -------------------------------

        anomalies = anomaly_report.get(

            "anomalies",

            []

        )


        if len(anomalies) > 0:


            decision["priority"] = "HIGH"


            decision["decisions"].append(

                {

                    "issue":
                    "Suspicious data patterns detected",


                    "action":
                    "Investigate abnormal transactions"

                }

            )




        # -------------------------------
        # Check predictions
        # -------------------------------

        predictions = prediction_report.get(

            "predictions",

            []

        )


        for prediction in predictions:


            if prediction.get("trend") == "Declining":


                decision["priority"] = "HIGH"


                decision["decisions"].append(

                    {

                        "issue":
                        "Revenue decline predicted",


                        "action":
                        "Review customer engagement and sales strategy"

                    }

                )





        # -------------------------------
        # Default recommendation
        # -------------------------------

        if len(decision["decisions"]) == 0:


            decision["business_action"] = (

                "System healthy. Continue monitoring sales performance."

            )


        else:


            decision["business_action"] = (

                "Prioritize data correction, investigate causes, "
                "and validate business reports before decision making."

            )




        return decision