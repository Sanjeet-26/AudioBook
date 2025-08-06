#!/usr/bin/env python3
"""
PDF to Audiobook Converter
Main application entry point

This application allows users to:
1. Browse and select PDF files
2. Convert PDF text to audio speech
3. Save audio files
4. Customize voice settings

Author: AI Assistant
Date: 2025
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Import our custom modules
try:
    from pdf_reader import PDFReader
    from audio_converter import AudioConverter
    from gui import AudiobookGUI
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all required files are in the same directory:")
    print("- pdf_reader.py")
    print("- audio_converter.py") 
    print("- gui.py")
    sys.exit(1)


class AudiobookApp:
    """Main application class"""
    
    def __init__(self):
        """Initialize the application"""
        self.pdf_reader = None
        self.audio_converter = None
        self.gui = None
        
        # Check dependencies
        if not self.check_dependencies():
            return
        
        # Initialize components
        self.initialize_components()
    
    def check_dependencies(self):
        """Check if required libraries are installed"""
        missing_libs = []
        
        try:
            import PyPDF2
        except ImportError:
            missing_libs.append("PyPDF2")
        
        try:
            import pyttsx3
        except ImportError:
            missing_libs.append("pyttsx3")
        
        if missing_libs:
            error_msg = f"""
Missing required libraries: {', '.join(missing_libs)}

Please install them using:
pip install {' '.join(missing_libs)}

Or install all requirements:
pip install -r requirements.txt
"""
            print(error_msg)
            
            # Try to show GUI error if tkinter is available
            try:
                root = tk.Tk()
                root.withdraw()  # Hide main window
                messagebox.showerror("Missing Dependencies", error_msg)
                root.destroy()
            except:
                pass
            
            return False
        
        return True
    
    def initialize_components(self):
        """Initialize application components"""
        try:
            # Initialize PDF reader
            self.pdf_reader = PDFReader()
            print("PDF reader initialized")
            
            # Initialize audio converter
            self.audio_converter = AudioConverter()
            print("Audio converter initialized")
            
            # Initialize GUI
            self.gui = AudiobookGUI(self.pdf_reader, self.audio_converter)
            print("GUI initialized")
            
        except Exception as e:
            error_msg = f"Error initializing application: {str(e)}"
            print(error_msg)
            
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Initialization Error", error_msg)
                root.destroy()
            except:
                pass
            
            sys.exit(1)
    
    def run(self):
        """Run the application"""
        try:
            print("Starting PDF to Audiobook Converter...")
            print("=" * 40)
            
            # Display application info
            self.display_info()
            
            # Start GUI
            self.gui.run()
            
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        except Exception as e:
            print(f"Application error: {str(e)}")
        finally:
            self.cleanup()
    
    def display_info(self):
        """Display application information"""
        print("PDF to Audiobook Converter v1.0")
        print("-" * 30)
        print("Features:")
        print("• Browse and load PDF files")
        print("• Read text aloud page by page")
        print("• Read entire document")
        print("• Save audio to WAV files")
        print("• Customize voice settings")
        print("-" * 30)
        
        # Display voice info
        if self.audio_converter:
            voices = self.audio_converter.get_available_voices()
            print(f"Available voices: {len(voices)}")
            
            engine_info = self.audio_converter.get_engine_info()
            if engine_info:
                print(f"Current rate: {engine_info.get('rate', 'Unknown')} WPM")
                print(f"Current volume: {engine_info.get('volume', 'Unknown')}")
        
        print("=" * 40)
    
    def cleanup(self):
        """Cleanup resources"""
        print("Cleaning up...")
        
        if self.gui:
            self.gui.cleanup()
        
        if self.audio_converter:
            self.audio_converter.cleanup()
        
        if self.pdf_reader:
            self.pdf_reader.close_pdf()
        
        print("Cleanup complete")


def main():
    """Main entry point"""
    # Set up error handling
    try:
        # Create and run application
        app = AudiobookApp()
        app.run()
        
    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
