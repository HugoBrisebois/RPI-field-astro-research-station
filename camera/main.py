import picamera2
import adafruit_st7789
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont

print("starting up the device ...")

# setting up the lcd for displaying properties
def init_lcd():
    # Hardware SPI configuration.
    spi = board.SPI()
    
    # Define pins
    tft_cs = digitalio.DigitalInOut(board.D8)
    tft_dc = digitalio.DifitalInOut(board.D25)
    tft_reset = digitalio.DigitalInOut(board.D27)
    
    # Create the ST7789 display object (240*240)
    display = adafruit_st7789.ST7789(
        spi,
        cs=tft_cs,
        dc=tft_dc,
        rst=tft_reset,
        baudrate=64000000,
        width=240,
        hight=240,
        x_offset=0,
        y_offset=0,
    )
    
    #Create a blank image canvas using PIL (Pillow)
    image = Image.new("RGB", (display.width, display.height), (0, 0, 0,))
    draw = Image.Draw(image)
    
    # Draw shapes and text on he PIL canvas 
    draw.rectangle((20, 20, 120, 70), fill= (255, 0, 0)) # Red rectangle
    text((30, 100), "Hello Python!", fill=(255, 255, 255)) # White text
    
   #Push the canvas to the display
   display.image(image)
    