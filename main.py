"""
BIRST Team 1
Strato-Arcade
Flight Script
POC: Marco Newman
"""

import board
import adafruit_shtc3
import digitalio
import sys
import os
import datetime
import pixy2.build.python_demos.pixy as pixy
from ctypes import *
from pixy2.build.python_demos.pixy import *
from picamera import PiCamera

# Initialize Pi Camera V2
cam = PiCamera()
t='{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now())
cam.resolution = (1920,1080)

# Start Recording - Pi Camera V2
cam.start_recording(f"/home/pi/vid_{t}.yuv420")

# Initialize Data Stores
# |time|ball1_x|ball1_y|ball2_x|ball2_y|acc_x|acc_y|acc_z| - HiFi_Logs
# |time|humidity|temperature_external|pressure|temperature_internal| - LoFi_Logs
with open(f"/home/pi/HiFi_logs_{t}.csv", "w") as log:
  log.write("time, ball1_x, ball1_y, ball2_x, ball2_y, acc_x, acc_y, acc_z\n")
with open(f"/home/pi/LoFi_logs_{t}.csv", "w") as log:
  log.write("time, humidity, temperature_external, pressure, temperature_internal\n")

# Initialize I2C
i2c = board.I2C()

# Initialize Temperature + Humidity Sensor
sht = adafruit_shtc3.SHTC3(i2c)

# Initialize Accelerometer
int1 = digitalio.DigitalInOut(board.D6)  # Set this to the correct pin for the interrupt!
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

# Initialize Temperature + Pressure Sensor
dps310 = adafruit_dps310.DPS310(i2c)

# Initialize Pixy2s



# MAIN LOOP
time_previous = datetime.now()
lofi_loop_counter = 0
while(1):
  # Time Check for 1/60s WAITING
  time_now = datetime.now()
  if (loop_counter != 0):
    while (time_now - time_previous < datetime.timedelta(seconds=1/60)):
      time_now = datetime.now()

  # Query Pixy2 Blocks - x,y
  

  # Query Accelerometer
  if (loop_counter % 6 == 0): # 1/10 seconds
    acc_x, acc_y, acc_z = lis3dh.acceleration

  # Time Check for 5 seconds
  if (loop_counter == 300)
    # Query Humidity + Temperature Sensor
    humidity = sht.relative_humidity
    temperature_external = sht.temperature
    
    # Query Pressure + Temperature Sensor
    pressure = dps310.pressure
    temperature_internal = dps310.temperature
    
    # Reset LoFi Loop Counter
    lofi_loop_counter = 0

    # Write to Data CSVs
    with open("/home/pi/LoFi_logs.csv", "a") as log:
      log.write(f"{time_now}, {humidity}, {temperature_external}, {pressure}, {temperature_internal}\n")
  with open("/home/pi/HiFi_logs.csv", "a") as log:
    if (loop_counter % 6 == 0):
      log.write(f"{time_now}, {ball1_x}, {ball1_y}, {ball2_x}, {ball2_y}, {acc_x}, {acc_y}, {acc_z}\n")
    else:
      log.write(f"{time_now}, {ball1_x}, {ball1_y}, {ball2_x}, {ball2_y}\n")
  

  # Increment Loop Counter and time_previous variables
  lofi_loop_counter += 1
  time_previous = time_now

  
# Stop Camera Recording
cam.stop_recording()
cam.close()
print('Video Thread Stopped')