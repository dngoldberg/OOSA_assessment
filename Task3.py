'''
Task 3

'''
# importing neccesary elements

import os
from matplotlib import pyplot as plt
import numpy as np
#from pyproj import Proj, transform
from osgeo import gdal
#from tiffExample import writeTiff
import rasterio
from rasterio.merge import merge
#from rasterio.plot import show
from Task2 import TiffLVIS
from Task2 import args

##########################################


##########################################
      
import os

class TiffBatch(TiffLVIS):
    def __init__(self, inputfolder, resolution):
        self.inputfolder = inputfolder
        self.resolution = resolution 

    def AllRasters(self, filename, resolution):
        files = os.listdir(self.inputfolder)
        print(files)

        for file in files:
            if file[-3:] == '.h5':
                try:
                    print(file)
                    filename = os.path.join(self.inputfolder, file)
                    self.LoadData(filename, self.resolution)  # Pass resolution to LoadData
                except Exception as e:
                    print("Error processing:", e)

    def MergeTiff(self):
        Rasters = []

        files = os.listdir(os.getcwd())
        
        for file in files:
            if file[:5] == ('LVIS_'):
  
                file_path = os.path.join(os.getcwd(), file)
                    
                src = rasterio.open(file_path)
                Rasters.append(src)

        print(Rasters)

        mosaic, out_trans = merge(Rasters)

        out_meta = Rasters[0].meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": out_trans,
            "crs": "EPSG:3031"
        }) 
        
        if args.filename == "/geos/netdata/oosa/assignment/lvis/2009":
            year = 2009
        else:
            year = 2015
            #change
    
        out_fp = os.path.join(os.getcwd(), f"{year}_ComboLVIS.tif")
        
        with rasterio.open(out_fp, "w", **out_meta) as dest:
            dest.write(mosaic)

            for file in files:
                if file[0:4] == ("LVIS"):
                    file_path = os.path.join(os.getcwd(), file)
                    os.remove(file_path)  
                    print(f"Deleted {file_path}")



if __name__ == "__main__":

    batch = TiffBatch(args.filename, args.resolution)  # Initialize with the folder and resolution
    batch.AllRasters(args.filename, args.resolution)  
    batch.MergeTiff()
    
      # Call the method to process files












            


    
