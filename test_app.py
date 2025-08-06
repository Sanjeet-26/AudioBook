#!/usr/bin/env python3
"""
Test Script for PDF to Audiobook Converter
Tests basic functionality of all modules
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import PyPDF2
        print("✓ PyPDF2 imported successfully")
    except ImportError:
        print("✗ PyPDF2 not found - run: pip install PyPDF2")
        return False
    
    try:
        import pyttsx3
        print("✓ pyttsx3 imported successfully")
    except ImportError:
        print("✗ pyttsx3 not found - run: pip install pyttsx3")
        return False
    
    try:
        from pdf_reader import PDFReader
        print("✓ PDFReader module imported successfully")
    except ImportError as e:
        print(f"✗ PDFReader module not found: {e}")
        return False
    
    try:
        from audio_converter import AudioConverter
        print("✓ AudioConverter module imported successfully")
    except ImportError as e:
        print(f"✗ AudioConverter module not found: {e}")
        return False
    
    try:
        from gui import AudiobookGUI
        print("✓ AudiobookGUI module imported successfully")
    except ImportError as e:
        print(f"✗ AudiobookGUI module not found: {e}")
        return False
    
    return True

def test_audio_converter():
    """Test AudioConverter functionality"""
    print("\nTesting AudioConverter...")
    
    try:
        from audio_converter import AudioConverter
        
        converter = AudioConverter()
        
        # Test engine initialization
        info = converter.get_engine_info()
        if info:
            print(f"✓ TTS engine initialized (Rate: {info['rate']}, Volume: {info['volume']})")
        else:
            print("✗ TTS engine failed to initialize")
            return False
        
        # Test available voices
        voices = converter.get_available_voices()
        print(f"✓ Found {len(voices)} available voices")
        
        # Test basic speech (non-blocking)
        print("✓ Testing basic speech functionality...")
        success, message = converter.speak_text("Hello, this is a test.", blocking=False)
        
        if success:
            print("✓ Speech test completed successfully")
        else:
            print(f"✗ Speech test failed: {message}")
            return False
        
        converter.cleanup()
        print("✓ AudioConverter cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"✗ AudioConverter test failed: {str(e)}")
        return False

def test_pdf_reader():
    """Test PDFReader functionality"""
    print("\nTesting PDFReader...")
    
    try:
        from pdf_reader import PDFReader
        
        reader = PDFReader()
        print("✓ PDFReader instance created")
        
        # Note: We can't test PDF loading without an actual PDF file
        print("✓ PDFReader basic functionality available")
        print("  (Note: PDF loading requires an actual PDF file)")
        
        reader.close_pdf()
        print("✓ PDFReader cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"✗ PDFReader test failed: {str(e)}")
        return False

def create_sample_pdf():
    """Create a simple sample PDF for testing"""
    try:
        # This is optional - requires reportlab
        # We'll skip this for now to avoid additional dependencies
        print("\nSample PDF creation skipped (requires reportlab)")
        return None
    except:
        return None

def main():
    """Run all tests"""
    print("PDF to Audiobook Converter - Test Suite")
    print("=" * 45)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test AudioConverter
    if not test_audio_converter():
        all_passed = False
    
    # Test PDFReader
    if not test_pdf_reader():
        all_passed = False
    
    print("\n" + "=" * 45)
    
    if all_passed:
        print("✓ All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("python main.py")
    else:
        print("✗ Some tests failed. Please check the error messages above.")
        print("\nMake sure to install required dependencies:")
        print("pip install -r requirements.txt")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
