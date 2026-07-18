from fastapi import APIRouter
from datetime import datetime


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)



# ==========================================
# Dashboard Overview
# ==========================================

@router.get("/overview")
def dashboard_overview():

    now = datetime.now().isoformat()


    return {


        "status": "ONLINE",


        "timestamp": now,


        "system": {

            "application":
            "DataGuardian AI",

            "pipeline":
            "ACTIVE",

            "database":
            "SQLite Connected",

            "analytics":
            "Enabled"

        },



        "metrics": {


            "datasets_processed":

            0,


            "quality_score":

            0,


            "anomalies_detected":

            0,


            "repairs_completed":

            0


        },



        "agents": {


            "total":

            10,


            "active":

            10,


            "failed":

            0


        }



    }







# ==========================================
# AI Agents Status
# ==========================================

@router.get("/agents")
def agents():


    now = datetime.now().isoformat()


    return {


        "agents": [



            {

                "name":
                "Data Investigator Agent",

                "status":
                "Running",

                "health":
                "Healthy",

                "last_execution":
                now,

                "description":
                "Coordinates AI investigations."

            },



            {

                "name":
                "Pipeline Monitoring Agent",

                "status":
                "Running",

                "health":
                "Healthy",

                "last_execution":
                now,

                "description":
                "Monitors ETL pipelines."

            },



            {

                "name":
                "Repair Agent",

                "status":
                "Running",

                "health":
                "Healthy",

                "last_execution":
                now,

                "description":
                "Automatically repairs corrupted datasets."

            },



            {

                "name":
                "Data Quality Agent",

                "status":
                "Running",

                "health":
                "Healthy",

                "last_execution":
                now,

                "description":
                "Calculates dataset quality scores."

            },



            {

                "name":
                "Root Cause Agent",

                "status":
                "Running",

                "health":
                "Healthy",

                "last_execution":
                now,

                "description":
                "Finds causes of data problems."

            },



            {

                "name":
                "Anomaly Detection Agent",

                "status":
                "Running",

                "health":
                "Healthy",

                "last_execution":
                now,

                "description":
                "Detects unusual data patterns."

            },



            {

                "name":
                "Prediction Agent",

                "status":
                "Running",

                "health":
                "Healthy",

                "last_execution":
                now,

                "description":
                "Predicts future data risks."

            },



            {

                "name":
                "Recommendation Agent",

                "status":
                "Running",

                "health":
                "Healthy",

                "last_execution":
                now,

                "description":
                "Generates improvement recommendations."

            },



            {

                "name":
                "Alert Monitoring Agent",

                "status":
                "Running",

                "health":
                "Healthy",

                "last_execution":
                now,

                "description":
                "Monitors system alerts."

            },



            {

                "name":
                "Memory Agent",

                "status":
                "Running",

                "health":
                "Healthy",

                "last_execution":
                now,

                "description":
                "Stores investigation history."

            }



        ]

    }