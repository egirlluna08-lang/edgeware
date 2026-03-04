# edgeware

Opens images in rapid succession. One new window every 1.5 seconds, keeps max 20 windows open at once.

## Requirements

- Python 3.7+
- Pillow (PIL)

## Installation & Usage

### Windows & Mac

1. Make sure you have Python 3.7+ installed
2. Install dependencies:
   ```
   pip install Pillow
   ```
3. Run:
   ```
   python edgeware.py
   ```

That's it. Windows will start opening automatically.

## What It Does

- Opens images from the `images/` folder
- One new window opens every 1.5 seconds
- Keeps a max of 20 windows open at once
- When window limit reached, oldest window closes automatically
- Loops forever through all images
- Skips the first 15 images

## Control

- Close any window normally
- Close the console/terminal to stop the app entirely

---

Made with ❤️
