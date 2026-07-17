from dotenv import load_dotenv


# ========================================
# Load Environment Variables
# ========================================

load_dotenv()



from fastapi import FastAPI

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


from api.routes import router as main_router


from api.agent_routes import router as agent_router


from api.dashboard_routes import router as dashboard_router


from api.websocket_routes import router as websocket_router


from api.upload_routes import router as upload_router


from api.history_routes import router as history_router


from api.download_routes import router as download_router


from api.analytics_routes import router as analytics_router







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