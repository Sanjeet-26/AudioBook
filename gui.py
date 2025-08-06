"""
GUI Module
Handles the graphical user interface using Tkinter
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os

class AudiobookGUI:
    def __init__(self, pdf_reader, audio_converter):
        self.pdf_reader = pdf_reader
        self.audio_converter = audio_converter
        
        # Main window
        self.root = tk.Tk()
        self.root.title("PDF to Audiobook Converter")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Variables
        self.selected_file_path = tk.StringVar()
        self.current_page = tk.IntVar(value=1)
        self.total_pages = tk.IntVar()
        self.speaking_status = tk.StringVar(value="Ready")
        
        # Create GUI components
        self.create_widgets()
        
        # Center window on screen
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        
        # Main title
        title_label = tk.Label(
            self.root, 
            text="PDF to Audiobook Converter",
            font=("Arial", 16, "bold"),
            fg="blue"
        )
        title_label.pack(pady=10)
        
        # File selection frame
        file_frame = ttk.LabelFrame(self.root, text="File Selection", padding=10)
        file_frame.pack(fill="x", padx=20, pady=10)
        
        # File path display
        self.file_path_label = tk.Label(
            file_frame, 
            textvariable=self.selected_file_path,
            bg="white",
            relief="sunken",
            anchor="w",
            width=60
        )
        self.file_path_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Browse button
        self.browse_button = ttk.Button(
            file_frame,
            text="Browse PDF",
            command=self.browse_file,
            width=15
        )
        self.browse_button.pack(side="right")
        
        # Page selection frame
        page_frame = ttk.LabelFrame(self.root, text="Page Selection", padding=10)
        page_frame.pack(fill="x", padx=20, pady=10)
        
        # Current page selection
        tk.Label(page_frame, text="Current Page:").pack(side="left")
        
        self.page_spinbox = tk.Spinbox(
            page_frame,
            from_=1,
            to=1,
            textvariable=self.current_page,
            width=10,
            state="readonly"
        )
        self.page_spinbox.pack(side="left", padx=10)
        
        # Total pages display
        tk.Label(page_frame, text="Total Pages:").pack(side="left", padx=(20, 0))
        self.total_pages_label = tk.Label(
            page_frame, 
            textvariable=self.total_pages,
            font=("Arial", 10, "bold")
        )
        self.total_pages_label.pack(side="left", padx=5)
        
        # Control buttons frame
        control_frame = ttk.LabelFrame(self.root, text="Controls", padding=10)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        # Buttons row 1
        button_frame1 = tk.Frame(control_frame)
        button_frame1.pack(fill="x", pady=5)
        
        self.read_current_button = ttk.Button(
            button_frame1,
            text="Read Current Page",
            command=self.read_current_page,
            width=20
        )
        self.read_current_button.pack(side="left", padx=5)
        
        self.read_all_button = ttk.Button(
            button_frame1,
            text="Read All Pages",
            command=self.read_all_pages,
            width=20
        )
        self.read_all_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(
            button_frame1,
            text="Stop Reading",
            command=self.stop_reading,
            width=15
        )
        self.stop_button.pack(side="left", padx=5)
        
        # Buttons row 2
        button_frame2 = tk.Frame(control_frame)
        button_frame2.pack(fill="x", pady=5)
        
        self.save_audio_button = ttk.Button(
            button_frame2,
            text="Save as Audio File",
            command=self.save_audio_file,
            width=20
        )
        self.save_audio_button.pack(side="left", padx=5)
        
        self.settings_button = ttk.Button(
            button_frame2,
            text="Voice Settings",
            command=self.open_settings,
            width=15
        )
        self.settings_button.pack(side="left", padx=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = tk.Label(
            status_frame,
            textvariable=self.speaking_status,
            font=("Arial", 10),
            fg="green"
        )
        self.status_label.pack()
        
        # Text preview frame
        preview_frame = ttk.LabelFrame(self.root, text="Text Preview", padding=10)
        preview_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Text widget with scrollbar
        text_frame = tk.Frame(preview_frame)
        text_frame.pack(fill="both", expand=True)
        
        self.text_widget = tk.Text(
            text_frame,
            wrap="word",
            width=60,
            height=10,
            font=("Arial", 10),
            state="disabled"
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        self.text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initially disable buttons
        self.toggle_buttons(False)
    
    def toggle_buttons(self, enabled):
        """Enable or disable control buttons"""
        state = "normal" if enabled else "disabled"
        self.read_current_button.config(state=state)
        self.read_all_button.config(state=state)
        self.save_audio_button.config(state=state)
        if not self.audio_converter.is_busy():
            self.stop_button.config(state="disabled")
    
    def browse_file(self):
        """Open file browser to select PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            self.load_pdf(file_path)
    
    def load_pdf(self, file_path):
        """Load PDF file and update GUI"""
        self.speaking_status.set("Loading PDF...")
        
        # Close previous PDF if any
        self.pdf_reader.close_pdf()
        
        success, message = self.pdf_reader.open_pdf(file_path)
        
        if success:
            self.selected_file_path.set(os.path.basename(file_path))
            self.total_pages.set(self.pdf_reader.total_pages)
            
            # Update page spinbox
            self.page_spinbox.config(to=self.pdf_reader.total_pages)
            self.current_page.set(1)
            
            # Load first page text
            self.load_page_text(0)
            
            # Enable buttons
            self.toggle_buttons(True)
            
            self.speaking_status.set("PDF loaded successfully")
            
        else:
            messagebox.showerror("Error", message)
            self.speaking_status.set("Failed to load PDF")
    
    def load_page_text(self, page_number):
        """Load and display text from specific page"""
        success, text = self.pdf_reader.get_page_text(page_number)
        
        if success:
            # Update text widget
            self.text_widget.config(state="normal")
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(1.0, text)
            self.text_widget.config(state="disabled")
            
            return text
        else:
            messagebox.showerror("Error", text)
            return None
    
    def on_page_change(self, *args):
        """Handle page number change"""
        try:
            page_num = self.current_page.get() - 1  # Convert to 0-based index
            if 0 <= page_num < self.pdf_reader.total_pages:
                self.load_page_text(page_num)
        except:
            pass
    
    def read_current_page(self):
        """Read current page aloud"""
        if self.audio_converter.is_busy():
            messagebox.showwarning("Warning", "Already reading. Please stop current reading first.")
            return
        
        page_num = self.current_page.get() - 1
        text = self.load_page_text(page_num)
        
        if text:
            self.speaking_status.set("Reading current page...")
            self.stop_button.config(state="normal")
            
            # Start reading in separate thread
            threading.Thread(
                target=self._read_text_async,
                args=(text, "current page"),
                daemon=True
            ).start()
    
    def read_all_pages(self):
        """Read all pages aloud"""
        if self.audio_converter.is_busy():
            messagebox.showwarning("Warning", "Already reading. Please stop current reading first.")
            return
        
        success, text = self.pdf_reader.get_all_text()
        
        if success:
            self.speaking_status.set("Reading all pages...")
            self.stop_button.config(state="normal")
            
            # Start reading in separate thread
            threading.Thread(
                target=self._read_text_async,
                args=(text, "all pages"),
                daemon=True
            ).start()
        else:
            messagebox.showerror("Error", text)
    
    def _read_text_async(self, text, description):
        """Read text asynchronously"""
        try:
            success, message = self.audio_converter.speak_text(text, blocking=True)
            
            # Update status on main thread
            self.root.after(0, self._update_status_after_reading, success, message, description)
            
        except Exception as e:
            self.root.after(0, self._update_status_after_reading, False, str(e), description)
    
    def _update_status_after_reading(self, success, message, description):
        """Update status after reading completion"""
        if success:
            self.speaking_status.set(f"Finished reading {description}")
        else:
            self.speaking_status.set(f"Error reading {description}: {message}")
        
        self.stop_button.config(state="disabled")
    
    def stop_reading(self):
        """Stop current reading"""
        if self.audio_converter.stop_speech():
            self.speaking_status.set("Reading stopped")
            self.stop_button.config(state="disabled")
    
    def save_audio_file(self):
        """Save current page or all pages as audio file"""
        if self.pdf_reader.total_pages == 0:
            messagebox.showwarning("Warning", "No PDF loaded")
            return
        
        # Ask user what to save
        choice = messagebox.askyesnocancel(
            "Save Audio",
            "Yes = Save current page\nNo = Save all pages\nCancel = Cancel"
        )
        
        if choice is None:  # Cancel
            return
        
        # Get text to save
        if choice:  # Yes - current page
            page_num = self.current_page.get() - 1
            success, text = self.pdf_reader.get_page_text(page_num)
            default_name = f"page_{self.current_page.get()}"
        else:  # No - all pages
            success, text = self.pdf_reader.get_all_text()
            default_name = "audiobook"
        
        if not success:
            messagebox.showerror("Error", text)
            return
        
        # Get save location
        filename = filedialog.asksaveasfilename(
            title="Save Audio File",
            defaultextension=".wav",
            initialfile=default_name,
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        
        if filename:
            self.speaking_status.set("Saving audio file...")
            
            # Save in separate thread
            threading.Thread(
                target=self._save_audio_async,
                args=(text, filename),
                daemon=True
            ).start()
    
    def _save_audio_async(self, text, filename):
        """Save audio file asynchronously"""
        success, message = self.audio_converter.save_to_audio_file(text, filename)
        
        # Update status on main thread
        self.root.after(0, self._update_status_after_saving, success, message)
    
    def _update_status_after_saving(self, success, message):
        """Update status after saving completion"""
        if success:
            self.speaking_status.set(message)
            messagebox.showinfo("Success", message)
        else:
            self.speaking_status.set("Failed to save audio")
            messagebox.showerror("Error", message)
    
    def open_settings(self):
        """Open voice settings dialog"""
        SettingsDialog(self.root, self.audio_converter)
    
    def run(self):
        """Start the GUI main loop"""
        # Bind page change event
        self.current_page.trace("w", self.on_page_change)
        
        # Start main loop
        self.root.mainloop()
    
    def cleanup(self):
        """Cleanup resources"""
        self.audio_converter.cleanup()
        self.pdf_reader.close_pdf()


class SettingsDialog:
    def __init__(self, parent, audio_converter):
        self.parent = parent
        self.audio_converter = audio_converter
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Voice Settings")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.center_dialog()
        
        # Variables
        self.rate_var = tk.IntVar(value=150)
        self.volume_var = tk.DoubleVar(value=0.8)
        self.voice_var = tk.StringVar()
        
        # Get current settings
        self.load_current_settings()
        
        # Create widgets
        self.create_widgets()
    
    def center_dialog(self):
        """Center dialog on parent window"""
        self.dialog.update_idletasks()
        
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"+{x}+{y}")
    
    def load_current_settings(self):
        """Load current audio converter settings"""
        info = self.audio_converter.get_engine_info()
        if info:
            self.rate_var.set(info.get('rate', 150))
            self.volume_var.set(info.get('volume', 0.8))
    
    def create_widgets(self):
        """Create settings dialog widgets"""
        
        # Title
        title_label = tk.Label(
            self.dialog,
            text="Voice Settings",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=10)
        
        # Rate setting
        rate_frame = ttk.LabelFrame(self.dialog, text="Speaking Rate (WPM)", padding=10)
        rate_frame.pack(fill="x", padx=20, pady=10)
        
        rate_scale = tk.Scale(
            rate_frame,
            from_=50,
            to=300,
            variable=self.rate_var,
            orient="horizontal",
            length=300
        )
        rate_scale.pack()
        
        # Volume setting
        volume_frame = ttk.LabelFrame(self.dialog, text="Volume", padding=10)
        volume_frame.pack(fill="x", padx=20, pady=10)
        
        volume_scale = tk.Scale(
            volume_frame,
            from_=0.0,
            to=1.0,
            variable=self.volume_var,
            orient="horizontal",
            resolution=0.1,
            length=300
        )
        volume_scale.pack()
        
        # Voice selection
        voice_frame = ttk.LabelFrame(self.dialog, text="Voice", padding=10)
        voice_frame.pack(fill="x", padx=20, pady=10)
        
        voices = self.audio_converter.get_available_voices()
        if voices:
            voice_names = [f"{voice['name']}" for voice in voices]
            self.voice_combobox = ttk.Combobox(
                voice_frame,
                values=voice_names,
                state="readonly",
                width=40
            )
            self.voice_combobox.pack()
            if voice_names:
                self.voice_combobox.set(voice_names[0])
        else:
            tk.Label(voice_frame, text="No voices available").pack()
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        ttk.Button(
            button_frame,
            text="Apply",
            command=self.apply_settings
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="Test",
            command=self.test_voice
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="Close",
            command=self.dialog.destroy
        ).pack(side="right", padx=5)
    
    def apply_settings(self):
        """Apply selected settings"""
        # Apply rate
        self.audio_converter.set_voice_rate(self.rate_var.get())
        
        # Apply volume
        self.audio_converter.set_volume(self.volume_var.get())
        
        # Apply voice
        if hasattr(self, 'voice_combobox'):
            voice_index = self.voice_combobox.current()
            if voice_index >= 0:
                self.audio_converter.set_voice(voice_index)
        
        messagebox.showinfo("Settings", "Settings applied successfully!")
    
    def test_voice(self):
        """Test current voice settings"""
        self.apply_settings()
        
        test_text = "This is a test of the current voice settings."
        self.audio_converter.speak_text(test_text, blocking=False)
