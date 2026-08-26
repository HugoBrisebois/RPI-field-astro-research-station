from picamera2 import Picamera2
from libcamera import controls
import time


# configuring the rpi camera module 3
# to be able to capture and display the various images 
# captured by the camera
picam = Picamera2()
capture_config = picam.create_still_configuration(main={"size": (1280, 960)})


# set global variables for the camera settings
exposure = 2000000   # 2 second frameing preview
gain = 8.0       # amplify the sensor signal

picam.set_controls({
    "AfMode": controls.AfModeEnum.Manual,   "LensPosition": 0.0,      # Set Focus to infinity
    "AeEnable": False,        # Enable manual shutter mode so that the camera doesn't auto adjust brightness
    "ExposureTime": exposure,
    "AnalogueGain": gain
})

picam.start()


# capturing an image

time.sleep(1)
image = picam.capture_file(capture_config, "test.jpeg")


# stop the camera
picam.stop()