# openrgb-scripts

A few Python scripts and Windows batch files I put together to manage my PC's RGB setup with OpenRGB.

My hardware:
- Asus ROG Strix LC AIO
- Gigabyte RTX 3070 Gaming OC
- Corsair Dominator Platinum DDR4
- Asus Prime B550M-A motherboard
- Razer peripherals (mouse, keyboard, pad)

The main goal was keeping everything on a clean static white and fixing a few annoying issues (GPU resetting to blue, AIO acrylic looking yellow, Armoury Crate services locking the bus).

## What's in here

- `sync_white.py` - Connects to OpenRGB SDK and sets all detected devices to white. Calibrates the AIO color slightly cool so the pump's frosted acrylic actually looks white instead of warm/cream. Also resizes the motherboard ARGB zone to 120 LEDs.
- `keeper.py` - Lightweight daemon that keeps pinging the GPU every 15s to prevent Gigabyte's firmware watchdog from turning the logo back to default blue.
- `effects.py` - Simple waterfall / rain drop animation and breathing effect using the SDK.
- `run_admin.bat` - Kills leftover Asus Armoury Crate processes that lock the SMBus, starts the PawnIO service, and launches OpenRGB as admin so the Corsair RAM gets detected properly.
- `clean_asus.bat` - Stops and disables the leftover Asus background services.

## Setup

1. Install [OpenRGB](https://openrgb.org/) (tested on v1.0).
2. On Windows, install [PawnIO](https://pawnio.eu/) if you need DDR4/DDR5 SMBus control.
3. Install the Python client:
   ```bash
   pip install openrgb-python
   ```
4. Start OpenRGB with the SDK server enabled (`OpenRGB.exe --server` or check the box in OpenRGB settings).
5. Run:
   ```bash
   python sync_white.py
   ```

## A few notes from my build

- **Corsair RAM not showing up?** OpenRGB needs admin rights to talk to PawnIO on Windows, and Asus Armoury Crate (`asus_framework.exe`) locks the I2C bus. `run_admin.bat` takes care of killing those and launching with the right permissions.
- **AIO looking yellowish?** Frosted pump diffusers absorb cool light. Setting pure `255, 255, 255` looked creamy on my ROG LC, so the script uses a cooler blue-white curve (`100, 180, 255`) on the pump which refracts as pure neutral white.
- **Motherboard orange line:** On the Asus Prime B550M-A, the audio trace LED is physically amber-only (not RGB). If you want 100% white with no orange, disable "Audio Lighting" in BIOS (Advanced > Onboard Devices Configuration).

## License

MIT
