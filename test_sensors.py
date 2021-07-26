"""
BIRST Team 1
Strato-Arcade
Flight Script
POC: Marco Newman
"""

import board
import adafruit_lis3dh
import adafruit_dps310
import adafruit_shtc3
import digitalio
import sys
import os
import datetime

# Get time of flight
t='{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now())

# Initialize log data store
# |time|acc_x|acc_y|acc_z|humidity|temperature_external|pressure|temperature_internal| - Sensor Logs
with open(f"/home/pi/BIRST/logs/{t}_sensors.csv", "w") as log:
  log.write("time, acc_x, acc_y, acc_z, humidity, temperature_external, pressure, temperature_internal\n")

# Initialize I2C
i2c = board.I2C()

# Initialize Accelerometer
int1 = digitalio.DigitalInOut(board.D6)  # Set this to the correct pin for the interrupt!
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

# Initialize Temperature + Pressure Sensor
dps310 = adafruit_dps310.DPS310(i2c)

# Initialize Temperature + Humidity Sensor
sht = adafruit_shtc3.SHTC3(i2c)

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

    # Query Accelerometer
    if (loop_counter % 3 == 0): # 1/10 seconds
      acc_x, acc_y, acc_z = lis3dh.acceleration
      print(f"Accelerometer Data: x-{acc_x}, y-{acc_y}, z-{acc_z}")
      
      # Write accelerometer data
      with open("/home/pi/BIRST/logs/{t}_sensors.csv", "a") as log:
        log.write(f"{time_now}, {acc_x}, {acc_y}, {acc_z}")
        if (loop_counter % 150 == 0): # 5 seconds
          log.write(',')
        else:
          log.write('\n')
    

    # Query Enviornmental Sensors
    if (loop_counter % 150 == 0): # 5 seconds
      # Query Temperature + Pressure Sensor
      pressure = dps310.pressure
      temperature_internal = dps310.temperature
      print(f"Pressure Sensor Data: pressure-{pressure}, temperature-{temperature_internal}")

      # Query Temperature + Humidity Sensor
      humidity = sht.relative_humidity
      temperature_external = sht.temperature
      print(f"Humidity Sensor Data: humidity-{humidity}, temperature-{temperature_external}")

      # Write sensor data
      with open("/home/pi/BIRST/logs/{t}_sensors.csv", "a") as log:
        log.write(f"{humidity}, {temperature_external}, {pressure}, {temperature_internal}\n")

      # Reset Loop Counter
      loop_counter = 0

    # Increment loop counter and time log
    loop_counter += 1
    time_previous = time_now

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print(' Interrupted')

    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
