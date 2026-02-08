import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="TechSupport AI", page_icon="🤖")

# --- 1. SESSION STATE INITIALIZATION ---
# This keeps track of whether we have a valid key
if "api_key" not in st.session_state:
    st.session_state.api_key = None

# --- 2. THE API KEY "GATE" ---
# If no API key is found, show ONLY the input screen
if st.session_state.api_key is None:
    st.title("🔑 API Setup")
    st.info("Please enter your Gemini API Key to unlock the Tech Support Bot.")
    
    with st.form("api_key_form"):
        user_key = st.text_input("Gemini API Key", type="password")
        submitted = st.form_submit_button("Start Chatting")
        
        if submitted and user_key:
            st.session_state.api_key = user_key
            st.rerun() # This "closes" the setup screen and reloads the app
    st.stop() # Prevents the rest of the code from running until key is provided

# --- 3. CHAT INTERFACE (Only visible after key is read) ---
st.title("🤖 Tech Support Assistant")
if st.button("Log Out / Change Key"):
    st.session_state.api_key = None
    st.session_state.chat_session = None
    st.rerun()

# Configure Gemini
genai.configure(api_key=st.session_state.api_key)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash", # Updated to the latest 2026 stable model
    system_instruction="You are a polite Tech Support specialist."
)

# Initialize Chat Session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display Chat History
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# User Input
if prompt := st.chat_input("How can I help you?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")