from datetime import datetime


class RepairAgent:

    def __init__(self):

        self.name = "Repair Agent"


    def repair(
        self,
        data,
        quality_report,
        anomaly_report,
        root_cause_report
    ):


        repaired_actions = []


        # ---------------------------------
        # Missing values repair
        # ---------------------------------

        try:

            missing_values = data.isnull().sum()


            for column, value in missing_values.items():

                if value > 0:

                    data[column] = data[column].fillna(
                        data[column].mean()
                        if data[column].dtype != "object"
                        else "Unknown"
                    )


                    repaired_actions.append({

                        "issue": "Missing Values",

                        "column": column,

                        "action": "Filled missing values"

                    })


        except Exception as e:


            repaired_actions.append({

                "issue": "Missing value repair failed",

                "error": str(e)

            })



        # ---------------------------------
        # Duplicate records repair
        # ---------------------------------

        try:

            duplicates = data.duplicated().sum()


            if duplicates > 0:

                data.drop_duplicates(
                    inplace=True
                )


                repaired_actions.append({

                    "issue": "Duplicate Records",

                    "action": f"Removed {duplicates} duplicate rows"

                })


        except Exception as e:


            repaired_actions.append({

                "issue": "Duplicate repair failed",

                "error": str(e)

            })



        # ---------------------------------
        # Final Repair Report
        # ---------------------------------

        return {


            "agent": self.name,


            "timestamp": datetime.now().isoformat(),


            "status": "COMPLETED",


            "repair_actions": repaired_actions,


            "quality_before": quality_report,


            "anomaly_reference": anomaly_report,


            "root_cause_reference": root_cause_report,


            "message": "Dataset repair process completed"

        }