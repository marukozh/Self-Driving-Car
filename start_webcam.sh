sudo ffserver -f /etc/ffserver.conf & ffmpeg -v quiet -r 5 -s 320x240 -f video4linux2 -i /dev/video0 http://localhost:8090/webcam.ffm
# http://raspberrypi.local:8090/webcam.mjpeg
