import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIGURATION ---
st.set_page_config(page_title="TechSupport AI", page_icon="🤖")
st.title("🤖 Tech Support Assistant")

# Sidebar for API Key (Better security than hardcoding)
with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    "[Get a Gemini API Key](https://aistudio.google.com/app/apikey)"

# --- 2. INITIALIZE GEMINI ---
if api_key:
    genai.configure(api_key=api_key)
    
    # Define the persona
    system_instruction = (
        "You are a friendly Tech Support Specialist. Provide step-by-step help "
        "for hardware/software issues. Use bold text for buttons or menu names."
    )
    
    # Initialize model
    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        system_instruction=system_instruction
    )

    # --- 3. CHAT HISTORY MANAGEMENT ---
    # Streamlit reruns the whole script on every interaction. 
    # We store the chat object in session_state so it persists.
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Display existing chat messages from history
    for message in st.session_state.chat_session.history:
        role = "assistant" if message.role == "model" else "user"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # --- 4. USER INPUT & RESPONSE ---
    if prompt := st.chat_input("How can I help you today?"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.info("Please enter your Gemini API Key in the sidebar to start.")