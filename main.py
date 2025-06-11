#!/usr/bin/env python3
"""
Chrome Dino bot with absolute pixel scan‐lines:

1. Takes & saves one test screenshot (dino_capture.png) & opens it.
2. Auto-starts the game with Space.
3. Uses a color-difference threshold.
4. Enforces a jump cooldown.
5. Quits on 'q'.
"""

import pyautogui as gui
from PIL import Image
import time
import math
from pynput.keyboard import Key, Controller, Listener

# ─── CONFIG ───────────────────────────────────────────────────────────
CAP_X, CAP_Y, CAP_W, CAP_H = 144, 215, 750, 240  # your tuned capture region



# Absolute scan‐lines *inside* that 605×160 capture:
Y_GROUND_HIGH       = 177  # e.g. row where the top of cacti live
Y_GROUND_LOW        = 196  # e.g. row just below
Y_BIRD              =  53  # row where birds fly

X_LOOKAHEAD_START   = 30  # how many pixels in from the left edge
X_LOOKAHEAD_END     = 120  # how far out to scan

JUMP_COOLDOWN       = 0.15   # min seconds between jumps
COLOR_THRESHOLD     = 45     # obstacle detection sensitivity
# ─────────────────────────────────────────────────────────────────────

exit_flag = False

def on_press(key):
    global exit_flag
    try:
        if key.char == 'q':
            exit_flag = True
            return False
    except AttributeError:
        pass

def color_diff(c1, c2):
    return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]) + abs(c1[2]-c2[2])

def start():
    global exit_flag

    listener = Listener(on_press=on_press)
    listener.start()

    # 1) Give you 3s to focus the Dino window
    time.sleep(3)

    # 2) Snap & show one test screenshot
    test_img = gui.screenshot(region=(CAP_X, CAP_Y, CAP_W, CAP_H))
    test_img.save("dino_capture.png")
    print("[INFO] Saved test screenshot as dino_capture.png")
    test_img.show()

    # 3) Auto-start the game with a click instead of space
    gui.click(x=CAP_X + CAP_W // 2, y=CAP_Y + CAP_H // 2)

    print(f"[INFO] Using capture {CAP_W}×{CAP_H}px. "
          f"Scanning ground at Y={Y_GROUND_HIGH},{Y_GROUND_LOW}, "
          f"bird at Y={Y_BIRD}, X={X_LOOKAHEAD_START}→{X_LOOKAHEAD_END}")
    print("[INFO] Press 'q' to quit.")

    last_jump = 0

    # 4) Main loop
    while not exit_flag:
        frame = gui.screenshot(region=(CAP_X, CAP_Y, CAP_W, CAP_H))
        bg = frame.getpixel((5, 5))
        now = time.time()

        if now - last_jump > JUMP_COOLDOWN:
            for sx in range(X_LOOKAHEAD_START, X_LOOKAHEAD_END):
                # ground obstacle?
                ph = frame.getpixel((sx, Y_GROUND_HIGH))
                pl = frame.getpixel((sx, Y_GROUND_LOW))
                if (color_diff(ph, bg) > COLOR_THRESHOLD or
                    color_diff(pl, bg) > COLOR_THRESHOLD):
                    # LEFT-CLICK jump
                    gui.click(x=CAP_X + CAP_W // 2, y=CAP_Y + CAP_H // 2)
                    last_jump = now
                    break

                # bird?
                pb = frame.getpixel((sx, Y_BIRD))
                if color_diff(pb, bg) > COLOR_THRESHOLD:
                    kb = Controller()
                    kb.press(Key.down)
                    time.sleep(0.3)
                    kb.release(Key.down)
                    last_jump = now
                    break

        time.sleep(0.005)

    listener.join()
    print("Exited cleanly.")

if __name__ == "__main__":
    start()
