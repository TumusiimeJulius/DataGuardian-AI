from datetime import datetime
import time

import pandas as pd

from datahub.client import datahub_client
from agents.ai_service import generate_analysis

from agents.quality_agent import DataQualityAgent
from agents.recommendation_agent import RecommendationAgent
from agents.rootcause_agent import RootCauseAgent
from agents.lineage_agent import LineageAgent
from agents.anomaly_agent import AnomalyDetectionAgent
from agents.prediction_agent import PredictionAgent
from agents.decision_agent import DecisionAgent
from agents.memory_agent import MemoryAuditAgent
from agents.alert_agent import AlertMonitoringAgent
from agents.observability_agent import DataObservabilityAgent

# Pipeline Agent
from agents.pipeline_agent import PipelineMonitoringAgent

# Repair Agent
from agents.repair_agent import RepairAgent



class DataInvestigatorAgent:


    def __init__(self):

        self.name = "Data Investigator Agent"


        self.quality_agent = DataQualityAgent()

        self.recommendation_agent = RecommendationAgent()

        self.rootcause_agent = RootCauseAgent()

        self.lineage_agent = LineageAgent()

        self.anomaly_agent = AnomalyDetectionAgent()

        self.prediction_agent = PredictionAgent()

        self.decision_agent = DecisionAgent()

        self.memory_agent = MemoryAuditAgent()

        self.alert_agent = AlertMonitoringAgent()

        self.observability_agent = DataObservabilityAgent()


        # Pipeline Monitoring
        self.pipeline_agent = PipelineMonitoringAgent()


        # Data Repair
        self.repair_agent = RepairAgent()



    # ----------------------------------------
    # Safe Execution Handler
    # ----------------------------------------

    def _safe_execute(self, func, *args):

        try:

            return func(*args)


        except Exception as e:

            return {

                "status": "FAILED",

                "error": str(e)

            }



    # ----------------------------------------
    # Investigation Engine
    # ----------------------------------------

    def investigate(self, question):


        start_time = time.time()



        # ----------------------------------------
        # DataHub Context
        # ----------------------------------------

        context = self._safe_execute(

            datahub_client.search_dataset,

            "sales"

        )



        # ----------------------------------------
        # Lineage Analysis
        # ----------------------------------------

        lineage_report = self._safe_execute(

            self.lineage_agent.analyze,

            context

        )



        # ----------------------------------------
        # Pipeline Monitoring
        # ----------------------------------------

        pipeline_report = self._safe_execute(

            self.pipeline_agent.analyze,

            {

                "lineage": lineage_report

            }

        )



        # ----------------------------------------
        # Load Dataset
        # ----------------------------------------

        try:

            data = pd.read_csv(
                "test_sales.csv"
            )


        except Exception as e:

            return {

                "agent": self.name,

                "status": "FAILED",

                "timestamp": datetime.now().isoformat(),

                "error": f"Dataset loading failed: {str(e)}"

            }



        # ----------------------------------------
        # Data Observability
        # ----------------------------------------

        observability_report = self._safe_execute(

            self.observability_agent.analyze,

            data,

            context

        )



        # ----------------------------------------
        # Initial Data Quality
        # ----------------------------------------

        quality_report = self._safe_execute(

            self.quality_agent.analyze,

            data

        )



        # ----------------------------------------
        # Anomaly Detection
        # ----------------------------------------

        anomaly_report = self._safe_execute(

            self.anomaly_agent.analyze,

            data

        )



        # ----------------------------------------
        # Prediction
        # ----------------------------------------

        prediction_report = self._safe_execute(

            self.prediction_agent.predict,

            data

        )



        # ----------------------------------------
        # Root Cause Analysis
        # ----------------------------------------

        root_cause_report = self._safe_execute(

            self.rootcause_agent.analyze,

            quality_report

        )



        # ----------------------------------------
        # Automated Data Repair
        # ----------------------------------------

        repair_report = self._safe_execute(

            self.repair_agent.repair,

            data,

            quality_report,

            anomaly_report,

            root_cause_report

        )



        # ----------------------------------------
        # Post Repair Validation
        # ----------------------------------------

        post_repair_quality_report = self._safe_execute(

            self.quality_agent.analyze,

            data

        )



        # ----------------------------------------
        # Recommendations
        # ----------------------------------------

        recommendation_report = self._safe_execute(

            self.recommendation_agent.generate,

            post_repair_quality_report

        )



        # ----------------------------------------
        # Decision Engine
        # ----------------------------------------

        decision_report = self._safe_execute(

            self.decision_agent.decide,

            post_repair_quality_report,

            anomaly_report,

            prediction_report,

            root_cause_report,

            recommendation_report

        )



        # ----------------------------------------
        # Alert Monitoring
        # ----------------------------------------

        alert_report = self._safe_execute(

            self.alert_agent.analyze,

            post_repair_quality_report,

            anomaly_report,

            prediction_report

        )



        # ----------------------------------------
        # AI Explanation
        # ----------------------------------------

        analysis = self._safe_execute(

            generate_analysis,

            question,

            {


                "datahub": context,


                "lineage": lineage_report,


                "pipeline": pipeline_report,


                "observability": observability_report,


                "quality_before_repair": quality_report,


                "anomalies": anomaly_report,


                "predictions": prediction_report,


                "root_causes": root_cause_report,


                "repair": repair_report,


                "quality_after_repair": post_repair_quality_report,


                "recommendations": recommendation_report,


                "decision": decision_report,


                "alerts": alert_report


            }

        )



        execution_time = round(

            time.time() - start_time,

            3

        )



        # ----------------------------------------
        # Final Investigation Report
        # ----------------------------------------

        investigation = {


            "agent": self.name,


            "status": "COMPLETED",


            "timestamp": datetime.now().isoformat(),


            "execution_time_seconds": execution_time,


            "question": question,


            "datahub_context": context,


            "lineage_report": lineage_report,


            "pipeline_report": pipeline_report,


            "observability_report": observability_report,


            "quality_report_before_repair": quality_report,


            "anomaly_report": anomaly_report,


            "prediction_report": prediction_report,


            "root_cause_report": root_cause_report,


            "repair_report": repair_report,


            "quality_report_after_repair": post_repair_quality_report,


            "recommendation_report": recommendation_report,


            "decision_report": decision_report,


            "alert_report": alert_report,


            "report": analysis


        }



        # ----------------------------------------
        # Memory Audit
        # ----------------------------------------

        memory_report = self._safe_execute(

            self.memory_agent.save,

            investigation

        )


        comparison_report = self._safe_execute(

            self.memory_agent.compare_last_two

        )



        investigation["memory_report"] = memory_report

        investigation["comparison_report"] = comparison_report



        return investigation
    