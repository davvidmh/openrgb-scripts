import sys
import time
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

# Colors
PURE_WHITE = RGBColor(255, 255, 255)
# Frosted pump diffusers absorb blue light, so compensate with cool white
AIO_COOL_WHITE = RGBColor(100, 180, 255)


def connect(retries=5):
    for i in range(retries):
        try:
            return OpenRGBClient()
        except Exception:
            time.sleep(1)
    return None


def main():
    cli = connect()
    if not cli:
        print("Error: Could not connect to OpenRGB. Is the SDK server running?")
        sys.exit(1)

    print(f"Connected. Found {len(cli.devices)} devices:")

    for dev in cli.devices:
        name_lower = dev.name.lower()
        print(f" - {dev.name} ({dev.type})")

        # Use cool white for AIO pump, pure white for everything else
        target = AIO_COOL_WHITE if ("strix lc" in name_lower or "aio" in name_lower) else PURE_WHITE

        # Resize ARGB header on motherboard if needed
        if "motherboard" in name_lower or "b550" in name_lower or "prime" in name_lower:
            for z in dev.zones:
                if "addressable" in z.name.lower() and len(z.leds) < 60:
                    try:
                        z.resize(120)
                    except Exception:
                        pass

        # Switch to Direct or Static mode
        modes = [m.name for m in dev.modes]
        if "Direct" in modes:
            try:
                dev.set_mode("Direct")
            except Exception:
                pass
        elif "Static" in modes:
            try:
                dev.set_mode("Static")
            except Exception:
                pass

        # Apply color
        try:
            dev.set_color(target)
            for z in dev.zones:
                z.set_color(target)
        except Exception as e:
            print(f"   warning setting {dev.name}: {e}")

    try:
        cli.save_profile("White")
        print("\nSaved profile 'White'.")
    except Exception:
        pass


if __name__ == "__main__":
    main()
