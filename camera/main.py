import ST7789
from PIL import Image, ImageDraw

# 1. Initialize display (auto-configures standard Pi SPI pins: CE0, GPIO 25 DC, GPIO 27 Reset)
disp = ST7789.ST7789(width=240, height=240, rotation=90)
disp.begin()

# 2. Create canvas
image = Image.new("RGB", (240, 240), color=(0, 0, 0))
draw = ImageDraw.Draw(image)

# 3. Draw something
draw.text((20, 20), "Hello World!", fill=(255, 255, 255))
draw.rectangle((20, 50, 100, 100), fill=(255, 0, 0))

# 4. Show on screen
disp.display(image)