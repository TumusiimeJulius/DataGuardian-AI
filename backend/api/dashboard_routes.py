from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/agents")
def agents():

    now = datetime.now().isoformat()

    return {
        "agents": [
            {
                "name": "Data Investigator",
                "status": "Running",
                "health": "Healthy",
                "last_execution": now,
                "description": "Coordinates AI investigations."
            },
            {
                "name": "Pipeline Monitoring",
                "status": "Running",
                "health": "Healthy",
                "last_execution": now,
                "description": "Monitors ETL pipelines."
            },
            {
                "name": "Repair Agent",
                "status": "Running",
                "health": "Healthy",
                "last_execution": now,
                "description": "Repairs data quality issues."
            },
            {
                "name": "Data Quality Agent",
                "status": "Running",
                "health": "Healthy",
                "last_execution": now,
                "description": "Checks dataset quality."
            },
            {
                "name": "Root Cause Agent",
                "status": "Running",
                "health": "Healthy",
                "last_execution": now,
                "description": "Performs root cause analysis."
            },
            {
                "name": "Anomaly Detection Agent",
                "status": "Running",
                "health": "Healthy",
                "last_execution": now,
                "description": "Detects anomalies."
            },
            {
                "name": "Prediction Agent",
                "status": "Running",
                "health": "Healthy",
                "last_execution": now,
                "description": "Predicts future risks."
            },
            {
                "name": "Recommendation Agent",
                "status": "Running",
                "health": "Healthy",
                "last_execution": now,
                "description": "Suggests corrective actions."
            },
            {
                "name": "Alert Monitoring Agent",
                "status": "Running",
                "health": "Healthy",
                "last_execution": now,
                "description": "Monitors alerts."
            },
            {
                "name": "Memory Agent",
                "status": "Running",
                "health": "Healthy",
                "last_execution": now,
                "description": "Stores investigation history."
            }
        ]
    }