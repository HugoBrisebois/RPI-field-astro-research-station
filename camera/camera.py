from picamera2 import Picamera2, Preview

picam = Picamera2()
picam.start_preview(Preview.DRM)
