import streamlit as st
import requests
import json
import os
import uuid
import time
import logging

# --- Setup Logging ---
# This will print logs to your console/terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# --- End Setup ---

# Set page config
st.set_page_config(
    page_title="Speaker Agent Chat",
    page_icon="🔊",
    layout="centered"
)

# Constants
API_BASE_URL = "http://localhost:8000"
APP_NAME = "hashfinance_orchestrator"

# Initialize session state variables
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user-{uuid.uuid4()}"
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "audio_to_play" not in st.session_state:
    st.session_state.audio_to_play = None

def create_session():
    session_id = f"session-{int(time.time())}"
    try:
        response = requests.post(
            f"{API_BASE_URL}/apps/{APP_NAME}/users/{st.session_state.user_id}/sessions/{session_id}",
            headers={"Content-Type": "application/json"},
            data=json.dumps({}),
            timeout=10
        )
        response.raise_for_status()
        st.session_state.session_id = session_id
        st.session_state.messages = []
        st.session_state.audio_to_play = None
        logging.info(f"Successfully created new session: {session_id}")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create session. Error: {e}")
        st.error(f"Failed to create session. Is the ADK API server running? Error: {e}")
        return False

def send_message(message):
    """
    Send a message to the speaker agent and process the response.
    """
    if not st.session_state.session_id:
        st.error("No active session. Please create a session first.")
        return False
    
    st.session_state.messages.append({"role": "user", "content": message})
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/run",
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                "app_name": APP_NAME,
                "user_id": st.session_state.user_id,
                "session_id": st.session_state.session_id,
                "new_message": {"role": "user", "parts": [{"text": message}]}
            }),
            timeout=30
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        st.error(f"Failed to send message. Error: {e}")
        st.session_state.messages.pop()
        return False
        
    events = response.json()
    logging.info(f"Received API response events: {events}")

    assistant_message = None
    audio_file_path = None
    
    # ==================== NEW LOGIC START ====================
    # Loop through all events to find the text response AND the function response path
    for event in events:
        content = event.get("content", {})
        if not content:
            continue
        
        parts = content.get("parts", [{}])
        
        # 1. Look for the final text response from the model to display
        if content.get("role") == "model" and "text" in parts[0]:
            assistant_message = parts[0]["text"]
            logging.info(f"Found final assistant text: '{assistant_message}'")

        # 2. Look for the function response that contains the file path
        if "functionResponse" in parts[0]:
            func_response_part = parts[0]["functionResponse"]
            logging.info(f"Found function response: {func_response_part}")

            # Check if this is from our speech agent (note the name from your logs)
            if func_response_part.get("name") == "speach_agent": 
                response_data = func_response_part.get("response", {})
                result_text = response_data.get("result", "")
                logging.info(f"Function result text: '{result_text}'")

                # Parse the path from this specific result text
                if "saved at" in result_text:
                    try:
                        # Get the part after "saved at", strip whitespace and backticks
                        path_part = result_text.split("saved at")[1].strip().strip('`')
                        if ".mp3" in path_part:
                            # Reconstruct to avoid extra text
                            audio_file_path = path_part.split(".mp3")[0] + ".mp3"
                            logging.info(f"Extracted path from function response: '{audio_file_path}'")
                    except IndexError:
                        pass
    # ===================== NEW LOGIC END =====================

    if audio_file_path:
        # Sanitize the path to handle Windows backslashes
        sanitized_path = audio_file_path.replace("\\", "/").strip()
        logging.info(f"Sanitized path for os.path.exists: '{sanitized_path}'")
        audio_file_path = sanitized_path
        
        # ==================== AUTOPLAY CHANGE ====================
        # Set the session state to trigger the audio player automatically
        st.session_state.audio_to_play = audio_file_path
        logging.info(f"Set audio_to_play for autoplay: {audio_file_path}")
        # =========================================================

    else:
        logging.warning("Could not find an audio file path in any of the API response events.")
    
    # Use the final text message, or a default if none is found
    final_message_to_display = assistant_message if assistant_message else "Action completed."
    
    st.session_state.messages.append({"role": "assistant", "content": final_message_to_display, "audio_path": audio_file_path})
    
    return True

# --- UI Components ---
st.title("🔊 Speaker Agent Chat")

with st.sidebar:
    st.header("Session Management")
    if st.session_state.session_id:
        st.success(f"Active session: {st.session_state.session_id}")
        if st.button("➕ New Session"):
            create_session()
            st.rerun()
    else:
        st.warning("No active session")
        if st.button("➕ Create Session"):
            create_session()
            st.rerun()
    st.divider()
    st.caption(f"Agent: '{APP_NAME}'")

st.subheader("Conversation")

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
        if msg["role"] == "assistant" and msg.get("audio_path"):
            audio_path = msg["audio_path"]
            
            # --- Detailed Logging for path check ---
            logging.info("--- Checking Audio Path ---")
            logging.info(f"Message index: {i}")
            logging.info(f"Path to check: '{audio_path}'")
            logging.info(f"Type of path variable: {type(audio_path)}")
            logging.info(f"Current working directory: {os.getcwd()}")
            
            exists = os.path.exists(audio_path)
            logging.info(f"os.path.exists() result: {exists}")
            # --- End Logging ---

            if exists:
                if st.button("▶️ Play Audio", key=f"play_{i}"):
                    st.session_state.audio_to_play = audio_path
                    st.rerun()
            else:
                st.warning(f"Audio file not accessible: `{audio_path}`")

if st.session_state.audio_to_play:
    path_to_play = st.session_state.audio_to_play
    logging.info(f"Attempting to play audio file: {path_to_play}")
    try:
        with open(path_to_play, "rb") as audio_file:
            audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        logging.info("Successfully loaded audio bytes for playback.")
    except Exception as e:
        logging.error(f"Could not open or read audio file. Error: {e}")
        st.error(f"Could not play audio file: {e}")
    
    st.session_state.audio_to_play = None

if st.session_state.session_id:
    user_input = st.chat_input("Type your message...")
    if user_input:
        send_message(user_input)
        st.rerun()
else:
    st.info("👈 Create a session in the sidebar to start chatting")