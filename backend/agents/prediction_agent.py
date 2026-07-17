import pandas as pd
from datetime import datetime



class PredictionAgent:


    def __init__(self):

        self.name = "Data Prediction Agent"



    def predict(self, data):


        report = {

            "agent": self.name,

            "predictions": [],

            "generated_at": datetime.now().isoformat()

        }



        # --------------------------------
        # Check revenue column
        # --------------------------------

        if "amount" not in data.columns:


            report["predictions"].append(

                {

                    "error":
                    "Amount column not found"

                }

            )


            return report




        # Convert amount to numeric

        data["amount"] = pd.to_numeric(

            data["amount"],

            errors="coerce"

        )



        clean_data = data.dropna(

            subset=["amount"]

        )



        if len(clean_data) == 0:


            report["predictions"].append(

                {

                    "error":
                    "No valid revenue data available"

                }

            )


            return report





        # --------------------------------
        # Revenue statistics
        # --------------------------------


        total_revenue = clean_data["amount"].sum()


        average_transaction = clean_data["amount"].mean()



        report["predictions"].append(

            {


                "metric":
                "Current Revenue",


                "value":
                float(total_revenue)


            }

        )



        report["predictions"].append(

            {


                "metric":
                "Average Transaction Value",


                "value":
                round(float(average_transaction),2)


            }

        )





        # --------------------------------
        # Simple trend prediction
        # --------------------------------


        if len(clean_data) >= 2:


            first_value = clean_data["amount"].iloc[0]


            last_value = clean_data["amount"].iloc[-1]



            if last_value > first_value:


                trend = "Increasing"



                prediction = (

                    "Revenue is showing positive growth. "
                    "Expected future revenue may increase."

                )


            elif last_value < first_value:


                trend = "Declining"



                prediction = (

                    "Revenue is declining. "
                    "Investigate customer activity and sales pipeline."

                )


            else:


                trend = "Stable"


                prediction = (

                    "Revenue is stable with no significant change."

                )




            report["predictions"].append(

                {

                    "metric":
                    "Revenue Trend",


                    "trend":
                    trend,


                    "prediction":
                    prediction

                }

            )





        # --------------------------------
        # Customer analysis
        # --------------------------------


        if "customer_id" in clean_data.columns:


            customers = clean_data.groupby(

                "customer_id"

            )["amount"].sum()



            top_customer = customers.idxmax()



            report["predictions"].append(

                {


                    "metric":
                    "Top Customer",


                    "customer_id":
                    int(top_customer),


                    "revenue":
                    float(customers.max())


                }

            )



        return report