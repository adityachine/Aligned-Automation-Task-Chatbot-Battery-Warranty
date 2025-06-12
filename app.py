# main.py

import streamlit as st
from logic.excel_reader import load_excel_data
from logic.decision_engine import process_case
from llm.ts_notes_processor import analyze_ts_notes
from ui.helpers import keyword_match_in_notes, is_battery_part
import json
import os
api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Tech Direct Chatbot", layout="centered")

# Styling and fonts
st.markdown("""
    <style>
    body {
        background-color: #D8F0FF;
        font-family: 'Lato', sans-serif;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.title("🤖 Tech Direct Chatbot")
st.markdown("Upload your Excel file and start processing the Tech Direct Battery Warranty flow.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = load_excel_data(uploaded_file)
        st.success(f"Loaded {len(df)} cases from the Excel file!")
        
        # Show preview
        st.dataframe(df.head(10))

        # Process button
        if st.button("Process Cases"):
            st.session_state.messages.append({"role": "system", "content": "Processing cases..."})

            for idx, row in df.iterrows():
                case_data = row.to_dict()
                
                # Run flow rules
                decision, matched_rules = process_case(case_data)

                # Analyze TS Notes with OpenAI LLM
                ts_notes = case_data.get("TS Notes", "")
                analysis_result_raw = analyze_ts_notes(ts_notes)
                try:
                    analysis_result = json.loads(analysis_result_raw)
                except:
                    analysis_result = {"error": "Could not parse analysis output."}

                # Build message
                message_text = (
                    f"Case ID: {case_data.get('Case ID', idx)}\n"
                    f"Decision: {decision}\n"
                    f"Matched Rules: {matched_rules}\n"
                    f"TS Notes Analysis: {analysis_result}"
                )

                st.session_state.messages.append({"role": "assistant", "content": message_text})

            st.experimental_rerun()

    except Exception as e:
        st.error(f"Error loading or processing Excel file: {e}")

# Display chat messages
for i, msg in enumerate(st.session_state.messages):
    is_user = msg["role"] == "user"
    st.markdown(f"**{'You' if is_user else 'Bot'}:** {msg['content']}")
