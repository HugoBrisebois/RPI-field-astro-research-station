import st7789
from PIL import Image, ImageDraw, ImageFont

# Waveshare 2inch screen resolution
WIDTH = 240
HEIGHT = 320

# Initialized specifically for Waveshare 2inch LCD pinout
disp = st7789.ST7789(
    port=0,           # SPI0 bus
    cs=0,             # CE0 (GPIO 8 / Pin 24)
    dc=25,            # Data/Command (GPIO 25 / Pin 22)
    rst=27,           # Reset (GPIO 27 / Pin 13)
    backlight=18,     # Waveshare default BL pin (GPIO 18 / Pin 18)
    rotation=0,       # 0 or 180 for portrait, 90 or 270 for landscape
    width=WIDTH,      # 240 px
    height=HEIGHT,    # 320 px
    offset_left=0,
    offset_top=0
)

disp.begin()

# Create canvas matching 240x320
image = Image.new("RGB", (disp.width, disp.height), color=(0, 0, 0))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()

# Draw on full 240x320 canvas
draw.rectangle((10, 10, disp.width - 10, 60), fill=(255, 0, 0), outline=(255, 255, 255))
draw.text((20, 25), "Waveshare 2inch Ready!", font=font, fill=(255, 255, 255))
draw.rectangle((20, 80, 220, 300), fill=(0, 0, 255))

disp.display(image)