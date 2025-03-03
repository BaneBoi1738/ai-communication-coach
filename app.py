import streamlit as st
import requests
import urllib.parse
import base64
import json
from io import BytesIO

# FastAPI Base URL
FASTAPI_URL = "http://127.0.0.1:8000"

st.title("AI Verbal Communication Trainer")

# User Input for Chat
st.subheader("Chat with AI")
user_input = st.text_input("Enter your message:")
if st.button("Send Chat Request"):
    if user_input:
        api_url = f"{FASTAPI_URL}/chat/?prompt={urllib.parse.quote(user_input)}"
        response = requests.post(api_url, headers={"Accept": "application/json"})
        if response.status_code == 200:
            st.write("### AI Response:")
            st.write(response.json()["response"])
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

# Speech-to-Text Upload
st.subheader("Speech to Text")
uploaded_audio = st.file_uploader("Upload your speech file (WAV/MP3)", type=["wav", "mp3"])
if uploaded_audio and st.button("Convert to Text"):
    files = {"file": (uploaded_audio.name, uploaded_audio, uploaded_audio.type)}
    response = requests.post(f"{FASTAPI_URL}/speech-to-text/", files=files)
    if response.status_code == 200:
        st.write("### Transcribed Text:")
        st.write(response.json()["transcription"])
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

# Text-to-Speech
st.subheader("Text to Speech")
tts_input = st.text_area("Enter text for speech synthesis:")
if st.button("Convert to Speech"):
    response = requests.post(f"{FASTAPI_URL}/text-to-speech/", json={"text": tts_input})
    if response.status_code == 200:
        audio_bytes = base64.b64decode(response.json()["audio_base64"])
        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

# Skill Training Module
st.subheader("Skill Training Activities")
activity_type = st.selectbox("Select Activity", ["Impromptu Speaking", "Storytelling", "Conflict Resolution"])
if st.button("Start Activity"):
    response = requests.post(f"{FASTAPI_URL}/train-skill/", json={"activity": activity_type})
    if response.status_code == 200:
        st.write("### Training Exercise:")
        st.write(response.json()["exercise"])
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

# Presentation Assessment
st.subheader("Presentation Assessment")
presentation_text = st.text_area("Enter or Upload Your Presentation")
if st.button("Get AI Feedback"):
    response = requests.post(f"{FASTAPI_URL}/assess-presentation/", json={"text": presentation_text})
    if response.status_code == 200:
        st.write("### AI Feedback:")
        st.write(response.json()["feedback"])
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

st.write("---")
st.write("Developed for AI Verbal Communication Training")