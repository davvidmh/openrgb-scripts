import math
import sys
import time
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor


def get_client():
    try:
        return OpenRGBClient()
    except Exception:
        print("Error: Could not connect to OpenRGB.")
        return None


def waterfall(speed=0.08):
    cli = get_client()
    if not cli:
        return

    print("Running waterfall effect. Press Ctrl+C to stop.")
    for d in cli.devices:
        if "Direct" in [m.name for m in d.modes]:
            try:
                d.set_mode("Direct")
            except Exception:
                pass

    step = 0
    try:
        while True:
            for d in cli.devices:
                n = len(d.leds)
                if n == 0:
                    continue
                colors = []
                for i in range(n):
                    pos = (i - step) % max(n, 8)
                    val = 255 if pos == 0 else (160 if pos == 1 else (60 if pos == 2 else 10))
                    colors.append(RGBColor(val, val, val))
                try:
                    d.set_colors(colors)
                except Exception:
                    pass
            step += 1
            time.sleep(speed)
    except KeyboardInterrupt:
        print("\nStopped.")


def breathing(speed=0.05):
    cli = get_client()
    if not cli:
        return

    print("Running breathing effect. Press Ctrl+C to stop.")
    t = 0
    try:
        while True:
            f = 0.55 + 0.45 * math.sin(t)
            t += speed
            v = int(255 * f)
            c = RGBColor(v, v, v)
            for d in cli.devices:
                try:
                    d.set_color(c, fast=True)
                except Exception:
                    pass
            time.sleep(0.04)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "waterfall"
    if mode == "breathing":
        breathing()
    else:
        waterfall()
