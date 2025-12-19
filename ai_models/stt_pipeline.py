"""
Speech-to-Text (STT) Pipeline
Converts speech to text for voice commands
"""

import speech_recognition as sr
import pyaudio
from typing import Optional, Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class STTPipeline:
    """
    Speech-to-Text pipeline using Google Speech Recognition
    """
    
    def __init__(self, language: str = 'en-US'):
        """
        Initialize STT pipeline
        
        Args:
            language: Language code (default: 'en-US')
        """
        self.recognizer = sr.Recognizer()
        self.language = language
        self.microphone = None
    
    def listen_and_transcribe(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen to microphone and transcribe speech
        
        Args:
            timeout: Timeout in seconds
            phrase_time_limit: Maximum phrase length in seconds
        
        Returns:
            Transcribed text or None
        """
        try:
            # Initialize microphone if not already done
            if self.microphone is None:
                self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            logger.info("Adjusting for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Listen and transcribe
            logger.info("Listening...")
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            # Recognize speech
            logger.info("Transcribing...")
            text = self.recognizer.recognize_google(audio, language=self.language)
            
            return text
        
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Error with speech recognition service: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def transcribe_audio_file(self, audio_file_path: str) -> Optional[str]:
        """
        Transcribe audio from file
        
        Args:
            audio_file_path: Path to audio file
        
        Returns:
            Transcribed text or None
        """
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
            
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
        
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Error with speech recognition service: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def continuous_listen(self, callback: Callable[[str], None], stop_phrase: str = "stop"):
        """
        Continuously listen and transcribe
        
        Args:
            callback: Callback function called with transcribed text
            stop_phrase: Phrase to stop listening
        """
        logger.info("Starting continuous listening...")
        logger.info(f"Say '{stop_phrase}' to stop")
        
        while True:
            text = self.listen_and_transcribe()
            
            if text:
                logger.info(f"Transcribed: {text}")
                
                # Check for stop phrase
                if stop_phrase.lower() in text.lower():
                    logger.info("Stop phrase detected. Stopping...")
                    break
                
                # Call callback
                callback(text)
    
    def get_available_microphones(self) -> list:
        """
        Get list of available microphones
        
        Returns:
            List of microphone names
        """
        return sr.Microphone.list_microphone_names()


def main():
    """Demo: STT pipeline"""
    print("Speech-to-Text Pipeline Demo")
    print("=" * 50)
    
    stt = STTPipeline(language='en-US')
    
    # List available microphones
    print("\nAvailable microphones:")
    mics = stt.get_available_microphones()
    for i, mic in enumerate(mics):
        print(f"  {i}: {mic}")
    
    # Test transcription
    print("\nListening for speech...")
    print("Say something (5 second timeout)...")
    
    text = stt.listen_and_transcribe(timeout=5, phrase_time_limit=10)
    
    if text:
        print(f"Transcribed: {text}")
    else:
        print("No speech detected or transcription failed")
    
    # Continuous listening example (commented out)
    # def on_transcription(text):
    #     print(f"Received: {text}")
    # 
    # stt.continuous_listen(on_transcription, stop_phrase="stop listening")


if __name__ == "__main__":
    main()

