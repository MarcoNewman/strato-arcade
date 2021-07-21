"""
BIRST Team 1
Strato-Arcade
Camera Test Script
POC: Marco Newman
"""
import time
from datetime import datetime
from picamera import PiCamera

# Initialize Pi Camera V2
cam = PiCamera()
t='{:%Y%m%d-%H%M%S}'.format(datetime.now())
cam.resolution = (1920,1080)

# Start Recording - Pi Camera V2
print('Starting Recording')
cam.start_recording(f"/home/pi/vid_{t}.yuv")
print('Recording...')
# Record for 10 Seconds
time.sleep(10)

# Stop Camera Recording
cam.stop_recording()
cam.close()
print('Video Thread Stopped')