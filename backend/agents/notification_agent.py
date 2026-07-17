from datetime import datetime


class NotificationAgent:

    def __init__(self):

        self.name = "Notification Agent"


    def notify(self, alert_report):

        notifications = []

        for alert in alert_report.get("alerts", []):

            notifications.append({

                "channel": "Dashboard",

                "severity": alert["severity"],

                "title": alert["title"],

                "message": alert["message"],

                "status": "READY"

            })

        return {

            "agent": self.name,

            "timestamp": datetime.now().isoformat(),

            "notification_count": len(notifications),

            "notifications": notifications

        }