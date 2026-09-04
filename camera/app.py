# web app imports
from flask import Flask
from flask import render_template
from markupsafe import escape

# camera imports
from picamera2 import Picamera2
from libcamera import controls
import time

def capture_image():
    pass    

















app = Flask(__name__)

@app.route("/")
def Index():
    return 'Index Page'

