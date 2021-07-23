"""
BIRST Team 1
Strato-Arcade
Flight Script
POC: Marco Newman
"""

#import board
#import adafruit_shtc3
#import digitalio
import sys
import os
import datetime
import pixy2.build.python_demos.pixy as pixy
from ctypes import *
from pixy2.build.python_demos.pixy import *
from picamera import PiCamera

# Get time of flight
t='{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now())

# Initialize Pi Camera V2
cam = PiCamera()
cam.resolution = (1920,1080)
cam.framerate = 30

# Start Recording - Pi Camera V2
os.mkdir(f"/home/pi/BIRST/videos/{t}")
print('Starting Recording')
cam.start_recording(f"/home/pi/BIRST/videos/{t}/{t}.h264")
print('Recording...')

# Initialize log data store
# |time|pixy_id|signature_id|block_x|block_y|block_width|block_height| - Pixy2 Logs
# |time|acc_x|acc_y|acc_z|humidity|temperature_external|pressure|temperature_internal| - Sensor Logs
with open(f"/home/pi/BIRST/logs/{t}_pixys.csv", "w") as log:
  log.write("time, pixy_id, signature_id, block_x, block_y, block_width, block_height\n")
with open(f"/home/pi/{t}_sensors.csv", "w") as log:
  log.write("time, acc_x, acc_y, acc_z, humidity, temperature_external, pressure, temperature_internal\n")

# Initialize I2C
#i2c = board.I2C()

# Initialize Temperature + Humidity Sensor
#sht = adafruit_shtc3.SHTC3(i2c)

# Initialize Accelerometer
#int1 = digitalio.DigitalInOut(board.D6)  # Set this to the correct pin for the interrupt!
#lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

# Initialize Temperature + Pressure Sensor
#dps310 = adafruit_dps310.DPS310(i2c)

# Initialize Pixy2s
a = pixy.init (1)
print(f"Pixy1 Initialized: {a}")
pixy.change_prog ("color_connected_components", 1)
b = pixy.init (2)
print(f"Pixy2 Initialized: {b}")
pixy.change_prog ("color_connected_components", 2)

# Define block data structure for tracks
class Blocks (Structure):
  _fields_ = [ ("m_signature", c_uint),
    ("m_x", c_uint),
    ("m_y", c_uint),
    ("m_width", c_uint),
    ("m_height", c_uint),
    ("m_angle", c_uint),
    ("m_index", c_uint),
    ("m_age", c_uint) ]
pixy1_blocks = BlockArray(100)
pixy2_blocks = BlockArray(100)
pixy1_frame = 0
pixy2_frame = 0

# Turn Pixy LEDs ON
pixy.set_lamp(1, 1, 1)
pixy.set_lamp(1, 1, 2)

def main():
  global t
  
  time_previous = datetime.datetime.now()
  loop_counter = 0
  while 1:
    # Get current loop time
    time_now = datetime.datetime.now()

    # 1/30s loop interval
    while (time_now - time_previous < datetime.timedelta(seconds=1/20)):
      time_now = datetime.datetime.now()

    # Query Pixy2 blocks
    pixy_data = query_pixys()

    # Query Accelerometer
    if (loop_counter % 3 == 0): # 1/10 seconds
      print("<ACCELEROMETER DATA>")
      #acc_x, acc_y, acc_z = lis3dh.acceleration
      
      # Write accelerometer data
      # with open("/home/pi/logs/{t}_sensor.csv", "a") as log:
      #   log.write(f"{time_now}, {acc_x}, {acc_y}, {acc_z}")
      #   if (loop_counter % 150 == 0): # 5 seconds
      #     log.write(',')
      #   else:
      #     log.write('\n')
    

    # Query Enviornmental Sensors
    if (loop_counter % 150 == 0): # 5 seconds
      # Query Humidity + Temperature Sensor
      print("<HUMIDITY/TEMPERATURE DATA")
      #humidity = sht.relative_humidity
      #temperature_external = sht.temperature
      
      # Query Pressure + Temperature Sensor
      print("<PRESSURE/TEMPERATURE DATA")
      #pressure = dps310.pressure
      #temperature_internal = dps310.temperature

      # Write sensor data
      # with open("/home/pi/logs/{t}_sensor.csv", "a") as log:
      #   log.write(f"{humidity}, {temperature_external}, {pressure}, {temperature_internal}\n")
    
    # Restart Recording - Pi Camera V2
    if (loop_counter == 300): # 10 seconds
      cam.stop_recording()
      cam.start_recording(f"/home/pi/BIRST/videos/{t}/{time_now}.h264")

      # Reset Loop Counter
      loop_counter = 0

  # Increment loop counter and time log
  loop_counter += 1
  time_previous = time_now


def query_pixys():
  global pixy1_blocks
  global pixy2_blocks
  global pixy1_frame
  global pixy2_frame

  # Check both pixys for track blocks
  pixy_data = ""
  for pixy_id in [1,2]:
    if pixy_id == 1:
      count = pixy.ccc_get_blocks (100, pixy1_blocks, pixy_id)
    else:
      count = pixy.ccc_get_blocks (100, pixy2_blocks, pixy_id)

    if count > 0:
      # Blocks detected -> update frame count and timestamp
      time = datetime.datetime.now()
      if pixy_id == 1:
        print(f'PixyID: {pixy_id} | Frame: {pixy1_frame} | {time}')
        pixy1_frame = pixy1_frame + 1
      else:
        print(f'PixyID: {pixy_id} | Frame: {pixy2_frame} | {time}')
        pixy2_frame = pixy2_frame + 1

      # Read block position data and size
      for index in range (0, count):
        if pixy_id == 1:
          signature_id = pixy1_blocks[index].m_signature
          block_x = pixy1_blocks[index].m_x
          block_y = pixy1_blocks[index].m_y
          block_width = pixy1_blocks[index].m_width
          block_height = pixy1_blocks[index].m_height
        else:
          signature_id = pixy2_blocks[index].m_signature
          block_x = pixy2_blocks[index].m_x
          block_y = pixy2_blocks[index].m_y
          block_width = pixy2_blocks[index].m_width
          block_height = pixy2_blocks[index].m_height

        # Report block data
        print(f'[BLOCK: SIG={signature_id:d} X={block_x:3d} Y={block_y:3d} WIDTH={block_width:3d} HEIGHT={block_height:3d}]')
        pixy_data += f"{time}, {pixy_id:d}, {signature_id:d}, {block_x:3d}, {block_y:3d}, {block_width:3d}, {block_height:3d}\n"
  
  # Return all formated block data
  return pixy_data

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print(' Interrupted')
    
    # Turn Pixy LEDs OFF
    pixy.set_lamp(0, 0, 1)
    pixy.set_lamp(0, 0, 2)

    # Stop Camera Recording
    cam.stop_recording()
    cam.close()
    print('Video Thread Stopped')

    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
