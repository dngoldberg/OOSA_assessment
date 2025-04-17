import rasterio     #higher level package raster functions
from rasterio.merge import merge
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
from osgeo import gdal             # pacage for handling geotiff data
from osgeo import osr              # pacage for handling projection information
import numpy as np
from pyproj import Transformer
from scipy.ndimage import generic_filter

from source.processLVIS import lvisGround

#eventually change this is own tiff class

class HandleTiff(lvisGround):
    ''' Class to handle geotiff files'''
##############################################

    # would ideally have write tiff function within this class

    # would add a function loop tiles/load data here to reduce duplication within the tasks 

#############################################################

    def reprojectLVIS(self,outEPSG):
        '''Reproject the data
        
        Args: 
            outEPSG = chosen out projection

        Returns:
            self.x and self.y that have been reprojected
        '''
        #set projections as direct strings
        inEPSG = "EPSG:4326"
        outEPSG = f"EPSG: {outEPSG}"
        #use transformer so dont deprecate with transform
        transformer = Transformer.from_crs(inEPSG, outEPSG, always_xy=True) #always long,lat order
        #reproject x and y
        self.x, self.y = transformer.transform(self.lon, self.lat)
        return self.x, self.y

###################################################

    def merge_tiles(self, input_dir, output_path):
        '''A function to merge the tiles within the specifed folder
        
        Args:
            input_dir = input directory 
            output_path = where the merged tiff would be saved
        
        Returns:
            saves a merged tiff
        '''

        # call all tif files in input folder
        tile_files = glob.glob(os.path.join(input_dir,'*tif'))

        # open tiles
        src_files_to_mosaic = []    # create empty array
        for fp in tile_files:       # loop over file paths
            src = rasterio.open(fp)
            src_files_to_mosaic.append(src)

        # merge with rasterio + maintain georeference
        mosaic, out_trans = merge(src_files_to_mosaic)

        # set mo data to NaN before export
        mosaic = np.where(mosaic == -999.0, np.nan, mosaic)

        # save merged file
        with rasterio.open(output_path, "w", driver='GTiff', #create output_tiff, specify format
                           height=mosaic.shape[1],  # tiff is same height as input
                           width=mosaic.shape[2],   # tiff is same width as input
                           count=1, dtype=rasterio.float32,     # can handle NaN
                           crs=src_files_to_mosaic[0].crs,  # uses same crs as input file
                           transform=out_trans) as dest:
                            dest.write(mosaic[0], 1)    # writes to first band 

        for src in src_files_to_mosaic:     # closes to free space 
                src.close()

        print(f'Merged DEM is saved as {output_path}')

###################################################

    def visualise_tiff(self, tiff_path, plot_filename):
        '''A function to visulaise the output via rasterio
        
        Args:
            tiff_path = saves to specified output folder with chosen output name 
            plot_filename = title of plot with .png
        
        Returns:
            saves a plot of a raster image
        '''
        # open the tiff to visualise with rasterio
        dataset = rasterio.open(tiff_path)
        # print raster dimensions
        print(f'The raster is {dataset.width} x {dataset.height}  pixels')
        print(dataset.crs)      #print projection

        merged_image = dataset.read(1)  #read band

        # make plot
        plt.figure(figsize=(6,10))
        plt.imshow(merged_image, cmap='cividis')
        plt.colorbar(label='Elevation (m)')      # legend
        plt.xlabel('Metres', fontsize=14)
        plt.ylabel('Metres', fontsize=14)
        plt.title(plot_filename)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        plt.show()
