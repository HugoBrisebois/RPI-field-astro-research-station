import st7789
from PIL import Image, ImageDraw, ImageFont

# Display Dimensions
WIDTH = 240
HEIGHT = 240

# Initialize ST7789 with explicit parameters
disp = st7789.ST7789(
    port=0,           # SPI port (SPI0 = 0)
    cs=0,             # Chip Select / CE pin (0 for CE0 / GPIO 8, 1 for CE1 / GPIO 7)
    dc=25,            # Data/Command pin (GPIO 25)
    rst=27,           # Reset pin (GPIO 27)
    backlight=24,     # Backlight PWM pin (GPIO 24) — set to None if connected to 3.3V
    rotation=90,      # Orientation: 0, 90, 180, or 270
    width=WIDTH,      # Screen width in pixels
    height=HEIGHT,    # Screen height in pixels
    offset_left=0,    # Horizontal pixel offset (adjust if screen edges are cropped)
    offset_top=0      # Vertical pixel offset (adjust if screen edges are cropped)
)

# Start communication with the display
disp.begin()

# Create a PIL canvas matching screen dimensions
image = Image.new("RGB", (disp.width, disp.height), color=(0, 0, 0))
draw = ImageDraw.Draw(image)

# Load font (uses PIL default)
font = ImageFont.load_default()

# Draw elements on canvas
draw.rectangle((10, 10, disp.width - 10, 60), fill=(255, 0, 0), outline=(255, 255, 255))
draw.text((20, 25), "ST7789 Ready!", font=font, fill=(255, 255, 255))
draw.rectangle((20, 80, 120, 180), fill=(0, 0, 255))

# Push image to the physical screen
disp.display(image)