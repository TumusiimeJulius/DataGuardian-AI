import sys
import os

# Only enable file logging in development environments
if os.getenv("ENVIRONMENT") != "production":
    try:
        sys.stdout = open("stdout.log", "a", encoding="utf-8", buffering=1)
        sys.stderr = open("stderr.log", "a", encoding="utf-8", buffering=1)
        print("\n--- SERVER START / RESTART ---")
    except Exception as e:
        # Silently fail if logging setup fails (e.g., on Render's ephemeral FS)
        pass

from dotenv import load_dotenv
load_dotenv()




from fastapi import APIRouter, FastAPI

from fastapi.middleware.cors import CORSMiddleware





# ========================================
# Database
# ========================================


from database import engine

from models import Base





# ========================================
# Create Database Tables
# ========================================


Base.metadata.create_all(
    bind=engine
)








# ========================================
# Import API Routes
# ========================================


def _import_router(module_name: str, router_name: str):
    try:
        module = __import__(module_name, fromlist=[router_name])
        return getattr(module, router_name)
    except Exception as exc:
        print(f"WARNING: failed to import {module_name}: {exc}")
        return APIRouter()


main_router = _import_router("api.routes", "router")
agent_router = _import_router("api.agent_routes", "router")
dashboard_router = _import_router("api.dashboard_routes", "router")
websocket_router = _import_router("api.websocket_routes", "router")
upload_router = _import_router("api.upload_routes", "router")
history_router = _import_router("api.history_routes", "router")
download_router = _import_router("api.download_routes", "router")
analytics_router = _import_router("api.analytics_routes", "router")







# ========================================
# FastAPI Application
# ========================================


app = FastAPI(


    title="DataGuardian AI",


    description="""


    Autonomous AI Data Quality Intelligence Platform.


    Features:


    ✓ Dataset Upload

    ✓ AI Dataset Investigation

    ✓ Data Quality Scoring

    ✓ Missing Value Detection

    ✓ Duplicate Detection

    ✓ ML Anomaly Detection

    ✓ Root Cause Analysis

    ✓ Automatic Dataset Repair

    ✓ Clean Dataset Export

    ✓ Investigation History

    ✓ AI Agent Monitoring

    ✓ Analytics Intelligence



    """,



    version="2.3.0"

)









# ========================================
# CORS Configuration
# ========================================
import os

cors_origins_env = os.getenv("CORS_ORIGINS")
if cors_origins_env:
    origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
else:
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "https://data-guardianai.vercel.app"
    ]




app.add_middleware(


    CORSMiddleware,


    allow_origins=origins,


    allow_credentials=True,


    allow_methods=["*"],


    allow_headers=["*"]

)









# ========================================
# Register API Routes
# ========================================



# General Routes

app.include_router(
    main_router
)




# AI Agents

app.include_router(
    agent_router
)




# Dashboard

app.include_router(
    dashboard_router
)





# Real-Time WebSocket

app.include_router(
    websocket_router
)





# Dataset Upload Pipeline

app.include_router(
    upload_router
)





# Dataset History

app.include_router(
    history_router
)





# Clean Dataset Download

app.include_router(
    download_router
)





# Analytics

app.include_router(
    analytics_router
)


# ========================================
# Global Exception Handler
# ========================================

from fastapi.responses import JSONResponse
from fastapi import Request

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    error_trace = traceback.format_exc()
    print(f"Unhandled exception: {error_trace}", file=sys.stderr)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc),
            "type": type(exc).__name__
        }
    )







# ========================================
# Test Endpoint (for debugging)
# ========================================

@app.get("/test")
def test_endpoint():
    return {"status": "ok", "message": "Backend is running"}


@app.get("/agent_health")
def agent_health():
    """Check if all agents can be initialized"""
    try:
        from agents.investigator import DataInvestigatorAgent
        agent = DataInvestigatorAgent()
        
        if agent.initialization_errors:
            return {
                "status": "degraded",
                "message": f"{len(agent.initialization_errors)} agent(s) failed",
                "errors": agent.initialization_errors
            }
        else:
            return {
                "status": "healthy",
                "message": "All agents initialized successfully",
                "agents_count": 12
            }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "type": type(e).__name__
        }


# ========================================
# Root Endpoint
# ========================================


@app.get("/")
def home():


    return {


        "project":

        "DataGuardian AI",



        "status":

        "ONLINE",



        "version":

        "2.3.0",



        "description":

        "Autonomous AI-powered data quality intelligence platform",



        "backend":

        "http://127.0.0.1:8000",



        "frontend":

        "http://localhost:5173",



        "websocket":

        "ws://127.0.0.1:8000/ws/dashboard",



        "database":

        "SQLite Investigation Archive",






        "pipeline":[



            "Dataset Upload",


            "AI Investigation",


            "Quality Analysis",


            "Anomaly Detection",


            "Root Cause Analysis",


            "Automatic Repair",


            "Recommendation Generation",


            "History Storage",


            "Analytics Intelligence",


            "Clean Dataset Export"



        ],







        "ai_agents":[


            "Data Investigator Agent",


            "Data Quality Agent",


            "Anomaly Detection Agent",


            "Root Cause Agent",


            "Repair Agent",


            "Recommendation Agent",


            "Prediction Agent",


            "Memory Agent"



        ],







        "api_endpoints":[



            "/upload",


            "/history",


            "/download/{filename}",


            "/agents",


            "/analytics",


            "/dashboard/overview",


            "/ws/dashboard",


            "/health"



        ]



    }









# ========================================
# Health Check
# ========================================


