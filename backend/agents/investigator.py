from datetime import datetime
from pathlib import Path
import traceback
import time
import sys

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
        self.initialization_errors = []

        # Initialize agents with error tracking
        agents_to_init = [
            ('quality_agent', DataQualityAgent),
            ('recommendation_agent', RecommendationAgent),
            ('rootcause_agent', RootCauseAgent),
            ('lineage_agent', LineageAgent),
            ('anomaly_agent', AnomalyDetectionAgent),
            ('prediction_agent', PredictionAgent),
            ('decision_agent', DecisionAgent),
            ('memory_agent', MemoryAuditAgent),
            ('alert_agent', AlertMonitoringAgent),
            ('observability_agent', DataObservabilityAgent),
            ('pipeline_agent', PipelineMonitoringAgent),
            ('repair_agent', RepairAgent),
        ]
        
        for agent_name, agent_class in agents_to_init:
            try:
                setattr(self, agent_name, agent_class())
            except Exception as e:
                self.initialization_errors.append({
                    'agent': agent_name,
                    'error': str(e),
                    'trace': traceback.format_exc()
                })
                # Set to None so we can handle gracefully
                setattr(self, agent_name, None)
        
        # If there are errors, log them but continue
        if self.initialization_errors:
            print(f"\n[WARN] {len(self.initialization_errors)} agent(s) failed to initialize:")
            for err in self.initialization_errors:
                print(f"  - {err['agent']}: {err['error']}")

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
        
        # Report any initialization errors first
        if self.initialization_errors:
            return {
                "status": "PARTIAL_FAILURE",
                "question": question,
                "message": f"{len(self.initialization_errors)} agent(s) failed to initialize",
                "initialization_errors": self.initialization_errors,
            }

        # Continue with investigation if all agents initialized successfully

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
                # Use mock data when file doesn't exist
                print("[INVESTIGATE] Dataset not found. Using mock data.", file=sys.stderr)
                data = pd.DataFrame({
                    "customer_id": [1, 2, 3, 4],
                    "amount": [100.0, 150.0, 200.0, 75.0],
                    "created_at": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
                })
            else:
                data = pd.read_csv(dataset_path)

        except Exception as e:

            print(f"[INVESTIGATE] Error loading dataset: {str(e)}", file=sys.stderr)
            # Still use mock data as fallback
            data = pd.DataFrame({
                "customer_id": [1, 2, 3, 4],
                "amount": [100.0, 150.0, 200.0, 75.0],
                "created_at": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
            })

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