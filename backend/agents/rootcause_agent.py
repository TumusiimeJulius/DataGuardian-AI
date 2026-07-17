class RootCauseAgent:


    def __init__(self):

        self.name = "Root Cause Agent"



    def analyze(self, quality_report):

        causes = []


        for issue in quality_report["issues"]:


            if issue["type"] == "Missing Values":

                causes.append({

                    "problem":
                    "Missing transaction values",

                    "possible_cause":
                    "Incomplete data ingestion pipeline",

                    "confidence":
                    "85%"

                })



            elif issue["type"] == "Duplicate Records":

                causes.append({

                    "problem":
                    "Duplicate transactions",

                    "possible_cause":
                    "ETL process loading duplicate records",

                    "confidence":
                    "90%"

                })



            elif issue["type"] == "Invalid Dates":

                causes.append({

                    "problem":
                    "Invalid date values",

                    "possible_cause":
                    "Incorrect date formatting during data import",

                    "confidence":
                    "75%"

                })



        return {


            "agent":
            self.name,


            "root_causes":
            causes

        }