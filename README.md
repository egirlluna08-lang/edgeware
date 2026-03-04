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

## LOCKED MODE

**The app is locked by default.** You cannot close windows normally.

**To unlock and exit:**
1. Press any key on one of the image windows
2. A black dialog box appears asking for "UNLOCK CODE"
3. Type the code: `6767`
4. If correct, all windows close and the app exits
5. If wrong, it will show "WRONG" and clear the input

**That's it.** The entire app is locked down - no clicking X buttons, no escape key, nothing works until you enter the code.

---

Made with ❤️
