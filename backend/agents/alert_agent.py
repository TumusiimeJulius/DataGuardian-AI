from datetime import datetime


class AlertMonitoringAgent:

    def __init__(self):

        self.name = "Alert & Monitoring Agent"


    def analyze(
        self,
        quality_report,
        anomaly_report,
        prediction_report
    ):

        alerts = []


        # Quality Score

        score = quality_report.get(
            "quality_score",
            100
        )

        if score < 80:

            alerts.append({

                "severity": "HIGH",

                "title": "Poor Data Quality",

                "message":
                f"Quality score dropped to {score}"

            })


        # Missing Values

        for issue in quality_report.get(
            "issues",
            []
        ):

            if issue["type"] == "Missing Values":

                alerts.append({

                    "severity": "MEDIUM",

                    "title": "Missing Data",

                    "message":
                    f"{issue['count']} missing values detected"

                })


        # Duplicate Records

        for issue in quality_report.get(
            "issues",
            []
        ):

            if issue["type"] == "Duplicate Records":

                alerts.append({

                    "severity": "MEDIUM",

                    "title": "Duplicate Records",

                    "message":
                    f"{issue['count']} duplicates detected"

                })


        # Anomalies

        if anomaly_report.get("anomaly_count", 0) > 0:

            alerts.append({

                "severity": "HIGH",

                "title": "Anomalies Detected",

                "message":
                f"{anomaly_report['anomaly_count']} anomalies found"

            })


        # Prediction

        if prediction_report.get(
            "risk",
            ""
        ) == "HIGH":

            alerts.append({

                "severity": "CRITICAL",

                "title": "Predicted Business Risk",

                "message":
                prediction_report.get("summary")

            })


        return {

            "agent": self.name,

            "timestamp": datetime.now().isoformat(),

            "alert_count": len(alerts),

            "alerts": alerts

        }