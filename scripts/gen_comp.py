import re
import os
from ome_model import experimental as ome

"""
Generate companion.ome files because the tif files aren't 
recognized as z-stack but incorrectly as timelapse.
Their size (sizeT) has to be determined with showinf beforehand,
see IMAGE_FILES_SRC .
Create with:
find * -name "*.tif" -exec sh -c 'echo "$1"; showinf -nopix "$1" |
    grep SizeT' _ {} \; >> /tmp/sizeT.txt 
"""

SIZE_T = 1
ORDER = "XYCTZ"
TYPE = "uint16"
OUTPUT_DIR = "../experimentA/companions"
BASE_DIR = "/uod/idr/filesets/idr0110-rodermund-xistrna/20210404-ftp"

IMAGE_FILES_SRC = "image_info.txt"
"""
20180526_Xist_turnover_pulsechase1_transgenic_diAcFAM_JF585_0_02_FUS_SIR_THR_MCF_ALN-full.tif
	Width = 512
	Height = 512
	SizeZ = 1
	SizeT = 88
	SizeC = 1
...
Generate with find * -name "*.tif" -exec sh -c 'echo "$1"; showinf -nopix "$1" | grep "Size\|Width \|Height"' _ {} \; >> /tmp/image_info.txt
"""


def create_companion(filename, x, y, z, c, t, order, type):
  companion = ome.Image(filename, x, y, z, c,
      sizeT=t, order=order, type=type)
  companion.add_tiff(filename)
  companion_file = f"{OUTPUT_DIR}/{filename}.companion.ome"

  with open(companion_file, 'wb') as o:
      ome.create_companion(images=[companion], out=o)
  return companion_file


image_files = open(IMAGE_FILES_SRC, 'r').readlines()
for i in range(0, len(image_files)-1, 6):
  image_file = image_files[i].strip() # 20180526_Xist_turnover_pulsechase1_transgenic_diAcFAM_JF585_0_02_FUS_SIR_THR_MCF_ALN-full.tif
  w = image_files[i+1].strip().split("=")[1].strip() # Width = 512
  h = image_files[i+2].strip().split("=")[1].strip() # Height = 512
  z = image_files[i+4].strip().split("=")[1].strip() # SizeT = 1
  c = image_files[i+5].strip().split("=")[1].strip() # SizeC = 1
  try:
    comp = create_companion(image_file, w, h, z, c, SIZE_T, ORDER, TYPE)
    print(comp)
    ln_src = f"{BASE_DIR}/{image_file}"
    ln_tgt = f"{OUTPUT_DIR}/{image_file}"
    if not os.path.islink(ln_tgt):
        os.symlink(ln_src, ln_tgt)
  except Exception as e:
    print(f"Failed to create companion for {image_file}")
    print(e)
