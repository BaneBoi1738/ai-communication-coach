from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("\u274c Missing OpenAI API Key! Set it in .env or environment variables.")

# Initialize OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Database Setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Fix threading issue
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define FastAPI App
app = FastAPI(title="AI Chat API", description="FastAPI wrapper for OpenAI GPT", version="1.0")

# Root endpoint for health check
@app.get("/")
async def root():
    return {"message": "API is running!"}

# Chat API
@app.post("/chat/")
async def chat(prompt: str = Query(..., description="User's chat query")):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"response": response.choices[0].message.content}  # FIXED LINE
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Speech to Text
@app.post("/speech-to-text/")
async def speech_to_text(audio_data: str = Query(..., description="Base64 encoded audio")):
    try:
        response = client.audio.transcriptions.create(
            model="whisper-1", 
            audio=audio_data
        )
        return {"text": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Text to Speech
@app.post("/text-to-speech/")
async def text_to_speech(text: str = Query(..., description="Text to convert to speech")):
    try:
        response = client.audio.speech.create(
            model="tts-1", 
            input=text, 
            voice="alloy"
        )
        return {"speech_url": response.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Conflict Resolution Training
@app.post("/training/conflict-resolution/")
async def conflict_resolution(user_input: str = Query(..., description="Conflict resolution scenario input")):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"How to resolve conflict: {user_input}"}]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Storytelling Training
@app.post("/training/storytelling/")
async def storytelling(user_input: str = Query(..., description="Storytelling prompt")):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Tell a story about: {user_input}"}]
        )
        return {"story": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Presentation Assessment
@app.post("/presentation-assessment/")
async def presentation_assessment(text: str = Query(..., description="Presentation content for evaluation")):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Assess this presentation: {text}"}]
        )
        return {"feedback": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
