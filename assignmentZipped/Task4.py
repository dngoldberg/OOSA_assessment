import rasterio
import numpy as np
import os
from rasterio.plot import show
from rasterio.fill import fillnodata 
from Task2 import TiffLVIS
from Task2 import args
import argparse


##########################################

##########################################

import rasterio
import numpy as np
from rasterio.fill import fillnodata
from Task2 import args

def GapFill(filename, search_dist):

    with rasterio.open(filename) as fp:
        raster = fp.read(1)  

        mask_boolean = (raster != -999)

        filled_raster = fillnodata(raster, mask=mask_boolean, max_search_distance=search_dist)

        filecode = args.filename[-18:-14]

        output_fp = f"/home/s2015364/AssignmentRepo/LVIS_combo_filled_{filecode}.tif"

        profile = fp.profile
        profile.update(dtype=rasterio.float32)
        
        with rasterio.open(output_fp, "w", **profile) as dst:
            dst.write(filled_raster.astype(np.float32), 1)

if __name__ == "__main__":

    GapFill(args.filename, args.searchdist)

