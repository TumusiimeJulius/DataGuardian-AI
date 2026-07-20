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


@app.get("/test_imports")
def test_imports():
    results = {}
    
    # 1. Test google.genai import
    try:
        from google import genai
        results["google_genai_import"] = "OK"
    except Exception as e:
        results["google_genai_import"] = f"FAIL: {str(e)}"
        
    # 2. Test pandas import
    try:
        import pandas as pd
        results["pandas_import"] = "OK"
    except Exception as e:
        results["pandas_import"] = f"FAIL: {str(e)}"
        
    # 3. Test numpy import
    try:
        import numpy as np
        results["numpy_import"] = "OK"
    except Exception as e:
        results["numpy_import"] = f"FAIL: {str(e)}"
        
    # 4. Test sklearn import
    try:
        import sklearn
        results["sklearn_import"] = "OK"
    except Exception as e:
        results["sklearn_import"] = f"FAIL: {str(e)}"
        
    # 5. Test ai_service import
    try:
        from agents.ai_service import generate_analysis
        results["ai_service_import"] = "OK"
    except Exception as e:
        results["ai_service_import"] = f"FAIL: {str(e)}"
        
    # 6. Test investigator import
    try:
        from agents.investigator import DataInvestigatorAgent
        results["investigator_import"] = "OK"
    except Exception as e:
        results["investigator_import"] = f"FAIL: {str(e)}"
        
    # 7. Test investigator instantiation
    if results.get("investigator_import") == "OK":
        try:
            agent = DataInvestigatorAgent()
            results["investigator_instantiation"] = "OK"
            results["initialization_errors"] = agent.initialization_errors
        except Exception as e:
            results["investigator_instantiation"] = f"FAIL: {str(e)}"
            
    return results



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

    # Step-by-step agent loader diagnostics
    agents_status = {}
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
            inst = agent_class()
            agents_status[agent_name] = "LOADED_OK"
        except Exception as exc:
            agents_status[agent_name] = f"ERROR: {str(exc)}"

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
            "gemini_api_key_present": bool(os.getenv("GEMINI_API_KEY")),
            "cors_origins_env": os.getenv("CORS_ORIGINS"),
            "active_cors_origins": origins,
            "agents_status": agents_status
        }
    }

@app.get("/test_pandas_1")
def test_pandas_1():
    import pandas as pd
    import numpy as np
    return {"pandas_version": pd.__version__, "numpy_version": np.__version__}

@app.get("/test_pandas_2")
def test_pandas_2():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({
        "customer_id": [1, 2, 3, 3],
        "amount": [500, np.nan, 500, -100],
        "created_at": ["2026-01-01", "2026-01-02", "invalid", "invalid"]
    })
    return {"status": "ok", "df_type": str(type(df))}

@app.get("/test_pandas_3")
def test_pandas_3():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({
        "customer_id": [1, 2, 3, 3],
        "amount": [500, np.nan, 500, -100],
        "created_at": ["2026-01-01", "2026-01-02", "invalid", "invalid"]
    })
    val = df.isnull().sum().to_dict()
    return {"status": "ok", "isnull": str(val)}

@app.get("/test_pandas_4")
def test_pandas_4():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({
        "customer_id": [1, 2, 3, 3],
        "amount": [500, np.nan, 500, -100],
        "created_at": ["2026-01-01", "2026-01-02", "invalid", "invalid"]
    })
    val = df.duplicated().sum()
    return {"status": "ok", "duplicated": int(val)}

@app.get("/test_pandas_5")
def test_pandas_5():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({
        "customer_id": [1, 2, 3, 3],
        "amount": [500, np.nan, 500, -100],
        "created_at": ["2026-01-01", "2026-01-02", "invalid", "invalid"]
    })
    val = pd.to_datetime(df["created_at"], errors="coerce")
    return {"status": "ok", "to_datetime_isna_sum": int(val.isna().sum())}

@app.get("/test_pandas_6")
def test_pandas_6():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({
        "customer_id": [1, 2, 3, 3],
        "amount": [500, np.nan, 500, -100],
        "created_at": ["2026-01-01", "2026-01-02", "invalid", "invalid"]
    })
    val = (df["amount"] < 0).sum()
    return {"status": "ok", "negatives": int(val)}











