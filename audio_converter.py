"""
Audio Converter Module
Handles text to speech conversion using pyttsx3
"""
import pyttsx3
import threading
import os

class AudioConverter:
    def __init__(self):
        self.engine = None
        self.is_speaking = False
        self.is_paused = False
        self.speech_thread = None
        self.initialize_engine()
    
    def initialize_engine(self):
        """Initialize the TTS engine with default settings"""
        try:
            self.engine = pyttsx3.init()
            
            # Set default properties
            self.set_voice_rate(150)  # Default speaking rate
            self.set_volume(0.8)      # Default volume
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)  # Use first available voice
            
            return True
            
        except Exception as e:
            print(f"Error initializing TTS engine: {str(e)}")
            return False
    
    def get_available_voices(self):
        """Get list of available voices"""
        try:
            if self.engine is None:
                return []
            
            voices = self.engine.getProperty('voices')
            voice_list = []
            
            for i, voice in enumerate(voices):
                voice_info = {
                    'id': voice.id,
                    'name': voice.name,
                    'gender': getattr(voice, 'gender', 'Unknown'),
                    'age': getattr(voice, 'age', 'Unknown'),
                    'index': i
                }
                voice_list.append(voice_info)
            
            return voice_list
            
        except Exception as e:
            print(f"Error getting voices: {str(e)}")
            return []
    
    def set_voice(self, voice_index=0):
        """Set voice by index"""
        try:
            if self.engine is None:
                return False
            
            voices = self.engine.getProperty('voices')
            if 0 <= voice_index < len(voices):
                self.engine.setProperty('voice', voices[voice_index].id)
                return True
            return False
            
        except Exception as e:
            print(f"Error setting voice: {str(e)}")
            return False
    
    def set_voice_rate(self, rate):
        """Set speaking rate (words per minute)"""
        try:
            if self.engine is None:
                return False
            
            # Typical range: 50-300 WPM
            rate = max(50, min(300, rate))
            self.engine.setProperty('rate', rate)
            return True
            
        except Exception as e:
            print(f"Error setting voice rate: {str(e)}")
            return False
    
    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)"""
        try:
            if self.engine is None:
                return False
            
            volume = max(0.0, min(1.0, volume))
            self.engine.setProperty('volume', volume)
            return True
            
        except Exception as e:
            print(f"Error setting volume: {str(e)}")
            return False
    
    def speak_text(self, text, blocking=False):
        """Convert text to speech"""
        try:
            if self.engine is None:
                return False, "TTS engine not initialized"
            
            if self.is_speaking:
                return False, "Already speaking"
            
            if not text.strip():
                return False, "No text to speak"
            
            if blocking:
                # Synchronous speech
                self.is_speaking = True
                self.engine.say(text)
                self.engine.runAndWait()
                self.is_speaking = False
                return True, "Speech completed"
            else:
                # Asynchronous speech
                self.speech_thread = threading.Thread(target=self._speak_async, args=(text,))
                self.speech_thread.daemon = True
                self.speech_thread.start()
                return True, "Speech started"
            
        except Exception as e:
            self.is_speaking = False
            return False, f"Error during speech: {str(e)}"
    
    def _speak_async(self, text):
        """Internal method for asynchronous speech"""
        try:
            self.is_speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
            self.is_speaking = False
        except Exception as e:
            print(f"Error in async speech: {str(e)}")
            self.is_speaking = False
    
    def stop_speech(self):
        """Stop current speech"""
        try:
            if self.engine is None:
                return False
            
            if self.is_speaking:
                self.engine.stop()
                self.is_speaking = False
            
            return True
            
        except Exception as e:
            print(f"Error stopping speech: {str(e)}")
            return False
    
    def save_to_audio_file(self, text, filename):
        """Save text as audio file"""
        try:
            if self.engine is None:
                return False, "TTS engine not initialized"
            
            if not text.strip():
                return False, "No text to save"
            
            # Ensure filename has .wav extension
            if not filename.lower().endswith('.wav'):
                filename += '.wav'
            
            # Save to file
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            
            # Check if file was created
            if os.path.exists(filename):
                return True, f"Audio saved to {filename}"
            else:
                return False, "Failed to create audio file"
            
        except Exception as e:
            return False, f"Error saving audio: {str(e)}"
    
    def is_busy(self):
        """Check if TTS engine is currently speaking"""
        return self.is_speaking
    
    def get_engine_info(self):
        """Get information about the TTS engine"""
        try:
            if self.engine is None:
                return None
            
            info = {
                'rate': self.engine.getProperty('rate'),
                'volume': self.engine.getProperty('volume'),
                'voice': self.engine.getProperty('voice'),
                'available_voices': len(self.get_available_voices())
            }
            
            return info
            
        except Exception as e:
            print(f"Error getting engine info: {str(e)}")
            return None
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            if self.is_speaking:
                self.stop_speech()
            
            if self.engine is not None:
                self.engine.stop()
                del self.engine
                self.engine = None
                
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.cleanup()
