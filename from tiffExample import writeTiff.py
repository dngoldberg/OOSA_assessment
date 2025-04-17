from tiffExample import writeTiff
from pyproj import Proj, transform
from processLVIS import lvisGround
import argparse
import tracemalloc

tracemalloc.start()

ap = argparse.ArgumentParser(description='Specifys the file and desired resolution')
ap.add_argument("filename", metavar='filename', help="enter the entire file location")
ap.add_argument("resolution", metavar = 'resolution', type=int, help="enter the desired resolution")

args = ap.parse_args()

class TiffLVIS(lvisGround):

    def reprojectLVIS(self,outEPSG):
        inEPSG = Proj("epsg:4326")
        outEPSG = Proj(f"epsg:{outEPSG}")
        self.x, self.y = transform(inEPSG, outEPSG, self.lat, self.lon)
        return self.x, self.y

if __name__ == "__main__":

    filename = args.filename
    resolution = args.resolution

    b = TiffLVIS(filename, onlyBounds=True)

    x0, y0, x1, y1 = b.bounds

    rows = 10
    columns = 10

    width = (x1 - x0) / columns
    height = (y1 - y0) / rows

    gridcounter = 0

    for i in range(rows):
        for j in range(columns):
            gridcounter += 1

            grid_x0 = x0 + j * width
            grid_x1 = x0 + (j + 1) * width
            grid_y0 = y0 + i * height
            grid_y1 = y0 + (i + 1) * height

            try:
                lvis = TiffLVIS(filename, minX=grid_x0, minY=grid_y0, maxX=grid_x1, maxY=grid_y1)
                lvis.setElevations()

                lvis.x, lvis.y = lvis.reprojectLVIS(3031)

                grounds = lvis.estimateGround()

                outputname = f'{gridcounter}_LVIS.tif'

                writeTiff(lvis.zG, lvis.x, lvis.y, resolution, outputname)

            except Exception as e:
                print(f"Error in grid {gridcounter}: {e}")

    peak = tracemalloc.get_traced_memory()[1]
    print(f"{peak/1000000000} GB")

    tracemalloc.stop()
