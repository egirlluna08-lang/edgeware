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
            
            # Track window
            window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(window))
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
    
    def run(self):
        """Keep the app running"""
        # Create invisible root window to keep app alive
        root = tk.Tk()
        root.withdraw()
        root.geometry("1x1+0+0")
        
        def on_closing():
            self.running = False
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        try:
            root.mainloop()
        except KeyboardInterrupt:
            self.running = False

if __name__ == "__main__":
    app = EdgewareApp()
    app.run()
