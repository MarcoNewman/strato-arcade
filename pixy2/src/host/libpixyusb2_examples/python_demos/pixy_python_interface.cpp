#include <string.h>
#include "libpixyusb2.h"

Pixy2  pixy_instance_1;
Pixy2  pixy_instance_2;

int init(int instance)
{
  if (instance == 1){
    return  pixy_instance_1.init();
  }
  else {
    return  pixy_instance_2.init();
  }
  
}

int change_prog (const char *  program_name, int instance)
{
  if (instance == 1){
    return pixy_instance_1.changeProg (program_name);
  }
  else{
    return pixy_instance_2.changeProg (program_name);
  }
}

int get_frame_width ()
{
  return pixy_instance_1.frameWidth;
}

int get_frame_height ()
{
  return pixy_instance_1.frameHeight;
}

void video_get_RGB (int  X, int  Y, uint8_t *  Red, uint8_t *  Green, uint8_t *  Blue)
{
  pixy_instance_1.video.getRGB (X, Y, Red, Green, Blue);
}

int ccc_get_blocks (int  max_blocks, struct Block *  blocks, int instance)
{
  int  number_of_blocks_copied;
  int  blocks_available;
  int  index;
  
  // Get number of blocks detected //
  if (instance == 1){
    pixy_instance_1.ccc.getBlocks();
    blocks_available = pixy_instance_1.ccc.numBlocks;
  }
  else{
    pixy_instance_2.ccc.getBlocks();
    blocks_available = pixy_instance_2.ccc.numBlocks;
  }
  // Copy the maximum amount of blocks that can be copied //
  number_of_blocks_copied = (max_blocks >= blocks_available ? blocks_available : max_blocks);   

  // Copy blocks //
  if (instance == 1){
    for (index = 0; index != number_of_blocks_copied; ++index)  {
      memcpy (&blocks[index], &pixy_instance_1.ccc.blocks[index], sizeof (Block));
    }
  }
  else{
    for (index = 0; index != number_of_blocks_copied; ++index)  {
      memcpy (&blocks[index], &pixy_instance_2.ccc.blocks[index], sizeof (Block));
    }
  }

  return number_of_blocks_copied;
}

void line_get_all_features ()
{
  pixy_instance_1.line.getAllFeatures();
}

void line_get_main_features ()
{
  pixy_instance_1.line.getMainFeatures();
}

int line_get_vectors (int  max_vectors, struct Vector *  vectors)
{
  int  number_of_vectors_copied;
  int  vectors_available;
  int  index;

  vectors_available        = pixy_instance_1.line.numVectors;
  number_of_vectors_copied = (max_vectors >= vectors_available ? vectors_available : max_vectors);

  // Copy vectors //
  for (index = 0; index != number_of_vectors_copied; ++index)  {
    memcpy (&vectors[index], &pixy_instance_1.line.vectors[index], sizeof (Vector));
  }

  return number_of_vectors_copied;
}

int line_get_intersections (int  max_intersections, struct Intersection *  intersections)
{
  int  number_of_intersections_copied;
  int  intersections_available;
  int  index;

  intersections_available        = pixy_instance_1.line.numIntersections;
  number_of_intersections_copied = (max_intersections >= intersections_available ? intersections_available : max_intersections);

  // Copy intersections //
  for (index = 0; index != number_of_intersections_copied; ++index)  {
    memcpy (&intersections[index], &pixy_instance_1.line.intersections[index], sizeof (Intersection));
  }

  return number_of_intersections_copied;
}

int line_get_barcodes (int  max_barcodes, struct Barcode *  barcodes)
{
  int  number_of_barcodes_copied;
  int  barcodes_available;
  int  index;

  barcodes_available        = pixy_instance_1.line.numBarcodes;
  number_of_barcodes_copied = (max_barcodes >= barcodes_available ? barcodes_available : max_barcodes);

  // Copy barcodes //
  for (index = 0; index != number_of_barcodes_copied; ++index) {
    memcpy (&barcodes[index], &pixy_instance_1.line.barcodes[index], sizeof (Barcode));
  }

  return number_of_barcodes_copied;
}

void set_lamp (int upper, int lower, int instance)
{
  if (instance == 1){
    pixy_instance_1.setLamp (upper, lower);
  }
  else{
    pixy_instance_2.setLamp (upper, lower);
  }
}

void set_servos (int  S1_Position, int  S2_Position)
{
  pixy_instance_1.setServos (S1_Position, S2_Position);
}
