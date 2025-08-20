# step1: streamlit setup
import streamlit as st
import requests

BACKEND_URL = "https://ai-medical-therapist.onrender.com/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("Safespace Mental Health Therapist")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# step2: user is able to asks question
user_input = st.chat_input("What's on your mind today?")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    try:
        response = requests.post(BACKEND_URL, json={"message": user_input})
        if response.ok:
            data = response.json()
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"{data.get('response', 'No response')} WITH TOOL: [{data.get('tool_called', 'None')}]"
            })
        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"Error {response.status_code}: Could not process your request."
            })
    except requests.exceptions.JSONDecodeError:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Error: Backend did not return valid JSON."
        })

# step3: show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
