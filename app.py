#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, url_for, redirect

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html', stat=0)

def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/power/<int:state>')
def power_control(state):
    if state == 0:
        print("power off")
        return render_template('index.html', stat=0)
    elif state == 1: 
        print("power on")
        return render_template('index.html', stat=1)
    


if __name__ == '__main__':
    app.run(host='10.1.1.49', threaded=True)
