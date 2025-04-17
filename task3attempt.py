'''TASK3 - looping through all files and using bounds to create DEM raster'''
# import libraries
import os
import argparse
import tracemalloc
from rasterio.merge import merge
from glob import glob
import numpy as np
import shutil

#import other classes and functions
from source.lvisTiff import HandleTiff
from source.tiffExample import writeTiff

###################################

def chooseArg():
# ideally would combine this with task 1 function 
    '''Method to pick arguements from command line
    
    Command Line Args:
        --i = optional = index of wavefrom
        --o = optional = output tiff file
        --res = optional = resolution for raster
    
    Returns:
        args.x = object containing chosen arguement'''

    # create argparse object
    parser = argparse.ArgumentParser(description='Choose processing options')
    # filename compulsory  
    #parser.add_argument('-f', type=str, required=True, help='Path to the LVIS HDF5 file')
    # merged DEM tiff name
    parser.add_argument('--o', type=str, default='2009_DEMbounded.tif', help='Name ' \
                            'of output TIFF file')
    # resolution for raster
    parser.add_argument('--res', type=int, default=30, help='Resolution for DEM')
    # parse the arguements
    args = parser.parse_args()
    return args

#############################

class plotLVIS(HandleTiff):

# ideally should call this directly from task 2
    def makeDEM(self, resolution, tiffName):
        '''convert data to a geotiff 
        
        Args: 
            resolution = chosen spatial resolution
            tiffname = name of output file

        Returns:
            writes geotiff to file'''
        writeTiff(self.zG, self.x, self.y, resolution, tiffName, epsg= 3031)
        return  

##########################################

if __name__=="__main__":
  '''Main block'''

# start tracking RAM
tracemalloc.start()

command = chooseArg()

# for looping through all files
filelist_2009 = glob('/geos/netdata/oosa/assignment/lvis/2009/*.h5')  #only.h5 files
#filelist_2015 = glob('/geos/netdata/oosa/assignment/lvis/2015/*.h5')  #only.h5 files
print(filelist_2009)   # check

for filename in filelist_2009:
    # get name of file
    basename = os.path.basename(filename)
    file_id = basename.split('.')[0][-6:]   # 6 digits before extension
    # find bounds of the file before loop
    b=plotLVIS(filename,onlyBounds=True)

    #loop for tile subdivisions
    subset_size = 8
    columns = (b.bounds[2]-b.bounds[0])/subset_size  #columns/subset
    rows = (b.bounds[3]-b.bounds[1])/subset_size  #rows/subset
    tile_number = 1   # first tile is 1

for i in range(subset_size):    # loop for x axis
    for j in range(subset_size):    # loop for y axis
        x0=b.bounds[0] + i * columns   # first x
        y0=b.bounds[1] + j * rows   # first y
        x1 = x0 + columns    # end x
        y1 = y0 + rows    # end y
        print(f'Reading file:{os.path.basename(filename)} | Tile {tile_number}')

        try:
            # read in all data within our spatial subset
            lvis=plotLVIS(filename,minX=x0,minY=y0,maxX=x1,maxY=y1, setElev=True)   #read in elev

            lvis.x,lvis.y = lvis.reprojectLVIS(3031)
            # find middle of reprojected coords
            minx = np.min(lvis.x)
            miny = np.min(lvis.y)
            maxx = np.max(lvis.x)
            maxy = np.max(lvis.y)

            tile_midx = (minx+maxx)/2
            tile_midy = (miny+maxy)/2
                         
            if tile_midx < -1571000:
                if tile_midy > -260000:
                    if tile_midx > -1600000:
                        if tile_midy < -210000:
                            print(f'Reading file {os.path.basename(filename)}|Tile {tile_number}')
                            # folder managment
                            data_folder = 'Data2009'    # specify input dir
                            os.makedirs(data_folder, exist_ok=True) # check folder exists and create if not
                            
                            # process if within bounds
                            lvis.estimateGround()
                            tiffName = f"Data2009/DEM{os.path.basename(filename)}|{tile_number}.tif"   #filename with tile identifier
                            lvis.makeDEM(command.res, tiffName)
                else:
                    print(f'Tile {tile_number} in {os.path.basename(filename)} is not within bounds')


        except AttributeError as error:
            print(f'Tile {tile_number} has been skipped')

        tile_number +=1   # loop counter

# Outside loop
print(f'Each array is split into {subset_size} x {subset_size} tiles')

# merge the rasters
# folder management
tiles_dir2009 = 'Data2009'   # specify input dir
output_folder = 'Outputs'    # specify output dir
os.makedirs(output_folder, exist_ok=True) # check folder exists and create if not
output_tiff = os.path.join(output_folder, command.o)

# call functions
lvis.merge_tiles(tiles_dir2009, output_tiff)
plot_name = command.o
lvis.visualise_tiff(output_tiff, plot_name)

# after merging tiles remove data folder
try:
    shutil.rmtree('Data2009')
    print('Temporary files deleted sucessfully')
except Exception as e:
    print(f'An arror occured: {e}')

# Memory tracking
current, peak = tracemalloc.get_traced_memory() # both needed as returns a tuple
peak_GB = peak/(1024**3)
print(f'Peak memory used was: {peak_GB:.2f} GB')