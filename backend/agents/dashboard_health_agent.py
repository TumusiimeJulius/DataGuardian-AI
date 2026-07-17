class DashboardHealthAgent:


    def __init__(self):

        self.name = "Dashboard Health Agent"



    def calculate(
        self,
        quality_report,
        anomaly_report,
        root_cause_report
    ):


        score = 100


        # Reduce score based on quality issues

        score -= (
            100 - quality_report["quality_score"]
        )



        # Reduce score based on anomalies

        anomaly_count = anomaly_report.get(
            "anomalies_detected",
            0
        )


        score -= anomaly_count * 5



        # Reduce score based on root causes

        root_causes = root_cause_report.get(
            "root_causes",
            []
        )


        score -= len(root_causes) * 5



        # Prevent negative score

        if score < 0:

            score = 0



        # Determine status

        if score >= 90:

            status = "HEALTHY"


        elif score >= 70:

            status = "WARNING"


        else:

            status = "CRITICAL"



        return {


            "agent":
            self.name,


            "dashboard":
            "Sales Dashboard",


            "health_score":
            score,


            "status":
            status,


            "summary":
            self.generate_summary(status)

        }



    def generate_summary(self, status):


        if status == "HEALTHY":

            return "Dashboard data is reliable"



        elif status == "WARNING":

            return "Dashboard requires data quality investigation"



        else:

            return "Dashboard has critical data reliability problems"