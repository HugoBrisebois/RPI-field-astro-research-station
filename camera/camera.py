from picamera2 import Picamera2
from libcamera import controls
import time


# configuring the rpi camera module 3
# to be able to capture and display the various images 
# captured by the camera
picam = Picamera2()
config = picam.create_preview_configuration(main={"size": (1280, 960)})
picture = picam.create_still_configuration(main={"size": (4608, 2592)})
picam.configure(config)
picam.configure(picture)
# set global variables for the camera settings
exposure = 2.0   # 2 second frameing preview
gain = 8.0       # amplify the sensor signal

picam.set_controls({
    "AfMode": controls.AfModeEnum.Manual,
    "LensPosition": 0.0,      # Set Focus to infinity
    "AeEnable": False,        # Enable manual shutter mode so that the camera doesn't auto adjust brightness
    "ExposureTime": exposure,
    "AnalogueGain": gain
})

picam.start()


# capturing an image

time.sleep(1)
image = picam.capture_image("main.jpg")
