#!/usr/bin/env python3
from flask import Flask, render_template, Response
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time


app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    template = cv2.imread('moi.jpg',0)
    w, h = template.shape[::-1]

    meth = 'cv2.TM_CCOEFF_NORMED'
    method = eval(meth)

    cap = cv2.VideoCapture(0)
    if (cap.isOpened() == False):
      print("Unabl e to read camera feed")
      return
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb+').read() + b'\r\n')
        time.sleep( 5 )

    cap.release()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
