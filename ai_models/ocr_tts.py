"""
OCR to TTS Pipeline
Converts printed text to speech for low-vision/blind users
"""

import cv2
import numpy as np
from PIL import Image
import pytesseract
from gtts import gTTS
import io
import os
from typing import Optional

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    print("Warning: pyttsx3 not available. Using gTTS only.")


class OCRTTS:
    """
    OCR to Text-to-Speech pipeline
    """
    
    def __init__(self, tts_engine: str = "gtts"):
        """
        Initialize OCR-TTS pipeline
        
        Args:
            tts_engine: TTS engine ('gtts' or 'pyttsx3')
        """
        self.tts_engine = tts_engine
        
        if tts_engine == "pyttsx3" and PYTTSX3_AVAILABLE:
            self.tts = pyttsx3.init()
            self.tts.setProperty('rate', 150)  # Speed
            self.tts.setProperty('volume', 0.9)  # Volume
        else:
            self.tts = None
    
    def extract_text(self, image_path: str) -> str:
        """
        Extract text from image using OCR
        
        Args:
            image_path: Path to image file
        
        Returns:
            Extracted text
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # Preprocess image
            processed = self._preprocess_image(image)
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(processed, lang='eng')
            
            # Clean text
            text = self._clean_text(text)
            
            return text
        
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def extract_text_from_array(self, image_array: np.ndarray) -> str:
        """
        Extract text from numpy array image
        
        Args:
            image_array: Image as numpy array (BGR format)
        
        Returns:
            Extracted text
        """
        try:
            # Preprocess
            processed = self._preprocess_image(image_array)
            
            # Extract text
            text = pytesseract.image_to_string(processed, lang='eng')
            
            # Clean
            text = self._clean_text(text)
            
            return text
        
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def text_to_speech(self, text: str, output_path: Optional[str] = None, lang: str = 'en') -> str:
        """
        Convert text to speech
        
        Args:
            text: Text to convert
            output_path: Optional output path for audio file
            lang: Language code (default: 'en')
        
        Returns:
            Path to audio file (if saved) or plays audio
        """
        if not text.strip():
            print("No text to convert to speech")
            return ""
        
        if self.tts_engine == "pyttsx3" and self.tts:
            # Use pyttsx3 (offline)
            if output_path:
                self.tts.save_to_file(text, output_path)
                self.tts.runAndWait()
                return output_path
            else:
                self.tts.say(text)
                self.tts.runAndWait()
                return ""
        else:
            # Use gTTS (online)
            tts = gTTS(text=text, lang=lang, slow=False)
            
            if output_path:
                tts.save(output_path)
                return output_path
            else:
                # Save to temporary file and play
                temp_path = "temp_tts.mp3"
                tts.save(temp_path)
                # In production, use audio player library
                print(f"Audio saved to {temp_path}")
                return temp_path
    
    def process_image_to_speech(self, image_path: str, output_audio_path: Optional[str] = None) -> str:
        """
        Complete pipeline: Image -> Text -> Speech
        
        Args:
            image_path: Path to image file
            output_audio_path: Optional output path for audio file
        
        Returns:
            Path to audio file
        """
        # Extract text
        text = self.extract_text(image_path)
        
        if not text:
            print("No text found in image")
            return ""
        
        print(f"Extracted text: {text[:100]}...")
        
        # Convert to speech
        if not output_audio_path:
            output_audio_path = "output_tts.mp3"
        
        audio_path = self.text_to_speech(text, output_audio_path)
        return audio_path
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR results
        
        Args:
            image: Input image (BGR format)
        
        Returns:
            Preprocessed image (grayscale)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        return denoised
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text
        
        Args:
            text: Raw extracted text
        
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n'.join(lines)
        
        # Remove special characters (optional)
        # text = re.sub(r'[^\w\s\n]', '', text)
        
        return text


def main():
    """Demo: OCR to TTS pipeline"""
    print("OCR to TTS Pipeline Demo")
    print("=" * 50)
    
    ocr_tts = OCRTTS(tts_engine="gtts")
    
    # Example: Process image to speech
    # image_path = "assets/images/sample_text.png"
    # if os.path.exists(image_path):
    #     audio_path = ocr_tts.process_image_to_speech(image_path)
    #     print(f"Audio saved to: {audio_path}")
    # else:
    #     print(f"Image not found: {image_path}")
    
    # Example: Direct text to speech
    sample_text = "Hello, this is a test of the text-to-speech system."
    print(f"\nConverting text to speech: {sample_text}")
    audio_path = ocr_tts.text_to_speech(sample_text, "demo_tts.mp3")
    print(f"Audio saved to: {audio_path}")


if __name__ == "__main__":
    main()

