from datetime import datetime


class PipelineMonitoringAgent:

    def __init__(self):

        self.name = "Pipeline Monitoring Agent"

    def analyze(self, context):

        pipeline = context.get("lineage", [])

        report = {

            "agent": self.name,

            "timestamp": datetime.now().isoformat(),

            "status": "HEALTHY",

            "pipeline_steps": [],

            "issues": [],

            "health_score": 100

        }

        if len(pipeline) == 0:

            report["status"] = "UNKNOWN"

            report["issues"].append({

                "type": "Missing Pipeline",

                "message": "No pipeline lineage found."

            })

            report["health_score"] -= 40

            return report

        for i, step in enumerate(pipeline):

            report["pipeline_steps"].append({

                "step": i + 1,

                "component": step,

                "status": "SUCCESS"

            })

        if len(pipeline) < 3:

            report["issues"].append({

                "type": "Incomplete Pipeline",

                "message": "Pipeline appears incomplete."

            })

            report["health_score"] -= 20

        if report["health_score"] < 80:

            report["status"] = "WARNING"

        return report