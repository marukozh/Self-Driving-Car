import argparse
import cv2
import urllib2
import numpy as np
from datetime import datetime
import time
import traceback
import os
import sys


# Example: python save_streaming_video_data.py --host raspberrypi.local
ap = argparse.ArgumentParser()
ap.add_argument("--host", required=True, help="Raspberry Pi hostname or IP")
args = vars(ap.parse_args())
host = args["host"]

# First log into the raspberry pi, and then do these two things:
# cd /usr/src/ffmpeg
# sudo modprobe bcm2835-v4l2
# sudo ffserver -f /etc/ffserver.conf & ffmpeg -v quiet -r 5 -s 320x240 -f video4linux2 -i /dev/video0 http://localhost:8090/webcam.ffm

fourcc = cv2.cv.CV_FOURCC(*'jpeg')
out = cv2.VideoWriter('output.mov',fourcc, 20.0, (320,240))
file_path = str(os.path.dirname(os.path.realpath(__file__)))+"/video_timestamps.txt"
stream = urllib2.urlopen('http://{host}/webcam.mjpeg'.format(host=host))

try:
    bytes = bytes()
    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            #cv2.imshow('Car Camera', frame)
            now = datetime.now()
            print(now)
            if frame is not None:
              # cv2.imshow("car camera", frame)

              # Use the code below if I need find the dimensions of the video
              '''
              height, width, channels = frame.shape
              print(height)
              print(width)
              '''
              out.write(frame)
              timestamp = datetime.now()
              with open(file_path,"a") as writer:
                writer.write(str(timestamp)+"\n")
except KeyboardInterrupt:
    print('Interrupted')
    try:
        print('Trying to release VideoWriter.')
        time.sleep(5)
        out.release()
        sys.exit(0)
    except Exception:
        print('Failed to release VideoWriter.')
        print(traceback.format_exc())
        sys.exit(1)
