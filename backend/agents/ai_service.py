import os
from datetime import datetime

try:
    from google import genai
except Exception:
    genai = None


# ==========================================
# Gemini Configuration
# ==========================================

API_KEY = os.getenv("GEMINI_API_KEY")


# ==========================================
# Local AI Fallback
# ==========================================

def local_analysis(question, context):

    return {
        "type": "LOCAL_AI_ANALYSIS",
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "summary": "Gemini AI is unavailable. DataGuardian AI generated a local investigation report.",
        "findings": context,
        "recommendation": (
            "Configure GEMINI_API_KEY on the deployment platform "
            "to enable AI-generated explanations."
        )
    }


# ==========================================
# Gemini Analysis
# ==========================================

def generate_analysis(question, context):

    if not API_KEY:
        return local_analysis(question, context)

    if genai is None:
        return local_analysis(question, context)

    try:

        client = genai.Client(api_key=API_KEY)

        prompt = f"""
You are DataGuardian AI.

Investigate this dataset.

Question:
{question}

Evidence:
{context}

Produce:

1. Executive Summary
2. Root Cause Analysis
3. Data Quality Issues
4. Repair Actions
5. Business Impact
6. Recommendations
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return {
            "type": "GEMINI_ANALYSIS",
            "timestamp": datetime.now().isoformat(),
            "result": response.text,
        }

    except Exception as e:

        print("Gemini Error:", str(e))

        return {
            **local_analysis(question, context),
            "gemini_error": str(e),
        }