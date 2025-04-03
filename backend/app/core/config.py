from pydantic import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "NLP Chatbot"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React frontend
        "http://localhost:8000",  # FastAPI backend
    ]
    
    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = None
    
    # Speech Recognition Settings
    SPEECH_RECOGNITION_LANGUAGES: List[str] = ["en-IN", "hi-IN"]
    SPEECH_RECOGNITION_TIMEOUT: int = 5
    SPEECH_RECOGNITION_PHRASE_TIMEOUT: int = 10
    
    # WebSocket Settings
    WEBSOCKET_PING_INTERVAL: int = 20
    WEBSOCKET_PING_TIMEOUT: int = 20
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Model Settings
    MODEL_NAME: str = "facebook/wav2vec2-base-960h"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 