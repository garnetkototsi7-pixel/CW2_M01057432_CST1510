import streamlit as st
from google import genai
from google.genai import types
from google.genai.types import Part, GenerateContentConfig

st.title("🛡 Cybersecurity AI Assistant")

client = genai.Client(api_key=st.secrets["api_key"])

st.subheader("Gemini App")

system_instructions = """You are a cybersecurity expert assistant.
- Analyze incidents and threats
- Provide technical guidance
- Explain attack vectors and mitigations
- Use standard terminology (MITRE ATT&CK, CVE)
- Prioritize actionable recommendations
Tone: Professional, technical
Format: Clear, structured using headings and bullet points."""

# Initialise session state
if 'messages' not in st.session_state:
    st.session_state.messages = []


# Display existing messages
for message in st.session_state.messages:
    if message["role"] == "model":
        role = "assistant"
    else:
        role = message["role"]
    with st.chat_message(role):
        if message.get("parts") and hasattr(message["parts"][0], 'text'):
            st.markdown(message["parts"][0].text)
        else:
            st.markdown("_Message content is not text._")

# Show message count
with st.sidebar:
    st.title("💬 Chat Controls")

    # Show message count
    message_count = len(st.session_state.get("messages", []))
    st.metric("Messages", message_count)

    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        # Reset messages to initial state
        st.session_state.messages = []
        # Rerun to refresh the interface
        st.rerun()

# User input
prompt = st.chat_input("Say Something")

if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "parts": [Part(text=prompt)] 
    })

    # Send to Gemini
    response = client.models.generate_content_stream(
        model="gemini-flash-lite-latest",
        config=GenerateContentConfig(
            system_instruction=system_instructions),
        contents=st.session_state.messages,
    )

    # Display streaming assistant output
    with st.chat_message("assistant"):
        container = st.empty()
        full_reply = ""
        for chunk in response:
            if chunk.text:
              full_reply += chunk.text
              container.markdown(full_reply)

    # Save assistant message
    assistant_message = {
        "role": "model",
        "parts": [Part(text=full_reply)]
        }
    st.session_state.messages.append(assistant_message)
    st.rerun()