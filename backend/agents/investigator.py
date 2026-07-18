from datetime import datetime
from pathlib import Path
import traceback
import time
import sys

try:
    import pandas as pd
except Exception:
    pd = None

from datahub.client import datahub_client
from agents.ai_service import generate_analysis

import importlib

# Note: agent modules are imported dynamically inside the initializer
# to avoid hard failures at module import time in constrained production
# environments (this prevents the whole app from crashing if a single
# agent has an import-time error).


class DataInvestigatorAgent:

    def __init__(self):

        self.name = "Data Investigator Agent"
        self.initialization_errors = []

        # Initialize agents with error tracking using dynamic imports
        agents_to_init = [
            ('quality_agent', 'agents.quality_agent', 'DataQualityAgent'),
            ('recommendation_agent', 'agents.recommendation_agent', 'RecommendationAgent'),
            ('rootcause_agent', 'agents.rootcause_agent', 'RootCauseAgent'),
            ('lineage_agent', 'agents.lineage_agent', 'LineageAgent'),
            ('anomaly_agent', 'agents.anomaly_agent', 'AnomalyDetectionAgent'),
            ('prediction_agent', 'agents.prediction_agent', 'PredictionAgent'),
            ('decision_agent', 'agents.decision_agent', 'DecisionAgent'),
            ('memory_agent', 'agents.memory_agent', 'MemoryAuditAgent'),
            ('alert_agent', 'agents.alert_agent', 'AlertMonitoringAgent'),
            ('observability_agent', 'agents.observability_agent', 'DataObservabilityAgent'),
            ('pipeline_agent', 'agents.pipeline_agent', 'PipelineMonitoringAgent'),
            ('repair_agent', 'agents.repair_agent', 'RepairAgent'),
        ]

        for agent_name, module_path, class_name in agents_to_init:
            try:
                module = importlib.import_module(module_path)
                agent_class = getattr(module, class_name)
                setattr(self, agent_name, agent_class())
            except Exception as e:
                self.initialization_errors.append({
                    'agent': agent_name,
                    'module': module_path,
                    'class': class_name,
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

            if pd is None:
                print("[INVESTIGATE] pandas unavailable; using fallback mock dataset", file=sys.stderr)
                data = {
                    "customer_id": [1, 2, 3, 4],
                    "amount": [100.0, 150.0, 200.0, 75.0],
                    "created_at": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
                }
            elif not dataset_path.exists():
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
            data = None

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

        # Ensure all data is JSON serializable
        investigation = self._make_serializable(investigation)
        return investigation

    def _make_serializable(self, obj):
        """Convert non-JSON-serializable objects to strings recursively"""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif hasattr(obj, '__dict__'):
            # Convert objects to dictionaries
            return str(obj)
        else:
            try:
                return str(obj)
            except:
                return f"<non-serializable: {type(obj).__name__}>"