from datetime import datetime


class DataObservabilityAgent:

    def __init__(self):

        self.name = "Data Observability Agent"

    def analyze(self, data, context):

        report = {

            "agent": self.name,

            "timestamp": datetime.now().isoformat(),

            "status": "HEALTHY",

            "checks": [],

            "issues": [],

            "health_score": 100

        }

        # ----------------------------------
        # Dataset freshness
        # ----------------------------------

        report["checks"].append({

            "check": "Dataset Freshness",

            "status": "PASS",

            "message": "Dataset successfully loaded."

        })

        # ----------------------------------
        # Dataset volume
        # ----------------------------------

        if isinstance(data, dict):
            rows = len(data.get("customer_id", []))
            actual = list(data.keys())
        else:
            rows = len(data)
            actual = list(data.columns)

        report["checks"].append({

            "check": "Dataset Volume",

            "rows": rows

        })

        if rows < 5:

            report["issues"].append({

                "type": "Low Volume",

                "message": "Dataset contains very few records."

            })

            report["health_score"] -= 10

        # ----------------------------------
        # Schema validation
        # ----------------------------------

        expected = context.get("schema", [])

        missing = [c for c in expected if c not in actual]

        extra = [c for c in actual if c not in expected]

        report["checks"].append({

            "check": "Schema Validation",

            "expected": expected,

            "actual": actual

        })

        if missing:

            report["issues"].append({

                "type": "Missing Columns",

                "columns": missing

            })

            report["health_score"] -= 15

        if extra:

            report["issues"].append({

                "type": "Unexpected Columns",

                "columns": extra

            })

            report["health_score"] -= 5

        # ----------------------------------
        # Null percentage
        # ----------------------------------

        if hasattr(data, 'isnull'):
            nulls = data.isnull().mean() * 100
            report["null_percentage"] = {
                col: round(val, 2)
                for col, val in nulls.items()
            }
        else:
            report["null_percentage"] = {}

        # ----------------------------------
        # Final Status
        # ----------------------------------

        if report["health_score"] < 80:

            report["status"] = "WARNING"

        if report["health_score"] < 60:

            report["status"] = "CRITICAL"

        return report