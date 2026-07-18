from datetime import datetime
from pathlib import Path
import traceback
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
from agents.pipeline_agent import PipelineMonitoringAgent
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
        self.pipeline_agent = PipelineMonitoringAgent()
        self.repair_agent = RepairAgent()

    # -------------------------------------------------
    # Safe Execution
    # -------------------------------------------------

    def _safe_execute(self, func, *args):

        try:
            return func(*args)

        except Exception as e:

            print(f"\nERROR in {func.__name__}")
            traceback.print_exc()

            return {
                "status": "FAILED",
                "agent": func.__name__,
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    # -------------------------------------------------
    # Investigation
    # -------------------------------------------------

    def investigate(self, question):

        start_time = time.time()

        # ---------------------------------------------
        # DataHub
        # ---------------------------------------------

        context = self._safe_execute(
            datahub_client.search_dataset,
            "sales"
        )

        # ---------------------------------------------
        # Lineage
        # ---------------------------------------------

        lineage_report = self._safe_execute(
            self.lineage_agent.analyze,
            context
        )

        # ---------------------------------------------
        # Pipeline
        # ---------------------------------------------

        pipeline_report = self._safe_execute(
            self.pipeline_agent.analyze,
            {"lineage": lineage_report}
        )

        # ---------------------------------------------
        # Dataset
        # ---------------------------------------------

        try:

            BASE_DIR = Path(__file__).resolve().parent.parent

            dataset_path = BASE_DIR / "test_sales.csv"

            print("Dataset:", dataset_path)

            if not dataset_path.exists():

                return {
                    "status": "FAILED",
                    "agent": self.name,
                    "error": f"Dataset not found: {dataset_path}"
                }

            data = pd.read_csv(dataset_path)

        except Exception:

            return {
                "status": "FAILED",
                "agent": self.name,
                "error": "Dataset loading failed",
                "traceback": traceback.format_exc()
            }

        # ---------------------------------------------
        # Observability
        # ---------------------------------------------

        observability_report = self._safe_execute(
            self.observability_agent.analyze,
            data,
            context
        )

        # ---------------------------------------------
        # Quality
        # ---------------------------------------------

        quality_report = self._safe_execute(
            self.quality_agent.analyze,
            data
        )

        # ---------------------------------------------
        # Anomalies
        # ---------------------------------------------

        anomaly_report = self._safe_execute(
            self.anomaly_agent.analyze,
            data
        )

        # ---------------------------------------------
        # Prediction
        # ---------------------------------------------

        prediction_report = self._safe_execute(
            self.prediction_agent.predict,
            data
        )

        # ---------------------------------------------
        # Root Cause
        # ---------------------------------------------

        root_cause_report = self._safe_execute(
            self.rootcause_agent.analyze,
            quality_report
        )

        # ---------------------------------------------
        # Repair
        # ---------------------------------------------

        repair_report = self._safe_execute(
            self.repair_agent.repair,
            data,
            quality_report,
            anomaly_report,
            root_cause_report
        )

        # ---------------------------------------------
        # Quality After Repair
        # ---------------------------------------------

        quality_after = self._safe_execute(
            self.quality_agent.analyze,
            data
        )

        # ---------------------------------------------
        # Recommendation
        # ---------------------------------------------

        recommendation_report = self._safe_execute(
            self.recommendation_agent.generate,
            quality_after
        )

        # ---------------------------------------------
        # Decision
        # ---------------------------------------------

        decision_report = self._safe_execute(
            self.decision_agent.decide,
            quality_after,
            anomaly_report,
            prediction_report,
            root_cause_report,
            recommendation_report
        )

        # ---------------------------------------------
        # Alerts
        # ---------------------------------------------

        alert_report = self._safe_execute(
            self.alert_agent.analyze,
            quality_after,
            anomaly_report,
            prediction_report
        )

        # ---------------------------------------------
        # AI
        # ---------------------------------------------

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
                "quality_after_repair": quality_after,
                "recommendations": recommendation_report,
                "decision": decision_report,
                "alerts": alert_report,
            },
        )

        execution_time = round(time.time() - start_time, 3)

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
            "quality_report_after_repair": quality_after,
            "recommendation_report": recommendation_report,
            "decision_report": decision_report,
            "alert_report": alert_report,
            "report": analysis,
        }

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