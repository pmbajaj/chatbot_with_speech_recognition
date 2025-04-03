import speech_recognition as sr
import numpy as np
import io
from typing import Optional
import asyncio
from deep_translator import GoogleTranslator
import wave
import json
import os
import tempfile
import time
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import soundfile as sf
import librosa
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechService:
    def __init__(self):
        try:
            logger.info("Initializing SpeechService...")
            
            # Initialize speech recognizer
            self.recognizer = sr.Recognizer()
            # Configure recognizer settings for better recognition
            self.recognizer.energy_threshold = 6000  # Higher base threshold
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            self.recognizer.phrase_threshold = 0.3
            self.recognizer.non_speaking_duration = 0.5
            self.min_energy_threshold = 3000  # Much higher minimum threshold
            self.max_energy_threshold = 10000  # Maximum threshold to prevent over-sensitivity
            
            # Initialize wav2vec2 model
            logger.info("Loading wav2vec2 model...")
            # Using the correct model identifier
            self.model_name = "facebook/wav2vec2-base-960h"
            
            try:
                logger.info(f"Loading tokenizer from {self.model_name}...")
                self.tokenizer = Wav2Vec2Tokenizer.from_pretrained(self.model_name)
                logger.info("Tokenizer loaded successfully!")
                
                logger.info(f"Loading model from {self.model_name}...")
                self.model = Wav2Vec2ForCTC.from_pretrained(self.model_name)
                logger.info("Model loaded successfully!")
                
                # Move model to GPU if available
                if torch.cuda.is_available():
                    logger.info("Moving model to GPU...")
                    self.model = self.model.to('cuda')
                    logger.info("Model moved to GPU successfully!")
                else:
                    logger.info("No GPU available, using CPU")
                
            except Exception as e:
                logger.error(f"Error loading wav2vec2 model: {str(e)}")
                raise
            
            logger.info("SpeechService initialized successfully!")
            
        except Exception as e:
            logger.error(f"Failed to initialize SpeechService: {str(e)}")
            raise

    def _preprocess_audio(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Preprocess audio for better recognition"""
        # Resample to 16kHz if needed
        if sample_rate != 16000:
            audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=16000)
        
        # Normalize audio
        audio = librosa.util.normalize(audio)
        
        # Apply noise reduction
        audio = librosa.effects.preemphasis(audio)
        
        return audio

    async def process_audio(self, audio_data: bytes) -> str:
        """
        Process audio data and convert it to text using wav2vec2.
        Supports both English and Hindi speech recognition.
        """
        temp_file = None
        try:
            # Save audio data to a temporary WAV file
            temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            temp_file.close()
            
            # Convert bytes to WAV file
            with wave.open(temp_file.name, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(16000)  # 16kHz
                wav_file.writeframes(audio_data)
            
            print("Attempting to recognize speech using wav2vec2...")
            
            # Read audio file
            audio, sample_rate = sf.read(temp_file.name)
            
            # Ensure audio is mono and float32
            if len(audio.shape) > 1:
                audio = audio.mean(axis=1)
            audio = audio.astype(np.float32)
            
            # Preprocess audio
            audio = self._preprocess_audio(audio, sample_rate)
            
            # Tokenize audio
            inputs = self.tokenizer(
                audio,
                sampling_rate=16000,
                return_tensors="pt",
                padding=True
            )
            
            # Get model prediction
            with torch.no_grad():
                logits = self.model(inputs.input_values).logits
            
            # Get predicted ids
            predicted_ids = torch.argmax(logits, dim=-1)
            
            # Decode prediction
            transcription = self.tokenizer.batch_decode(predicted_ids)[0]
            
            if transcription and transcription.strip():
                # Calculate confidence based on word count and length
                words = transcription.split()
                confidence = min(1.0, len(words) * 0.2)  # 20% per word, max 100%
                print(f"\nTranscription: {transcription}")
                print(f"Confidence: {confidence:.2%}")
                
                if confidence > 0.15:
                    return transcription
            
            print("\nNo speech was recognized")
            return "Could not understand audio"

        except Exception as e:
            print(f"Error processing audio: {str(e)}")
            return f"Error processing audio: {str(e)}"
        finally:
            # Clean up temporary file with retry
            if temp_file and os.path.exists(temp_file.name):
                try:
                    # Close any open file handles
                    time.sleep(0.1)  # Give time for file handles to close
                    os.unlink(temp_file.name)
                except Exception as e:
                    print(f"Warning: Could not delete temporary file: {str(e)}")

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text.
        Returns 'en' for English or 'hi' for Hindi.
        """
        try:
            # Use Google Translate's language detection
            detected = GoogleTranslator(source='auto', target='en').detect(text)
            return detected.lang
        except:
            return 'en'  # Default to English if detection fails

    async def is_exit_command(self, text: str) -> bool:
        """
        Check if the text is an exit command in either English or Hindi.
        """
        exit_commands = {
            'en': ['exit', 'quit', 'stop', 'end'],
            'hi': ['बंद', 'बाहर', 'रुको', 'समाप्त']
        }
        
        text = text.lower().strip()
        lang = self.detect_language(text)
        
        return text in exit_commands.get(lang, []) 