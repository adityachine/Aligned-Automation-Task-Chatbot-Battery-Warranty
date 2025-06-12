# ts_notes_processor.py

import openai
import os

# Set your OpenAI key (ensure it's in your environment or use dotenv)
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_ts_notes(ts_notes):
    """
    Use OpenAI GPT to analyze TS Notes and extract useful diagnostics or keyword insights.
    """

    prompt = f"""
    You are a diagnostic assistant working on a technical support automation system.
    Analyze the following TS Notes and extract:

    1. Keywords related to hardware or battery issues.
    2. Whether this sounds like a known issue that should be escalated.
    3. Suggest a rule (1 to 6) if you think it applies.
    4. Mention if it's related to battery or not.

    TS Notes:
    \"\"\"{ts_notes}\"\"\"
    Provide your output in this JSON format:
    {{
        "keywords": [],
        "is_battery_related": true/false,
        "recommend_rule": "Rule 1/2/3/4/5/6/None",
        "needs_escalation": true/false
    }}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a technical support expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        content = response['choices'][0]['message']['content']
        return content
    except Exception as e:
        return str(e)
