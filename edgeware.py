#!/usr/bin/env python3
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import os
import sys
import threading
import time
import random
from pathlib import Path

class EdgewareApp:
    def __init__(self):
        self.windows = []
        self.image_files = []
        self.current_index = 0
        self.running = True
        self.code_input = ""
        self.unlock_code = "6767"
        self.root = None
        self.unlock_window = None
        
        # Find images folder
        script_dir = Path(__file__).parent.absolute()
        self.images_dir = script_dir / "images"
        
        if not self.images_dir.exists():
            print(f"Error: images folder not found at {self.images_dir}")
            sys.exit(1)
        
        self.load_images()
        
        if not self.image_files:
            print("Error: No images found in images folder")
            sys.exit(1)
        
        print(f"Found {len(self.image_files)} images")
        self.start_loop()
    
    def load_images(self):
        """Load images, skipping first 15"""
        all_images = []
        for f in self.images_dir.iterdir():
            if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                all_images.append(f)
        
        # Sort by number in filename
        all_images.sort(key=lambda x: int(x.stem.replace('pic', '') or 0))
        
        # Skip first 15
        self.image_files = all_images[15:] if len(all_images) > 15 else all_images
    
    def open_window(self, image_path):
        """Open a new window with an image"""
        try:
            window = tk.Toplevel()
            window.geometry("600x600")
            window.title("edgeware")
            
            # Random position
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = random.randint(0, max(0, screen_width - 600))
            y = random.randint(0, max(0, screen_height - 600))
            window.geometry(f"600x600+{x}+{y}")
            
            # Load and display image
            img = Image.open(image_path)
            img.thumbnail((600, 600), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            label = tk.Label(window, image=photo, bg="black")
            label.image = photo  # Keep a reference
            label.pack(fill=tk.BOTH, expand=True)
            
            # Block closing - show unlock dialog instead
            def block_close():
                self.show_unlock_dialog()
            
            window.protocol("WM_DELETE_WINDOW", block_close)
            
            # Listen for any key press to show unlock dialog
            window.bind('<Key>', lambda e: self.show_unlock_dialog())
            
            self.windows.append(window)
            
            return window
        except Exception as e:
            print(f"Error opening image {image_path}: {e}")
    
    def close_window(self, window):
        """Close a window and remove from tracking"""
        try:
            if window in self.windows:
                self.windows.remove(window)
            window.destroy()
        except:
            pass
    
    def start_loop(self):
        """Start the main loop in a separate thread"""
        thread = threading.Thread(target=self.loop, daemon=True)
        thread.start()
    
    def loop(self):
        """Main loop - open images every 1.5 seconds"""
        time.sleep(0.5)  # Small delay to let first window open
        
        while self.running:
            try:
                # If 20+ windows, close the oldest
                while len(self.windows) >= 20:
                    oldest = self.windows.pop(0)
                    try:
                        oldest.destroy()
                    except:
                        pass
                
                # Open next image
                if self.image_files:
                    image_path = self.image_files[self.current_index]
                    self.open_window(image_path)
                    self.current_index = (self.current_index + 1) % len(self.image_files)
                
                time.sleep(1.5)
            except Exception as e:
                print(f"Loop error: {e}")
                time.sleep(1)
    
    def show_unlock_dialog(self, event=None):
        """Show unlock dialog that requires code"""
        # Don't show multiple dialogs
        if self.unlock_window:
            try:
                if self.unlock_window.winfo_exists():
                    self.unlock_window.focus()
                    return
            except:
                pass
        
        unlock_win = tk.Toplevel()
        self.unlock_window = unlock_win
        unlock_win.geometry("300x150")
        unlock_win.title("LOCKED")
        unlock_win.configure(bg="black")
        unlock_win.resizable(False, False)
        
        # Make window stay on top
        unlock_win.attributes('-topmost', True)
        
        label = tk.Label(unlock_win, text="UNLOCK CODE:", fg="#ff1493", bg="black", font=("Arial", 12, "bold"))
        label.pack(pady=10)
        
        code_display = tk.Label(unlock_win, text="", fg="#00ff00", bg="black", font=("Courier", 24, "bold"))
        code_display.pack(pady=5)
        
        def check_code(event=None):
            if self.code_input == self.unlock_code:
                self.code_input = ""
                code_display.config(text="")
                unlock_win.destroy()
                self.unlock_window = None
                self.running = False
                for win in self.windows:
                    try:
                        win.destroy()
                    except:
                        pass
                if self.root:
                    self.root.destroy()
            elif len(self.code_input) >= len(self.unlock_code):
                self.code_input = ""
                code_display.config(text="WRONG")
                unlock_win.after(500, lambda: code_display.config(text=""))
        
        def on_key(event):
            if event.char.isdigit():
                self.code_input += event.char
                code_display.config(text="●" * len(self.code_input))
                if len(self.code_input) == len(self.unlock_code):
                    check_code()
        
        unlock_win.bind('<Key>', on_key)
        unlock_win.focus()
        
        return unlock_win
    
    def run(self):
        """Keep the app running"""
        # Create invisible root window to keep app alive
        root = tk.Tk()
        self.root = root
        root.withdraw()
        root.geometry("1x1+0+0")
        
        # Block normal window closing by showing unlock dialog
        def on_closing():
            self.show_unlock_dialog()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        try:
            root.mainloop()
        except KeyboardInterrupt:
            self.show_unlock_dialog()

if __name__ == "__main__":
    app = EdgewareApp()
    app.run()
