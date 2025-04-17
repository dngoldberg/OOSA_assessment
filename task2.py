'''TASK2 - making a DEM raster'''
# import libraries
import os
import tracemalloc
import shutil
#import other classes and functions
from source.lvisTiff import HandleTiff
from source.tiffExample import writeTiff
from task1 import chooseArg

#############################

class plotLVIS(HandleTiff):

    def makeDEM(self, resolution, tiffName):
        '''convert data to a geotiff 
        
        Args: 
            resolution = chosen spatial resolution
            tiffname = name of output file

        Returns:
            writes geotiff to file'''
        
        writeTiff(self.zG, self.x, self.y, resolution, tiffName)
        return  

##########################################

if __name__=="__main__":
  '''Main block'''

# start tracking RAM
tracemalloc.start()

command = chooseArg()

filename = command.f

# folder management
data_folder = 'Data2009'    # specify input dir
os.makedirs(data_folder, exist_ok=True) # check folder exists and create if not

# find bounds of the file
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

            # Make DEM as a geotiff
            lvis.reprojectLVIS(3031)
            lvis.estimateGround()

            # folder managment
            data_folder = 'Data2009'    # specify input dir
            os.makedirs(data_folder, exist_ok=True) # check folder exists and create if not
            tiffName = f"Data2009/lvisDEM_PIG{tile_number}.tif"   # filename with tile identifier
            lvis.makeDEM(command.res, tiffName)       # resolution
            tile_number +=1   # loop counter

        except AttributeError as error:
            print(f'Tile {tile_number} has been skipped')
            tile_number +=1   # loop counter

# Outside loop
print(f'Each array is split into {subset_size} x {subset_size} tiles')

# merge the rasters and folder management
tiles_dir2009 = 'Data2009'   # specify input dir
output_folder = 'Outputs'    # specify output dir
os.makedirs(output_folder, exist_ok=True) # check folder exists and create if not
output_tiff = os.path.join(output_folder, command.o)

# call functions
lvis.merge_tiles(tiles_dir2009, output_tiff)
plot_name = output_tiff.replace('.tif',',png')
lvis.visualise_tiff(output_tiff, plot_name)

# after merging tiles remove data folder
try:
    shutil.rmtree('Data2009')
    print('Temporary files deleted sucessfully')
except Exception as e:
    print(f'An arror occured: {e}')

# Memory tracking
current, peak = tracemalloc.get_traced_memory() #both needed as returns a tuple
peak_GB = peak/(1024**3)
print(f'Peak memory used was: {peak_GB:.2f} GB')
