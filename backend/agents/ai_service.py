import os
from datetime import datetime

try:
    import google.generativeai as genai
except Exception:
    genai = None



# ----------------------------------------
# Gemini Configuration
# ----------------------------------------

API_KEY = os.getenv("GEMINI_API_KEY")


if genai and API_KEY:

    genai.configure(
        api_key=API_KEY
    )


# ----------------------------------------
# Local AI Fallback
# ----------------------------------------

def local_analysis(question, context):

    quality = context.get(
        "quality",
        {}
    )

    repair = context.get(
        "repair",
        {}
    )

    anomalies = context.get(
        "anomalies",
        {}
    )


    return {


        "type": "LOCAL_AI_ANALYSIS",


        "timestamp": datetime.now().isoformat(),


        "question": question,


        "summary":

            "DataGuardian AI completed an automated investigation using internal agents.",



        "findings": {


            "data_quality":

                quality,


            "detected_anomalies":

                anomalies,


            "repair_actions":

                repair

        },



        "recommendation":

            "Review detected data quality problems, apply repair actions, and monitor future pipeline executions."

    }



# ----------------------------------------
# Gemini AI Analysis
# ----------------------------------------

def generate_analysis(question, context):


    try:


        if not genai or not API_KEY:

            return local_analysis(

                question,

                context

            )



        model = genai.GenerativeModel(

            "gemini-2.0-flash-lite"

        )


        prompt = f"""

You are DataGuardian AI.

Investigate this data problem:

{question}


Use this evidence:

{context}


Provide:

1. Root cause
2. Data problems
3. Repair actions
4. Recommendations
5. Business impact

"""



        response = model.generate_content(

            prompt

        )


        return {


            "type": "GEMINI_ANALYSIS",


            "result": response.text,


            "timestamp":

                datetime.now().isoformat()

        }



    except Exception as e:


        print(
            "GEMINI FAILED, USING LOCAL AI:",
            str(e)
        )


        return local_analysis(

            question,

            context

        )