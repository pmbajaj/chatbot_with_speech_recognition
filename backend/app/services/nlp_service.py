import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
from typing import Dict, List
import openai
from deep_translator import GoogleTranslator
import os
from dotenv import load_dotenv

# Download required NLTK data
nltk.download('punkt')
nltk.download('vader_lexicon')

class NLPService:
    def __init__(self):
        load_dotenv()
        self.sia = SentimentIntensityAnalyzer()
        self.nlp = spacy.load('en_core_web_sm')
        openai.api_key = os.getenv('OPENAI_API_KEY')

    async def process_text(self, text: str) -> str:
        """
        Process the input text and generate an appropriate response.
        """
        # Detect language
        lang = self.detect_language(text)
        
        # Analyze sentiment
        sentiment = self.analyze_sentiment(text)
        
        # Generate response using OpenAI
        response = await self.generate_ai_response(text, sentiment, lang)
        
        return response

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text.
        """
        try:
            # Use Google Translate's language detection
            detected = GoogleTranslator(source='auto', target='en').detect(text)
            return detected.lang
        except:
            return 'en'

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze the sentiment of the input text.
        """
        return self.sia.polarity_scores(text)

    async def generate_ai_response(self, text: str, sentiment: Dict[str, float], lang: str) -> str:
        """
        Generate an AI response using OpenAI's GPT model.
        """
        try:
            # Prepare the prompt
            prompt = f"""
            User message: {text}
            Language: {lang}
            Sentiment: {sentiment}
            
            Please provide a helpful and appropriate response in the same language as the user's message.
            If the sentiment is negative, be empathetic and supportive.
            """
            
            # Generate response using OpenAI
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful and empathetic AI assistant that can communicate in both English and Hindi."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback response if AI generation fails
            if lang == 'hi':
                return "मैं आपकी कैसे मदद कर सकता हूं?"
            return "How can I help you?"

    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize the input text.
        """
        return word_tokenize(text)

    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract named entities from the text.
        """
        doc = self.nlp(text)
        return [{"text": ent.text, "label": ent.label_} for ent in doc.ents] 