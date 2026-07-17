import json
import os
from datetime import datetime


class MemoryAuditAgent:

    def __init__(self):

        self.name = "Memory & Audit Agent"

        self.memory_file = "investigation_history.json"

        if not os.path.exists(self.memory_file):

            with open(self.memory_file, "w") as f:

                json.dump([], f)



    def save(self, investigation):

        with open(self.memory_file, "r") as f:

            history = json.load(f)

        history.append(

            {

                "timestamp": datetime.now().isoformat(),

                "question": investigation.get("question"),

                "status": investigation.get("status"),

                "quality_score": (
                    investigation.get("quality_report") or
                    investigation.get("quality_report_before_repair") or
                    {}
                ).get("quality_score"),

                "issues": (
                    investigation.get("quality_report") or
                    investigation.get("quality_report_before_repair") or
                    {}
                ).get("issues"),

                "prediction": investigation.get(
                    "prediction_report"
                ),

                "root_causes": investigation.get(
                    "root_cause_report"
                )

            }

        )

        with open(self.memory_file, "w") as f:

            json.dump(history, f, indent=4)

        return {

            "saved": True,

            "total_investigations": len(history)

        }



    def history(self):

        with open(self.memory_file, "r") as f:

            return json.load(f)



    def latest(self):

        history = self.history()

        if len(history) == 0:

            return None

        return history[-1]



    def compare_last_two(self):

        history = self.history()

        if len(history) < 2:

            return {

                "message": "Not enough investigations"

            }

        previous = history[-2]

        current = history[-1]

        prev_score = previous.get("quality_score")
        curr_score = current.get("quality_score")

        if prev_score is None or curr_score is None:
            return {
                "message": "Quality score missing in history records"
            }

        return {

            "previous_quality":

                prev_score,

            "current_quality":

                curr_score,

            "difference":

                curr_score - prev_score

        }