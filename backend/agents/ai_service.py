import os
from datetime import datetime

try:
    from google import genai
except ImportError:
    genai = None


# ==========================================
# Gemini Configuration
# ==========================================

API_KEY = os.getenv("GEMINI_API_KEY")


# ==========================================
# Local AI Fallback
# ==========================================

def local_analysis(question, context, error=None):
    return {
        "type": "LOCAL_AI_ANALYSIS",
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "summary": (
            "Gemini AI is unavailable. "
            "DataGuardian AI generated a local investigation report."
        ),
        "findings": context,
        "recommendation": (
            "Configure the GEMINI_API_KEY and ensure the "
            "google-genai package is installed."
        ),
        "gemini_error": error,
    }


# ==========================================
# Gemini AI Analysis
# ==========================================

def generate_analysis(question, context):

    if os.getenv("ENVIRONMENT") == "production" or os.getenv("SKIP_EXTERNAL_AI", "0").lower() in {"1", "true", "yes", "on"}:
        return local_analysis(
            question,
            context,
            "External AI generation is disabled in this environment."
        )

    # API key missing
    if not API_KEY:
        return local_analysis(
            question,
            context,
            "GEMINI_API_KEY is not configured."
        )

    # SDK missing
    if genai is None:
        return local_analysis(
            question,
            context,
            "google-genai SDK is not installed."
        )

    try:

        client = genai.Client(
            api_key=API_KEY
        )

        prompt = f"""
You are DataGuardian AI, an autonomous AI platform for data quality analysis.

Investigate the following dataset.

Question:
{question}

Evidence:
{context}

Generate a professional investigation report containing:

1. Executive Summary
2. Root Cause Analysis
3. Data Quality Issues
4. Repair Actions Performed
5. Business Impact
6. Recommendations
7. Overall Quality Assessment

Respond in clear professional English.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        text = ""

        if hasattr(response, "text") and response.text:
            text = response.text
        elif (
            hasattr(response, "candidates")
            and response.candidates
            and response.candidates[0].content.parts
        ):
            text = response.candidates[0].content.parts[0].text

        if not text:
            raise Exception("Gemini returned an empty response.")

        return {
            "type": "GEMINI_ANALYSIS",
            "timestamp": datetime.now().isoformat(),
            "model": "gemini-2.5-flash",
            "result": text,
        }

    except Exception as e:

        print("=" * 60)
        print("GEMINI ERROR")
        print(str(e))
        print("=" * 60)

        return local_analysis(
            question,
            context,
            str(e)
        )