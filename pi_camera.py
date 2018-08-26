from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 180

camera.start_recording('/home/pi/video.h264')
sleep(10)
camera.stop_recording()
# camera.capture('/home/pi/image.jpg')
