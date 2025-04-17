
'''An example of how to use the LVIS python scripts'''
# import libraries
import os
import argparse
import tracemalloc
from matplotlib import pyplot as plt
#import other classes and functions
from source.processLVIS import lvisGround

##########################################

def chooseArg():
    '''Method to pick arguements from command line
    
    Command Line Args:
        --i = optional = index of wavefrom
        -f = required = path to LVIS HDF5 file
        --o = optional = output tiff file
        --res = optional = resolution for raster
    
    Returns:
        args.x = object containing chosen arguement'''

    # create argparse object
    parser = argparse.ArgumentParser(description='Choose processing options')
    # waveform index optional
    parser.add_argument('--i', type=int, default=192, help = 'Index of waveform')
    # filename compulsory  
    parser.add_argument('-f', type=str, required=True, help='Path to the LVIS HDF5 file')
    # merged DEM tiff name
    parser.add_argument('--o', type=str, default='1file2009_DEM.tif', help='Name ' \
                            'of output TIFF file')
    # resolution for raster
    parser.add_argument('--res', type=int, default=30, help='Resolution for DEM')
    # parse the arguements
    args = parser.parse_args()
    return args

class plotLVIS(lvisGround):
    '''A class, ineriting from lvisground (from processLVIS) and a plotting method'''

    def plotSingleWave(self, index):
        '''Plot single waveform if it exiss and exports as a png

        Args:
            index = chosen index to display

        Returns:
            saves graph to file

        Raises:
            IndexError = if index has no data'''
        
        try:    # try-except so that it doesnt crash if index with no data is selected
          elevation, waveform = self.getOneWave(index) # waveform at chosen index
          plt.xlabel("Waveform Return (Amplitude)")
          plt.ylabel("Elevation (m)")
          plt.title(f'Waveform of Index:{index}')
          plt.plot(waveform, elevation, c='purple')
          folder = 'Outputs'
          os.makedirs(folder, exist_ok=True)
          plt.savefig('Outputs/FullWaveform.png', dpi=200, bbox_inches='tight')
          print(f'Waveform has been saved to Outputs')
          plt.show()
        except IndexError as e: # raise error if no data
          print(e)

## ########################################

if __name__=="__main__":
  '''Main block'''

# start tracking RAM
tracemalloc.start()

command = chooseArg()

filename = command.f

# find bounds
b = plotLVIS(filename,onlyBounds=True)    # first index in list

# Spatial subset for MWE
x0=b.bounds[0]
y0=b.bounds[1]
x1=(b.bounds[2]-b.bounds[0])/10+b.bounds[0] # columns/subset
y1=(b.bounds[3]-b.bounds[1])/10+b.bounds[1] # rows/subset
# check bounds
print(f'This tile has subset bounds {x0:.3f}, {y0:3f} to {x1:.3f}, {y1:.3f}')

# read in all data within our spatial subset
lvis=plotLVIS(filename,minX=x0,minY=y0,maxX=x1,maxY=y1)

# creates 2D array of z 
lvis.setElevations()

# call function to plot single waveform
lvis.plotSingleWave(index=command.i)

# Memory tracking
current, peak = tracemalloc.get_traced_memory() # both needed as returns a tuple
peak_GB = peak/(1024**3)  # convert to GB
print(f'Peak memory used was: {peak_GB:.2f} GB')