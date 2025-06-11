# Chrome Dino Bot with Absolute Pixel Scan-Lines

A simple automation script that plays the Google Chrome Dino game by scanning raw pixel data—no machine learning required. It captures a defined screen region, detects obstacles and birds using a color-difference threshold, and triggers jumps or ducks with mouse clicks and keyboard presses. Designed to work on macOS (and should be easily adaptable to other platforms supported by PyAutoGUI).

## Features

* **Absolute Pixel Scan-Lines**: Scans specific rows inside the capture region for ground obstacles and birds.
* **Color-Difference Threshold**: Uses a tunable sensitivity value to detect objects against the background.
* **Jump Cooldown**: Prevents repeated jumps by enforcing a minimum wait time between actions.
* **Auto-Start & Quit**: Clicks to start the game automatically and listens for `q` to exit cleanly.
* **Test Screenshot**: Captures and saves one test screenshot (`dino_capture.png`) so you can verify your capture region.
* **Interactive Calibration**: Provides a terminal-based tool to measure absolute and relative pixel positions for fine-tuning.
* **macOS Support**: Tested on macOS using PyAutoGUI, Pillow, and Pynput.

## Requirements

* Python 3.x
* [PyAutoGUI](https://github.com/asweigart/pyautogui)
* [Pillow (PIL)](https://python-pillow.org/)
* [Pynput](https://pynput.readthedocs.io/)

Install dependencies:

```bash
pip install pyautogui pillow pynput
```

## Configuration

Adjust these values at the top of the script to match your display and browser window:

```python
CAP_X, CAP_Y, CAP_W, CAP_H = 144, 215, 750, 240  # Capture region
Y_GROUND_HIGH       = 177  # Row for obstacle tops
Y_GROUND_LOW        = 196  # Row just below ground
Y_BIRD              =  53  # Row for flying birds
X_LOOKAHEAD_START   = 30   # Start scanning this many pixels from left edge
X_LOOKAHEAD_END     = 120  # End scanning this many pixels from left edge
JUMP_COOLDOWN       = 0.15 # Seconds between jumps
COLOR_THRESHOLD     = 45   # Sensitivity for obstacle detection
```

## Interactive Calibration

If you're unsure about the correct pixel values, use the built-in calibration snippet. Run the following at the top of your script or in a separate file:

```python
import pyautogui as gui
import time

print("👉 Move your cursor over the point you want to measure, then press Ctrl+C to stop.")
try:
    while True:
        x, y = gui.position()
        rx, ry = x - CAP_X, y - CAP_Y
        print(f"abs=({x:4},{y:4})   rel=({rx:4},{ry:4})", end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nDone.")
    print(f"[INFO] Using capture {CAP_W}×{CAP_H}px. "
          f"Scanning ground at Y={Y_GROUND_HIGH},{Y_GROUND_LOW}, "
          f"bird at Y={Y_BIRD}, X={X_LOOKAHEAD_START}→{X_LOOKAHEAD_END}")
    print("[INFO] Press 'q' to quit.")
```

* **Absolute coordinates** (`abs`) are your screen's pixel positions.
* **Relative coordinates** (`rel`) are positions inside your defined capture region (use these to adjust your config values).

Move your mouse to the desired point, watch the terminal for the printed values, and update the constants accordingly.

## Usage

1. Open Chrome and navigate to `chrome://dino`.

2. Focus the Dino window, then run:

   ```bash
   python dino_bot.py
   ```

3. You have **3 seconds** to click or focus the game window.

4. A test screenshot will be saved as `dino_capture.png`—verify that the capture region is correct.

5. The script will auto-start the game, jump over cacti, and duck under birds.

6. Press `q` in the terminal to quit cleanly.

## License

This project is released under the [MIT License](LICENSE).

---

*Enjoy! Have fun and watch the Dino run.*
