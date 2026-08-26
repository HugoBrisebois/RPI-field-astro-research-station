import time
import RPi.GPIO as GPIO
import spidev
from PIL import Image, ImageDraw, ImageFont

# --- Pin Definitions (Physical Header Pins to GPIO) ---
RST_PIN = 27  # Physical Pin 13
DC_PIN  = 25  # Physical Pin 22
BL_PIN  = 18  # Physical Pin 12
CS_BUS  = 0
CS_DEV  = 0   # GPIO 8 (CE0 / Physical Pin 24)

# --- Initialize GPIO ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RST_PIN, GPIO.OUT)
GPIO.setup(DC_PIN, GPIO.OUT)
GPIO.setup(BL_PIN, GPIO.OUT)

# Turn on Backlight
GPIO.output(BL_PIN, GPIO.HIGH)

# --- Initialize SPI ---
spi = spidev.SpiDev()
spi.open(CS_BUS, CS_DEV)
spi.max_speed_hz = 40000000  # 40 MHz
spi.mode = 0b00             # Mode 0 (CPOL=0, CPHA=0)

def send_command(cmd):
    GPIO.output(DC_PIN, GPIO.LOW)  # LOW = Command
    spi.writebytes([cmd])

def send_data(data):
    GPIO.output(DC_PIN, GPIO.HIGH) # HIGH = Data
    if isinstance(data, int):
        spi.writebytes([data])
    else:
        spi.writebytes(data)

def reset_display():
    GPIO.output(RST_PIN, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(RST_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(RST_PIN, GPIO.HIGH)
    time.sleep(0.1)

def init_st7789():
    """Initializes ST7789 display registers for 240x320 resolution."""
    reset_display()

    send_command(0x11)  # Sleep Out
    time.sleep(0.12)

    send_command(0x36)  # MADCTL (Memory Data Access Control)
    send_data(0x00)     # Portrait mode RGB order

    send_command(0x3A)  # COLMOD (Interface Pixel Format)
    send_data(0x05)     # 16-bit/pixel (RGB565)

    send_command(0xB2)  # PORCTRL (Porch Setting)
    send_data([0x0C, 0x0C, 0x00, 0x33, 0x33])

    send_command(0xB7)  # GCTRL (Gate Control)
    send_data(0x35)

    send_command(0xBB)  # VCOMS (VCOM Setting)
    send_data(0x19)

    send_command(0xC0)  # LCMCTRL
    send_data(0x2C)

    send_command(0xC2)  # VDVVRHEN
    send_data(0x01)

    send_command(0xC3)  # VRHS
    send_data(0x12)

    send_command(0xC4)  # VDVS
    send_data(0x20)

    send_command(0xC6)  # FRCTRL2 (Frame Rate Control)
    send_data(0x0F)

    send_command(0xD0)  # PWCTRL1 (Power Control 1)
    send_data([0xA4, 0xA1])

    send_command(0x21)  # Display Inversion ON (Needed for proper colors on Waveshare)

    send_command(0x29)  # Display ON
    time.sleep(0.05)

def display_image(img):
    """Converts a PIL RGB Image into RGB565 bytes and writes to display."""
    # ST7789 expects 240x320 resolution
    img = img.resize((320, 240))
    
    # Set Address Window to Full Screen
    send_command(0x2A)  # Column Address Set
    send_data([0x00, 0x00, 0x00, 239])

    send_command(0x2B)  # Row Address Set
    send_data([0x00, 0x00, 0x01, 0x3F]) # 319 = 0x013F

    send_command(0x2C)  # Memory Write

    # Convert PIL Image to RGB565 Byte Array
    pixels = img.getdata()
    buf = bytearray(320 * 240 * 2)
    idx = 0
    for r, g, b in pixels:
        # Convert RGB888 to RGB565
        rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        buf[idx] = (rgb565 >> 8) & 0xFF
        buf[idx + 1] = rgb565 & 0xFF
        idx += 2

    # Send pixel buffer over SPI in chunks
    GPIO.output(DC_PIN, GPIO.HIGH)
    chunk_size = 4096
    for i in range(0, len(buf), chunk_size):
        spi.writebytes(list(buf[i:i + chunk_size]))

try:
    print("Initializing ST7789 Display...")
    init_st7789()

    # display an image to the display taken by the camera
    image_path = "test.jpeg"
    image = Image.open(image_path).convert("RGB")

    # Debug
    print(f"displaying {image_path}")
    display_image(image)
    print("Success")

    # Keep script alive so display stays on
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting and cleaning up GPIO...")
    spi.close()
    GPIO.cleanup()