import re
import os
from ome_model import experimental as ome

"""
Generate companion.ome files because the tif files aren't 
recognized as z-stack but incorrectly as timelapse.
Their size (sizeT) has to be determined by showinf beforehand,
see IMAGE_FILES_SRC .
"""

SIZE_X = 512
SIZE_Y = 512
SIZE_T = 1
SIZE_C = 1
ORDER = "XYCTZ"
TYPE = "uint16"

IMAGE_FILES_SRC = "sizeT.txt"
"""
20190813_Pulse_Chase_3_CIZ1KO_Xist_turnover_on_chromatin_Maintenance_160min_10_FUS_SIR_THR_MCF_ALN-full.tif
    SizeT = 106
"""

def create_companion(filename, x, y, z, c, t, order, type)
  companion = ome.Image(filename, x, y, z, c,
      sizeT=t, order=order, type=type)
  companion.add_channel(name="0", samplesPerPixel=1)
  companion.add_tiff(filename)
  companion_file = f"{filename}.companion.ome"

  with open(companion_file, 'wb') as o:
      ome.create_companion(images=[companion], out=o)
  return companion_file

image_files = open(IMAGE_FILES_SRC, 'r').readlines()


for i in range(0, len(image_files)-1, 2):
  image_file = image_files[i]
  size_z = image_files[i+1]
  size_z = int(size_z.split("=")[1].strip())
  try:
    comp = create_companion(image_file, SIZE_X, SIZE_Y, size_z, SIZE_C, SIZE_T, ORDER, TYPE)
    print(f"{comp}")
  except Exception as e:
    print(f"Failed to create companion for {image_file}")
    print(e)