@app.get("/health")
def health():
    import importlib
    genai_legacy_available = False
    genai_new_available = False
    try:
        importlib.import_module("google.generativeai")
        genai_legacy_available = True
    except ImportError:
        pass
    try:
        importlib.import_module("google.genai")
        genai_new_available = True
    except ImportError:
        pass

    return {
        "application": "DataGuardian AI",
        "status": "healthy",
        "database": "SQLite connected",
        "ai_pipeline": "active",
        "analytics": "enabled",
        "agents": "running",
        "diagnostics": {
            "google_generativeai_installed": genai_legacy_available,
            "google_genai_installed": genai_new_available,
            "gemini_api_key_present": bool(os.getenv("GEMINI_API_KEY"))
        }
    }










@app.get("/debug_investigate")
def debug_investigate(question: str):
    try:
        import time
        import pandas as pd
        from datahub.client import datahub_client
        from agents.investigator import DataInvestigatorAgent
        agent = DataInvestigatorAgent()
        steps = {}
        
        start = time.time()
        
        # Step 1
        t = time.time()
        context = agent._safe_execute(datahub_client.search_dataset, "sales")
        steps["datahub"] = time.time() - t
        
        # Step 2
        t = time.time()
        lineage_report = agent._safe_execute(agent.lineage_agent.analyze, context)
        steps["lineage"] = time.time() - t
        
        # Step 3
        t = time.time()
        pipeline_report = agent._safe_execute(agent.pipeline_agent.analyze, {"lineage": lineage_report})
        steps["pipeline"] = time.time() - t
        
        # Step 4
        t = time.time()
        try:
            data = pd.read_csv("test_sales.csv")
            steps["load_dataset"] = time.time() - t
        except Exception as e:
            steps["load_dataset_error"] = str(e)
            return {"error": "load_dataset_failed", "steps": steps}
            
        # Step 5
        t = time.time()
        observability_report = agent._safe_execute(agent.observability_agent.analyze, data, context)
        steps["observability"] = time.time() - t
        
        # Step 6
        t = time.time()
        quality_report = agent._safe_execute(agent.quality_agent.analyze, data)
        steps["quality"] = time.time() - t
        
        # Step 7
        t = time.time()
        anomaly_report = agent._safe_execute(agent.anomaly_agent.analyze, data)
        steps["anomaly"] = time.time() - t
        
        # Step 8
        t = time.time()
        prediction_report = agent._safe_execute(agent.prediction_agent.predict, data)
        steps["prediction"] = time.time() - t
        
        # Step 9
        t = time.time()
        root_cause_report = agent._safe_execute(agent.rootcause_agent.analyze, quality_report)
        steps["root_cause"] = time.time() - t
        
        # Step 10
        t = time.time()
        repair_report = agent._safe_execute(agent.repair_agent.repair, data, quality_report, anomaly_report, root_cause_report)
        steps["repair"] = time.time() - t
        
        # Step 11
        t = time.time()
        post_repair_quality_report = agent._safe_execute(agent.quality_agent.analyze, data)
        steps["post_repair_quality"] = time.time() - t
        
        # Step 12
        t = time.time()
        recommendation_report = agent._safe_execute(agent.recommendation_agent.generate, post_repair_quality_report)
        steps["recommendation"] = time.time() - t
        
        # Step 13
        t = time.time()
        decision_report = agent._safe_execute(agent.decision_agent.decide, post_repair_quality_report, anomaly_report, prediction_report, root_cause_report, recommendation_report)
        steps["decision"] = time.time() - t
        
        # Step 14
        t = time.time()
        alert_report = agent._safe_execute(agent.alert_agent.analyze, post_repair_quality_report, anomaly_report, prediction_report)
        steps["alert"] = time.time() - t
        
        # Step 15
        t = time.time()
        from agents.ai_service import generate_analysis
        analysis = agent._safe_execute(generate_analysis, question, {
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
        })
        steps["generate_analysis"] = time.time() - t
        
        # Step 16
        t = time.time()
        memory_report = agent._safe_execute(agent.memory_agent.save, {
            "question": question,
            "status": "COMPLETED",
            "quality_report_before_repair": quality_report,
            "prediction_report": prediction_report,
            "root_cause_report": root_cause_report
        })
        steps["memory_save"] = time.time() - t
        
        # Step 17
        t = time.time()
        comparison_report = agent._safe_execute(agent.memory_agent.compare_last_two)
        steps["memory_compare"] = time.time() - t
        
        steps["total"] = time.time() - start
        return {"status": "success", "steps": steps}
    
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }


@app.get("/debug_logs")
def debug_logs():
    stdout_content = ""
    stderr_content = ""
    if os.path.exists("stdout.log"):
        with open("stdout.log", "r", encoding="utf-8", errors="ignore") as f:
            stdout_content = f.read()[-8000:]
    if os.path.exists("stderr.log"):
        with open("stderr.log", "r", encoding="utf-8", errors="ignore") as f:
            stderr_content = f.read()[-8000:]
    return {
        "stdout": stdout_content,
        "stderr": stderr_content
    }


# ========================================
# Startup Event
# ========================================




@app.on_event("startup")
def startup_event():


    print(
"""
===================================
 DataGuardian AI Started
===================================

Backend:
http://127.0.0.1:8000


API Docs:
http://127.0.0.1:8000/docs


Frontend:
http://localhost:5173


Available Services:

[x] Upload API
[x] AI Analysis
[x] Repair Engine
[x] History Database
[x] Analytics Engine
[x] AI Agents
[x] WebSocket Monitoring


Status:
ONLINE

===================================
"""
)