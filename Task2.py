'''
Task 2

'''
from tiffExample import writeTiff
from pyproj import Proj, transform
from processLVIS import lvisGround
import argparse
import tracemalloc
import os
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import matplotlib.pyplot as plt
import numpy as np


##########################################

tracemalloc.start()

ap = argparse.ArgumentParser(description='Specifys the file and desired resolution')
ap.add_argument("filename", metavar='filename', help="enter the entire file location")
ap.add_argument("resolution", metavar = 'resolution', type=int, help="enter the desired resolution")
ap.add_argument("--mask", metavar = 'mask', help='enter the type of mask',default = None)
ap.add_argument("--searchdist", metavar = 'searchdist', help='enter the interpolation distance',default = None)
ap.add_argument("--filename2", metavar ='filename2', help='enter the second entire file location',default=None)

args = ap.parse_args()

##########################################

class TiffLVIS(lvisGround):

    def reprojectLVIS(self,outEPSG):
        inEPSG = Proj("epsg:4326")
        outEPSG = Proj(f"epsg:{outEPSG}")
        self.x,self.y=transform(inEPSG, outEPSG,self.lat,self.lon)
        return self.x , self.y
    """Method which reprojects from WSG84 to a specified CRS, correspdoning to the target Coordinate Reference System"""

    def LoadData(self, filename, resolution):
     
        print(f"File: {filename}")
        print(f"Resolution: {resolution}")

        b=TiffLVIS(filename,onlyBounds=True)

  
        xmin=b.bounds[0]
        ymin=b.bounds[1]
        xmax=b.bounds[2]
        ymax=b.bounds[3]

        rows = 10
        columns = 10

        width = (xmax-xmin) / columns
        height = (ymax-ymin) / rows

        gridcounter = 0

        for i in range(columns):
            for j in range(rows):
                gridcounter += 1

                try:
                    x0 = xmin + j * width
                    y0 = ymin + i * height
                    x1 = x0 + width
                    y1 = y0 + height

                    # Create a new TiffLVIS object for the current grid section
                    lvis = TiffLVIS(filename, minX=x0, minY=y0, maxX=x1, maxY=y1)

                    lvis.setElevations()
                    lvis.x, lvis.y = lvis.reprojectLVIS(3031)

                    minX = np.min(lvis.x)
                    minY = np.min(lvis.y)
                    maxX = np.max(lvis.x)
                    maxY = np.max(lvis.y)

                    if minX < -1580000:
                        if minY > -340000:
                            if maxX > -1630000:
                                if maxY < -260000:
                            
                                    grounds = lvis.estimateGround()

                                    outputname = f'{gridcounter}_LVIS.tif'

                                    writeTiff(lvis.zG, lvis.x, lvis.y, resolution, outputname)

                                else:
                                    print(f"Area {gridcounter} not within the glacier bounds")
                                    continue

                except AttributeError as e:
                    print(f"Area {gridcounter} has no data")

        folder = os.getcwd()

        files = os.listdir(folder)

        Rasters = []

        for file in files:
            if file[-9:] == '_LVIS.tif':
                src = rasterio.open(file)
                Rasters.append(src)

        mosaic, out_trans = merge(Rasters)

        out_meta = Rasters[0].meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": out_trans,
            "crs": "EPSG:3031"
        }) 
        
        filecode = filename[-10:-4]
        out_fp = os.path.join(os.getcwd(), f"LVIS{filecode}.tif")
        
        with rasterio.open(out_fp, "w", **out_meta) as dest:
            dest.write(mosaic)

            for file in files:
                if file[-9:] == ("_LVIS.tif"):
                    file_path = os.path.join(folder, file)
                    os.remove(file_path)  
                    print(f"Deleted {file_path}")

######################################### 

if __name__=="__main__":

    lvis_data = TiffLVIS(args.filename, args.resolution)
    lvis_data.LoadData(args.filename, args.resolution)
  
peak = tracemalloc.get_traced_memory()[1]
print(f"{peak/1000000000} GB")

    
tracemalloc.stop