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

                "quality_score": investigation.get(
                    "quality_report",
                    {}
                ).get("quality_score"),

                "issues": investigation.get(
                    "quality_report",
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

        return {

            "previous_quality":

                previous["quality_score"],

            "current_quality":

                current["quality_score"],

            "difference":

                current["quality_score"] -
                previous["quality_score"]

        }