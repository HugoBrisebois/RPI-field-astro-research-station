from picamera2 import Picamera2, Preview


# configuring the camera for start
picam = Picamera2()
config = picam.create_preview_configuration()
picam.configure(config)

# start the pi camera module  
picam.start()
