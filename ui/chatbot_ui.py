import streamlit as st
from streamlit_chat import message
import pandas as pd
import openai

# --- CONFIG ---
st.set_page_config(page_title="Tech Direct Chatbot", layout="wide")
st.title("🤖 Tech Direct Chatbot")

# --- API Key Input ---
with st.sidebar:
    st.subheader("🔐 API Key")
    openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
    csv_file = st.file_uploader("Upload Battery CSV", type=["csv"])

# --- Load Battery Data ---
battery_data = None
if csv_file:
    battery_data = pd.read_csv(csv_file)

# --- Style ---
st.markdown("""
    <style>
    body, .main { background-color: #f0f4f8 !important; font-family: 'Segoe UI', sans-serif; }
    .chat-box { background-color: #ffffff; border-radius: 10px; padding: 20px; min-height: 400px; }
    </style>
""", unsafe_allow_html=True)

# --- Chat State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Helper: CSV Search ---
def search_csv(user_input):
    if battery_data is None:
        return None
    matches = battery_data[battery_data['Issue'].str.contains(user_input, case=False, na=False)]
    if not matches.empty:
        recs = matches['Recommendation'].tolist()
        return "\n\n".join(f"• {rec}" for rec in recs)
    return None

# --- Helper: OpenAI Response ---
def get_openai_response(prompt):
    try:
        if not openai_api_key:
            return "🚫 Please provide your OpenAI API key."
        openai.api_key = openai_api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a helpful battery support assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"❌ Error: {e}"

# --- Layout ---
col1, col2, col3 = st.columns([1, 4, 2])

# --- Left: Placeholder or Features ---
with col1:
    st.markdown("### 🔧 Tools")
    st.write("• Troubleshoot\n• Warranty Info\n• File Complaint")

# --- Center: Chat ---
with col2:
    st.markdown("### 💬 Chat")
    for i, msg in enumerate(st.session_state.messages):
        message(msg["content"], is_user=(msg["role"] == "user"), key=str(i))

    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user input
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Check CSV first
        local_response = search_csv(user_input)
        if local_response:
            bot_reply = f"🔍 Based on local database:\n{local_response}"
        else:
            # Use OpenAI
            bot_reply = get_openai_response(user_input)

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()

# --- Right: Suggestions ---
with col3:
    st.markdown("### 🧠 Quick Help")
    st.info("Battery Health Tips")
    st.info("Nearest Service Centers")
    st.markdown("💡 Try asking:")
    st.markdown("> My battery drains fast")
    st.markdown("> How long is the warranty?")
