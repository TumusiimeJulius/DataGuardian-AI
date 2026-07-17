class LineageAgent:


    def __init__(self):

        self.name = "Data Lineage Agent"



    def analyze(self, context):


        lineage = context.get(
            "lineage",
            []
        )


        analysis = {


            "agent":
            self.name,


            "pipeline":
            lineage,


            "impact_analysis":
            [],

        }



        if "raw_transactions" in lineage:


            analysis["impact_analysis"].append(

                {
                    "source":
                    "raw_transactions",

                    "role":
                    "Original transaction data source",

                    "risk":
                    "High"

                }

            )



        if "sales_model" in lineage:


            analysis["impact_analysis"].append(

                {

                    "source":
                    "sales_model",

                    "role":
                    "Revenue calculation layer",

                    "risk":
                    "Critical"

                }

            )



        if "dashboard" in lineage:


            analysis["impact_analysis"].append(

                {

                    "source":
                    "dashboard",

                    "role":
                    "Visualization layer",

                    "risk":
                    "Medium"

                }

            )



        return analysis