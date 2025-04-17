import rasterio
import numpy as np
from Task2 import args
import os

def RasterMaths(filename, filename2):
    '''Defining RasterMaths function which finds elevation change by subtracting 2009 from 2015'''
    with rasterio.open(filename) as f1:
        '''2009 set as file 1'''
        raster2009 = f1.read(1)
        nodata1 = f1.nodata

    with rasterio.open(filename2) as f2:
        '''2015 set as file 1'''
        raster2015 = f2.read(1)
        nodata2 = f2.nodata

    
    xmin = max(f1.bounds[0], f2.bounds[0])
    ymin = max(f1.bounds[1], f2.bounds[1])
    xmax = min(f1.bounds[2], f2.bounds[2])
    ymax =  min(f1.bounds[3], f2.bounds[3])
    '''Specifying the bounding area as the maximum extent of both the 2009 and 2015'''
    

    # Get pixel coordinates for the overlap region
    row_start, col_start = f1.index(xmin, ymax)
    row_stop, col_stop = f1.index(xmax, ymin)

    # Crop rasters to the overlapping region
    raster2009 = raster2009[row_start:row_stop, col_start:col_stop]
    raster2015 = raster2015[row_start:row_stop, col_start:col_stop]

    # Create valid masks and combine them
    mask_boolean = (raster2009 != 999) & (raster2015 != 999)

    # Perform the calculation on valid pixels
    result = np.full_like(raster2009, np.nan, dtype=np.float32)
    result[mask_boolean] = raster2015[mask_boolean] - raster2009[mask_boolean]

    out_fp = os.path.join(os.getcwd(), "LVIS_Elevation_Change.tif")

    # Save the result to a new file
    with rasterio.open(out_fp, 'w', **f1.meta) as dest:
        dest.write(result, 1)


if __name__ == "__main__":
    '''Main block to ensure code doesn't run when imported.'''

    RasterMaths(args.filename, args.filename2)

