import sys
import time
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

PURE_WHITE = RGBColor(255, 255, 255)
AIO_COOL_WHITE = RGBColor(100, 180, 255)


def run_keeper(interval=15):
    print(f"Keeper daemon running (pings every {interval}s). Press Ctrl+C to stop.")
    while True:
        try:
            cli = OpenRGBClient()
            for dev in cli.devices:
                name_lower = dev.name.lower()
                target = AIO_COOL_WHITE if ("strix lc" in name_lower or "aio" in name_lower) else PURE_WHITE
                
                modes = [m.name for m in dev.modes]
                if "Direct" in modes:
                    try:
                        dev.set_mode("Direct")
                    except Exception:
                        pass

                try:
                    dev.set_color(target)
                except Exception:
                    pass
        except Exception:
            pass
        time.sleep(interval)


if __name__ == "__main__":
    secs = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    try:
        run_keeper(secs)
    except KeyboardInterrupt:
        print("\nStopped.")
