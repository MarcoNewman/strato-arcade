"""
BIRST Team 1
Strato-Arcade
Multi-Pixy Test Script
POC: Marco Newman
"""
from datetime import datetime
import pixy2.build.python_demos.pixy as pixy
from ctypes import *
from pixy2.build.python_demos.pixy import *

print("Multiple Pixy2 Python Test -- Get/Save Blocks")
t='{:%Y%m%d-%H%M%S}'.format(datetime.now())

# Initialize log data store
# |time|pixy_id|signature_id|block_x|block_y|block_width|block_height| - Pixy_Logs
with open(f"/home/pi/BIRST/logs/Pixy2s_{t}.csv", "w") as log:
  log.write("time, pixy_id, signature_id, block_x, block_y, block_width, block_height\n")

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

# Time Check for 1/60s WAITING
time_previous = datetime.now()
while 1:
  time_now = datetime.now()
  while (time_now - time_previous < datetime.timedelta(seconds=1/30)):
    time_now = datetime.now()
  
  # Check both pixys for track blocks
  for pixy_id in [1,2]:
    if pixy_id == 1:
      count = pixy.ccc_get_blocks (100, pixy1_blocks, pixy_id)
    else:
      count = pixy.ccc_get_blocks (100, pixy2_blocks, pixy_id)

    if count > 0:
      # Blocks detected -> update frame count and timestamp
      time = datetime.now()
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
        with open(f"/home/pi/BIRST/logs/Pixy2s_{t}.csv", "a") as log:
          log.write(f"{time}, {pixy_id:d}, {signature_id:d}, {block_x:3d}, {block_y:3d}, {block_width:3d}, {block_height:3d}\n")

  time_previous = time_now
