'''A class to hold LVIS data with methods to read'''

###################################
import numpy as np
import h5py

###################################

class lvisData(object):
    '''LVIS data handler'''

    # would ideally define the bounds here (in EPSG:4326) so that is filtered at the beginning
    # minX = -100.585327
    # maxX = -96.734619
    # minY = -75.734596
    # maxY = -74.937994
    def __init__(self,filename,setElev=False,minX=-100000000, minY=-1000000000, maxX=100000000, maxY=100000000,onlyBounds=False):
        '''Class initialiser that reads LVIS data 
            and could be within specified spatial bounds
        
        Args:
            filename: The path to the LVIS data file.
            minX = min lon for spatial filtering
            minY = min lat for spatial filtering
            maxX = max lon for spatial filtering
            maxY = max lat for spatial filtering
            onlybounds = sets bounds not load data if called'''

        # call the file reader and load in to the self
        self.readLVIS(filename,minX,minY,maxX,maxY,onlyBounds)
        if(setElev):     # to save time, only read elev if wanted
          self.setElevations()

###########################################

    def readLVIS(self,filename,minX,minY,maxX,maxY,onlyBounds):
        '''Read LVIS data from files with specific bounds
 
        Args:
            filename: The path to the LVIS data file.
            minX = min lon for spatial filtering
            minY = min lat for spatial filtering
            maxX = max lon for spatial filtering
            maxY = max lat for spatial filtering
            onlyBounds(if true) = only calculate and store bounds without loading full data.

        Modifies:
            nBins = number of bins 
            lon =  array of longitudes (of selected data)
            lat = array of latitudes (of selected data)
            bounds = geographic bounds 
            nWaves =  number of selected waveforms
            waves = received waveforms'''

        # open file for reading
        f=h5py.File(filename,'r')
        # determine how many bins
        self.nBins=f['RXWAVE'].shape[1]


        # read coordinates for subsetting
        lon0=np.array(f['LON0'])       # longitude of waveform top
        lat0=np.array(f['LAT0'])       # lattitude of waveform top
        lonN=np.array(f['LON'+str(self.nBins-1)]) # longitude of waveform bottom
        latN=np.array(f['LAT'+str(self.nBins-1)]) # lattitude of waveform bottom
        # find a single coordinate per footprint
        tempLon=(lon0+lonN)/2.0
        tempLat=(lat0+latN)/2.0

        # write out bounds
        if(onlyBounds):   #if only bounds is true, exits function
          self.lon=tempLon
          self.lat=tempLat
          self.bounds=self.dumpBounds()
          return

        useInd=np.where((tempLon>=minX)&(tempLon<maxX)&(tempLat>=minY)&(tempLat<maxY))
        if(len(useInd)>0):
          useInd=useInd[0]
        '''this would only use the indices where the middle of the tile is
            within the specified geogrpahic bounds - but need to be set'''

        if(len(useInd)==0):
          print("No data contained in that region")
          self.nWaves=0
          return

        # save the geographic subset of all data
        self.nWaves=len(useInd)
        self.lon=tempLon[useInd]
        self.lat=tempLat[useInd]

        # load sliced arrays, to save RAM
        self.lfid=np.array(f['LFID'][useInd])          # LVIS flight ID number
        self.lShot=np.array(f['SHOTNUMBER'][useInd])   # the LVIS shot number, a label
        self.waves=np.array(f['RXWAVE'][useInd])  # the recieved waveforms. The data
        self.nBins=self.waves.shape[1]
        # these variables will be converted to easier variables
        self.lZN=np.array(f['Z'+str(self.nBins-1)][useInd])       # The elevation of the waveform bottom
        self.lZ0=np.array(f['Z0'][useInd])          # The elevation of the waveform top
        # close file
        f.close()
        # return to initialiser
        return

###########################################

    def setElevations(self):
        '''
        Decodes LVIS's RAM efficient elevation format and produces an array of
        elevations per waveform bin.

        Modifies:
            z array = 2D array (nWaves, nBins) filled with elevation data
        '''
        self.z=np.empty((self.nWaves,self.nBins))
        for i in range(0,self.nWaves):    # loop over waves
          self.z[i]=np.linspace(self.lZ0[i],self.lZN[i],self.nBins)   # returns an array of floats

###########################################

    def getOneWave(self,ind):
        '''
        Return a single waveform if it exists

        Args: 
            index (int) = index for retreival

        Returns:
            Tuple containing elevation (z) and waveform return (waves)

        Raises:
            IndexError: if index has no data'''
        if 0 <= ind < self.nWaves:
          return(self.z[ind],self.waves[ind])
        else:   # change this
          raise IndexError("The selected index does not have any waveform data")

###########################################

    def dumpCoords(self):
        '''Dump coordinates

        Returns:
            tuple of longitude and latitude (lon and lat)'''
        return(self.lon,self.lat)

###########################################

    def dumpBounds(self):
        '''Dump bounds is called when onlyBounds=True

        Returns:
           List containing the min and max of longitude and latitude'''
        # this returns a list instead of tuple
        return[np.min(self.lon),np.min(self.lat),np.max(self.lon),np.max(self.lat)]
