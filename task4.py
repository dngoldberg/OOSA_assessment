'''Task 4 just infill with hard coded file'''

'''pseudo-code for gap-filling but would be in lvisTiff

define function named fill_gaps where arg is the raster file path
    read first band of the raster with rasterio 
    use modeule rasterio.fill - https://rasterio.readthedocs.io/en/latest/api/rasterio.fill.html 
    identify gaps - NaN values
    fill gaps with interpolation (nearest neighbour)
    write the modified raster to file

    then call this function in the main block to process the raster
    save with an updated file name (e.g. filled_DEM)

    with attempt below that runs but doens't change anything
    -need to double check how the data gaps are recorded - as 0's?
'''

import numpy as np
import rasterio
from rasterio.fill import fillnodata

def fill_gaps(raster_path, filled_raster_path):
    
    with rasterio.open(raster_path) as src:
        data = src.read(1)  # Read the first band
        profile = src.profile

        # find NaN
        nan_mask = np.isnan(data)

        # fill gaps using fillnodata
        filled_data = fillnodata(data, mask=nan_mask)

    # save filled raster
    with rasterio.open(filled_raster_path, 'w', **profile) as dst:
        dst.write(filled_data, 1)

# using a smaller raster
fill_gaps('Outputs/Example.tif', 'Outputs/filled_tile.tif')
print('Saved as Outputs/filled_tile.tif')
