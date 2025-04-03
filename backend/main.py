from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.services.speech_service import SpeechService
from app.services.nlp_service import NLPService
from app.core.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NLP Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
try:
    logger.info("Initializing services...")
    speech_service = SpeechService()
    nlp_service = NLPService()
    logger.info("Services initialized successfully!")
except Exception as e:
    logger.error(f"Failed to initialize services: {str(e)}")
    raise

@app.get("/")
async def root():
    return {"message": "Welcome to the NLP Chatbot API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        return {
            "status": "healthy",
            "services": {
                "speech": "initialized",
                "nlp": "initialized"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/text")
async def chat_text(text: str, language: str = "en"):
    """Handle text chat messages"""
    try:
        response = await nlp_service.process_text(text)
        return {"text": response}
    except Exception as e:
        logger.error(f"Error processing text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/voice")
async def chat_voice(audio: bytes, language: str = "en"):
    """Handle voice chat messages"""
    try:
        text = await speech_service.process_audio(audio)
        response = await nlp_service.process_text(text)
        return {"text": response}
    except Exception as e:
        logger.error(f"Error processing voice: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive audio data
            data = await websocket.receive_bytes()
            
            # Process speech to text
            text = await speech_service.process_audio(data)
            
            # Process text with NLP
            response = await nlp_service.process_text(text)
            
            # Send response back to client
            await websocket.send_text(response)
            
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.close()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    try:
        logger.info("Starting server...")
        uvicorn.run(
            "main:app",
            host="127.0.0.1",  # Use localhost instead of 0.0.0.0
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise 