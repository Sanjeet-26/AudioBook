"""
PDF Reader Module
Handles PDF file reading and text extraction
"""
import PyPDF2
import os

class PDFReader:
    def __init__(self):
        self.pdf_file = None
        self.pdf_reader = None
        self.total_pages = 0
        self.current_page = 0
        
    def open_pdf(self, file_path):
        """Open and initialize PDF file for reading"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError("PDF file not found")
            
            self.pdf_file = open(file_path, 'rb')
            self.pdf_reader = PyPDF2.PdfReader(self.pdf_file)
            self.total_pages = len(self.pdf_reader.pages)
            self.current_page = 0
            
            return True, f"PDF opened successfully. Total pages: {self.total_pages}"
            
        except Exception as e:
            return False, f"Error opening PDF: {str(e)}"
    
    def get_page_text(self, page_number=None):
        """Extract text from a specific page"""
        try:
            if self.pdf_reader is None:
                return False, "No PDF file opened"
            
            if page_number is None:
                page_number = self.current_page              
            if page_number < 0 or page_number >= self.total_pages:
                return False, "Invalid page number"         
            page = self.pdf_reader.pages[page_number]
            text = page.extract_text()
            
            return True, text
            
        except Exception as e:
            return False, f"Error extracting text: {str(e)}"
    
    def get_all_text(self):
        """Extract text from all pages"""
        try:
            if self.pdf_reader is None:
                return False, "No PDF file```ened"
            
            full_text = ""
            for page_num in range(self.total_pages):
                success, text = self.get_page_text(page_num)
                if success:
                    full_text += text + "\n"
                else:
                    return False, text
            
            return True, full_text
            
        except Exception as e:
            return False, f"Error extracting all text: {str(e)}"
    
    def get_page_range_text(self, start_page, end_page):
        """Extract text from a range of pages"""  
        try:
            if self.pdf_reader is None:
                return False, "No PDF file opened"
            
            if start_page < 0 or end_page >= self.total_pages or art_page > end_page:
                return False, "Invalid page```nge"
            
            full_text = ""
            for page_num in range(start_page, end_page + 1):
                success, text = self.get_page_text(page_num)
                if success:
                    full_text += text +"/n"
                else:
                    return False, text
            
            return True, full_text
            
        except Exception as e:
            return False, f"Error extracting text from```ge range: {str(e)}"
    
    def close_pdf(self):
        """Close the PDF file"""
        if self.pdf_file:
            self.pdf_file.close()
            self.pdf_file = None
            self.pdf_reader = None
            self.total_pages = 0
            self.current_page = 0
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.close_pdf()
