'''
Task 1
'''

# Importing necessary elements

#from LvisDataReader import lvisData
#import h5py
#from pyproj import Proj, transform
from matplotlib import pyplot as plt
#from tiffExample import writeTiff
from processLVIS import lvisGround

##########################################

class PlotLVIS(lvisGround):
    '''A class, inheriting from lvisGround to process and plot LVIS waveform data.'''
  
    def plotWaves(self, i):
        '''Method to plot the waveform for a specified index, i.'''
        #for j in range(len(self.waves[i])):
            #if self.waves[i][j] == 0:
                #break
         
        plt.plot(self.waves[i], self.z[i])
        plt.title(f"Waveform Plot for shot {i}")
        plt.xlabel("Return Strength")
        plt.ylabel("Time (Height) ")
        plt.show()
    """Method which returns the waveform plot for a specified bin, chosen by argument i."""

##########################################


if __name__ == "__main__":
    '''Main block to ensure code doesn't run when imported.'''

    filename = '/geos/netdata/oosa/assignment/lvis/2009/ILVIS1B_AQ2009_1020_R1408_068453.h5'
    '''Location of file covering the study site.'''

    b = PlotLVIS(filename, onlyBounds=True)
    '''Load in the bounds using PlotLVIS.'''

    x0 = b.bounds[0]
    y0 = b.bounds[1]
    x1 = (b.bounds[2] - b.bounds[0]) + b.bounds[0]
    y1 = (b.bounds[3] - b.bounds[1]) + b.bounds[1]
    """Specify the bounds of loaded in data."""

    lvis = PlotLVIS(filename, minX=x0, minY=y0, maxX=x1, maxY=y1)
    """Read in the data within the specified bounds."""

    lvis.setElevations()
    """Use the setElevation function to find terrain elevation."""

    index = int(input("Enter the waveform index to plot: "))
    lvis.plotWaves(index)
    """Prompt the user for a waveform index and plot the selected waveform."""

