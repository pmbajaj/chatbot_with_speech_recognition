import speech_recognition as sr
import asyncio
from .services.speech_service import SpeechService
from .services.nlp_service import NLPService
import sys
import os
import time
import signal

class TerminalChat:
    def __init__(self):
        self.speech_service = SpeechService()
        self.nlp_service = NLPService()
        self.recognizer = sr.Recognizer()
        self.is_running = True
        # Set up signal handler
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle Ctrl+C signal"""
        print("\nExiting gracefully...")
        self.is_running = False
        sys.exit(0)

    async def process_voice_input(self):
        """Process voice input from the microphone"""
        try:
            # List available microphones
            mics = sr.Microphone.list_microphone_names()
            print("\nAvailable microphones:")
            for i, mic in enumerate(mics):
                print(f"{i}: {mic}")
            
            # Try to find the best microphone
            mic_index = None
            for i, mic in enumerate(mics):
                if "microphone" in mic.lower() and "realtek" in mic.lower():
                    mic_index = i
                    break
            
            if mic_index is None:
                print("Using default microphone...")
                mic = sr.Microphone()
            else:
                print(f"Using microphone: {mics[mic_index]}")
                mic = sr.Microphone(device_index=mic_index)
            
            with mic as source:
                print("\nListening... (Press Ctrl+C to stop)")
                try:
                    # Adjust for ambient noise with longer duration
                    print("Adjusting for ambient noise...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=3)
                    
                    # Ensure energy threshold is within bounds
                    current_threshold = self.recognizer.energy_threshold
                    if current_threshold < self.speech_service.min_energy_threshold:
                        print(f"Adjusting energy threshold from {current_threshold:.2f} to {self.speech_service.min_energy_threshold}")
                        self.recognizer.energy_threshold = self.speech_service.min_energy_threshold
                    elif current_threshold > self.speech_service.max_energy_threshold:
                        print(f"Adjusting energy threshold from {current_threshold:.2f} to {self.speech_service.max_energy_threshold}")
                        self.recognizer.energy_threshold = self.speech_service.max_energy_threshold
                    
                    print(f"Energy threshold: {self.recognizer.energy_threshold:.2f}")
                    print("Ready! Speak now...")
                    
                    # Listen for audio input with longer timeout
                    print("Waiting for speech...")
                    audio = self.recognizer.listen(
                        source,
                        timeout=10,  # Increased timeout
                        phrase_time_limit=15  # Increased phrase time limit
                    )
                    
                    # Calculate audio duration
                    duration = len(audio.frame_data) / (audio.sample_rate * audio.sample_width)
                    print(f"Audio captured! Duration: {duration:.2f} seconds")
                    
                    # Check if the audio is too short
                    if duration < 0.5:
                        print("Audio too short, please speak longer")
                        return None
                    
                    print("Processing audio...")
                    
                    # Process the audio
                    text = await self.speech_service.process_audio(audio.get_wav_data())
                    
                    if text and text != "Could not understand audio":
                        print(f"\nYou said: {text}")
                        return text
                    else:
                        print("\nNo speech was detected or understood. Please try again.")
                        return None
                        
                except sr.WaitTimeoutError:
                    print("No speech detected within timeout period")
                    return None
                except KeyboardInterrupt:
                    print("\nVoice input cancelled.")
                    self.is_running = False
                    return None
                except Exception as e:
                    print(f"Error during voice input: {str(e)}")
                    return None
        except KeyboardInterrupt:
            print("\nVoice input cancelled.")
            self.is_running = False
            return None

    async def process_text_input(self):
        """Process text input from the terminal"""
        try:
            text = input("\nYou: ")
            return text
        except KeyboardInterrupt:
            print("\nText input cancelled.")
            self.is_running = False
            return None

    async def run(self):
        """Main loop for the terminal chat"""
        print("Welcome to the NLP Chatbot!")
        print("You can type your message or press Enter to use voice input")
        print("Type 'exit' or 'quit' to end the conversation")
        print("Press Ctrl+C at any time to exit\n")

        try:
            while self.is_running:
                try:
                    # Get input (text or voice)
                    text = await self.process_text_input()
                    
                    if not text and self.is_running:
                        print("\nUsing voice input...")
                        text = await self.process_voice_input()

                    if not text or not self.is_running:
                        continue

                    # Check for exit command
                    if await self.speech_service.is_exit_command(text):
                        print("\nGoodbye!")
                        break

                    # Process the input and get response
                    print("\nProcessing your message...")
                    response = await self.nlp_service.process_text(text)
                    print(f"\nBot: {response}")

                except KeyboardInterrupt:
                    print("\nOperation cancelled.")
                    self.is_running = False
                    break
                except Exception as e:
                    print(f"\nError: {str(e)}")
                    continue
        except KeyboardInterrupt:
            print("\nChat terminated.")
            self.is_running = False
        finally:
            print("\nGoodbye!")

def main():
    try:
        # Clear terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Create and run the chat
        chat = TerminalChat()
        asyncio.run(chat.run())
    except KeyboardInterrupt:
        print("\nChat terminated.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 