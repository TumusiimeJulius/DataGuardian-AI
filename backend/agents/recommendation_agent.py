class RecommendationAgent:


    def __init__(self):

        self.name = "Data Recommendation Agent"



    def generate(self, quality_report):


        recommendations = []

        priority = "LOW"



        issues = quality_report.get("issues", [])



        for issue in issues:


            issue_type = issue["type"]



            if issue_type == "Missing Values":

                priority = "HIGH"

                recommendations.append(
                    {
                        "problem":
                        f"Missing values detected in {issue['column']}",

                        "solution":
                        "Clean missing records or apply appropriate default values",

                        "action":
                        f"Review column {issue['column']} before dashboard refresh"
                    }
                )



            elif issue_type == "Duplicate Records":


                priority = "HIGH"


                recommendations.append(
                    {
                        "problem":
                        "Duplicate transaction records found",

                        "solution":
                        "Remove duplicate rows using transaction identifiers",

                        "action":
                        "Run duplicate detection before loading data"
                    }
                )



            elif issue_type == "Invalid Dates":


                priority = "MEDIUM"


                recommendations.append(
                    {
                        "problem":
                        "Invalid date values detected",

                        "solution":
                        "Validate and standardize date formats",

                        "action":
                        "Apply date validation during ETL process"
                    }
                )



            elif issue_type == "Negative Revenue":


                priority = "HIGH"


                recommendations.append(
                    {
                        "problem":
                        "Negative revenue values detected",

                        "solution":
                        "Verify transaction calculations",

                        "action":
                        "Audit affected transactions"
                    }
                )



        return {


            "agent": self.name,

            "priority": priority,

            "recommendations": recommendations

        }