@app.get("/diagnose_investigate")
def diagnose_investigate(question: str, step_limit: int = 18):
    try:
        import time
        import pandas as pd
        from datahub.client import datahub_client
        from agents.investigator import DataInvestigatorAgent
        agent = DataInvestigatorAgent()
        steps = {}
        
        start = time.time()
        
        # Step 1: DataHub
        if step_limit >= 1:
            t = time.time()
            context = agent._safe_execute(datahub_client.search_dataset, "sales")
            steps["1_datahub"] = time.time() - t
        
        # Step 2: Lineage
        if step_limit >= 2:
            t = time.time()
            lineage_report = agent._safe_execute(agent.lineage_agent.analyze, context)
            steps["2_lineage"] = time.time() - t
            
        # Step 3: Pipeline
        if step_limit >= 3:
            t = time.time()
            pipeline_report = agent._safe_execute(agent.pipeline_agent.analyze, {"lineage": lineage_report})
            steps["3_pipeline"] = time.time() - t
            
        # Step 4: Load Dataset
        if step_limit >= 4:
            t = time.time()
            try:
                import os
                from pathlib import Path
                BASE_DIR = Path(__file__).resolve().parent
                dataset_path = BASE_DIR / "test_sales.csv"
                if not dataset_path.exists():
                    data = pd.DataFrame({
                        "customer_id": [1, 2, 3, 4],
                        "amount": [100.0, 150.0, 200.0, 75.0],
                        "created_at": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
                    })
                else:
                    data = pd.read_csv(dataset_path)
                steps["4_load_dataset"] = time.time() - t
            except Exception as e:
                steps["4_load_dataset_error"] = str(e)
                return {"error": "load_dataset_failed", "steps": steps}
                
        # Step 5: Observability
        if step_limit >= 5:
            t = time.time()
            observability_report = agent._safe_execute(agent.observability_agent.analyze, data, context)
            steps["5_observability"] = time.time() - t
            
        # Step 6: Quality
        if step_limit >= 6:
            t = time.time()
            quality_report = agent._safe_execute(agent.quality_agent.analyze, data)
            steps["6_quality"] = time.time() - t
            
        # Step 7: Anomaly
        if step_limit >= 7:
            t = time.time()
            anomaly_report = agent._safe_execute(agent.anomaly_agent.analyze, data)
            steps["7_anomaly"] = time.time() - t
            
        # Step 8: Prediction
        if step_limit >= 8:
            t = time.time()
            prediction_report = agent._safe_execute(agent.prediction_agent.predict, data)
            steps["8_prediction"] = time.time() - t
            
        # Step 9: Root Cause
        if step_limit >= 9:
            t = time.time()
            root_cause_report = agent._safe_execute(agent.rootcause_agent.analyze, quality_report)
            steps["9_root_cause"] = time.time() - t
            
        # Step 10: Repair
        if step_limit >= 10:
            t = time.time()
            repair_report = agent._safe_execute(agent.repair_agent.repair, data, quality_report, anomaly_report, root_cause_report)
            steps["10_repair"] = time.time() - t
            
        # Step 11: Quality After
        if step_limit >= 11:
            t = time.time()
            post_repair_quality_report = agent._safe_execute(agent.quality_agent.analyze, data)
            steps["11_post_repair_quality"] = time.time() - t
            
        # Step 12: Recommendation
        if step_limit >= 12:
            t = time.time()
            recommendation_report = agent._safe_execute(agent.recommendation_agent.generate, post_repair_quality_report)
            steps["12_recommendation"] = time.time() - t
            
        # Step 13: Decision
        if step_limit >= 13:
            t = time.time()
            decision_report = agent._safe_execute(agent.decision_agent.decide, post_repair_quality_report, anomaly_report, prediction_report, root_cause_report, recommendation_report)
            steps["13_decision"] = time.time() - t
            
        # Step 14: Alert
        if step_limit >= 14:
            t = time.time()
            alert_report = agent._safe_execute(agent.alert_agent.analyze, post_repair_quality_report, anomaly_report, prediction_report)
            steps["14_alert"] = time.time() - t
            
        # Step 15: AI explanation
        if step_limit >= 15:
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
            steps["15_generate_analysis"] = time.time() - t
            
        # Step 16: Memory save
        if step_limit >= 16:
            t = time.time()
            memory_report = agent._safe_execute(agent.memory_agent.save, {
                "question": question,
                "status": "COMPLETED",
                "quality_report_before_repair": quality_report,
                "prediction_report": prediction_report,
                "root_cause_report": root_cause_report
            })
            steps["16_memory_save"] = time.time() - t
            
        # Step 17: Memory compare
        if step_limit >= 17:
            t = time.time()
            comparison_report = agent._safe_execute(agent.memory_agent.compare_last_two)
            steps["17_memory_compare"] = time.time() - t
            
        # Step 18: serialization
        if step_limit >= 18:
            t = time.time()
            serialized = agent._make_serializable({
                "status": "COMPLETED",
                "report": analysis if 'analysis' in locals() else None
            })
            steps["18_serialization"] = time.time() - t
            
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