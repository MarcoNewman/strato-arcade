"""
BIRST Team 1
Strato-Arcade
Pixy Test Script
POC: Marco Newman
"""
from datetime import datetime
import pixy2.build.python_demos.pixy as pixy
from ctypes import *
from pixy2.build.python_demos.pixy import *

print("Pixy2 Python Test -- Get/Save Blocks")

# Initialize Data Stores
# |time|block_id|block_x|block_y|block_width|block_height| - Pixy_Logs
with open(f"/home/pi/BIRST/logs/Pixy_Blocks.csv", "w") as log:
  log.write("time, pixy_id, signature, block_x, block_y, block_width, block_height\n")

pixy.init (1)
pixy.change_prog ("color_connected_components", 1)
pixy.init (2)
pixy.change_prog ("color_connected_components", 2)

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
frame = 0

while 1:
  for pixy_id in [1,2]:
    if pixy_id == 1:
      count = pixy.ccc_get_blocks (100, pixy1_blocks, pixy_id)
    else:
      count = pixy.ccc_get_blocks (100, pixy2_blocks, pixy_id)

    if count > 0:
      time_now = datetime.now()
      print(f'frame {frame}: {time_now}')
      frame = frame + 1
      for index in range (0, count):
        if pixy_id == 1:
          sig = pixy1_blocks[index].m_signature
          block_x = pixy1_blocks[index].m_x
          block_y = pixy1_blocks[index].m_y
          block_width = pixy1_blocks[index].m_width
          block_height = pixy1_blocks[index].m_height
        else:
          sig = pixy2_blocks[index].m_signature
          block_x = pixy2_blocks[index].m_x
          block_y = pixy2_blocks[index].m_y
          block_width = pixy2_blocks[index].m_width
          block_height = pixy2_blocks[index].m_height

        print(f'[BLOCK: SIG={sig:d} X={block_x:3d} Y={block_y:3d} WIDTH={block_width:3d} HEIGHT={block_height:3d}]')
        with open(f"/home/pi/BIRST/logs/Pixy{pixy_id}_Blocks.csv", "a") as log:
          log.write(f"{time_now}, {sig:d}, {block_x:3d}, {block_y:3d}, {block_width:3d}, {block_height:3d}\n")
