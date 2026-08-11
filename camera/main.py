import sys
import time
import st7789
from PIL import Image, ImageDraw, ImageFont

# -------------------------------------------------------------------
# Configuration & Hardware Definitions
# -------------------------------------------------------------------
WIDTH = 240
HEIGHT = 320

PORT = 0         # SPI0
CS = 0           # CE0 (GPIO 8)
DC = 25          # Data/Command (GPIO 25)
RST = 27         # Reset (GPIO 27)
BL = 18          # Waveshare default Backlight (GPIO 18)
ROTATION = 0     # 0 or 180 (portrait), 90 or 270 (landscape)

print("=" * 50)
print("[DEBUG] Starting Waveshare 2inch ST7789 Initialization")
print("=" * 50)
print(f"[DEBUG] Target Resolution : {WIDTH}x{HEIGHT}")
print(f"[DEBUG] SPI Bus/Device    : Port {PORT}, CS {CS}")
print(f"[DEBUG] Control Pins      : DC=GPIO{DC}, RST=GPIO{RST}, BL=GPIO{BL}")

# -------------------------------------------------------------------
# Display Initialization
# -------------------------------------------------------------------
try:
    print("[DEBUG] Instantiating ST7789 display driver object...")
    disp = st7789.ST7789(
        port=PORT,
        cs=CS,
        dc=DC,
        rst=RST,
        backlight=BL,
        rotation=ROTATION,
        width=WIDTH,
        height=HEIGHT,
        offset_left=0,
        offset_top=0
    )
    print("[DEBUG] Display object instantiated successfully.")

    print("[DEBUG] Opening SPI bus and running display reset sequence...")
    disp.begin()
    print("[DEBUG] Display communication initialized! Backlight should be ON.")

except PermissionError:
    print("\n[ERROR] Permission denied! Try running the script with sudo:")
    print(f"        sudo python3 {sys.argv[0]}")
    sys.exit(1)
except FileNotFoundError:
    print("\n[ERROR] SPI device node not found (/dev/spidev0.0).")
    print("        Ensure SPI is enabled via 'sudo raspi-config' -> Interface Options -> SPI.")
    sys.exit(1)
except Exception as e:
    print(f"\n[ERROR] Failed to initialize ST7789 display: {e}")
    sys.exit(1)

# -------------------------------------------------------------------
# Canvas Creation & Rendering
# -------------------------------------------------------------------
try:
    print(f"\n[DEBUG] Creating PIL canvas with size ({disp.width}, {disp.height})...")
    image = Image.new("RGB", (disp.width, disp.height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)

    print("[DEBUG] Loading default font and rendering test shapes...")
    font = ImageFont.load_default()

    # Draw test elements
    draw.rectangle((10, 10, disp.width - 10, 60), fill=(255, 0, 0), outline=(255, 255, 255))
    draw.text((20, 25), "Waveshare 2inch Ready!", font=font, fill=(255, 255, 255))
    draw.rectangle((20, 80, disp.width - 20, disp.height - 20), fill=(0, 0, 255))

    print(f"[DEBUG] Pillow Canvas generated: Mode={image.mode}, Size={image.size}")
    
    print("[DEBUG] Sending image buffer to ST7789 display over SPI...")
    start_time = time.time()
    disp.display(image)
    render_time = (time.time() - start_time) * 1000
    
    print(f"[DEBUG] Frame transfer complete in {render_time:.2f} ms.")
    print("=" * 50)
    print("[SUCCESS] Display updated! You should see text and shapes on screen.")
    print("=" * 50)

except Exception as e:
    print(f"\n[ERROR] Exception occurred during image rendering/display: {e}")