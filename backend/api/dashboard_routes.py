from fastapi import APIRouter
from datetime import datetime


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)



# =========================================
# Dashboard Overview
# =========================================

@router.get("/overview")
def dashboard_overview():

    now = datetime.now().isoformat()


    return {

        "status": "ONLINE",

        "timestamp": now,


        "metrics": {


            "datasets_processed": 0,


            "quality_average": 0,


            "anomalies_detected": 0,


            "repairs_completed": 0,


            "active_agents": 10


        },


        "system": {


            "database":
            "SQLite Connected",


            "ai_engine":
            "Gemini AI Active",


            "pipeline":
            "Running"


        }


    }







# =========================================
# AI Agents Status
# =========================================

@router.get("/agents")
def agents():


    now = datetime.now().isoformat()


    return {


        "agents":[



            {
                "name":"Data Investigator Agent",
                "status":"Running",
                "health":"Healthy",
                "last_execution":now,
                "description":
                "Coordinates AI investigations."
            },



            {
                "name":"Pipeline Monitoring Agent",
                "status":"Running",
                "health":"Healthy",
                "last_execution":now,
                "description":
                "Monitors ETL pipelines."
            },



            {
                "name":"Data Quality Agent",
                "status":"Running",
                "health":"Healthy",
                "last_execution":now,
                "description":
                "Calculates data quality metrics."
            },



            {
                "name":"Anomaly Detection Agent",
                "status":"Running",
                "health":"Healthy",
                "last_execution":now,
                "description":
                "Detects unusual patterns."
            },



            {
                "name":"Root Cause Agent",
                "status":"Running",
                "health":"Healthy",
                "last_execution":now,
                "description":
                "Finds causes of data problems."
            },



            {
                "name":"Repair Agent",
                "status":"Running",
                "health":"Healthy",
                "last_execution":now,
                "description":
                "Creates clean datasets."
            },



            {
                "name":"Recommendation Agent",
                "status":"Running",
                "health":"Healthy",
                "last_execution":now,
                "description":
                "Generates improvement suggestions."
            },



            {
                "name":"Prediction Agent",
                "status":"Running",
                "health":"Healthy",
                "last_execution":now,
                "description":
                "Predicts future data risks."
            },



            {
                "name":"Alert Monitoring Agent",
                "status":"Running",
                "health":"Healthy",
                "last_execution":now,
                "description":
                "Monitors system alerts."
            },



            {
                "name":"Memory Agent",
                "status":"Running",
                "health":"Healthy",
                "last_execution":now,
                "description":
                "Stores investigation history."
            }


        ]

    }