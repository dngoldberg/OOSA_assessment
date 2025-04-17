'''Task 5 - calcualting th elevation change between the two DEMs'''

'''pseudo-code for calculating change functions

arg parser for file inputs and output name 

define elev change (masked inputs)
    boundedDEM2009 - boundedDEM2015

define calc_volume (masked elev change)
    get meta data on pixel size
    elevation difference * pixel area
    print total volume change (convert from m3 to km3)

define function named quantifyChange 
    read both DEM files (band 1) with rasterio
    get the dimensions of the rasters and crs and check they align
        (would need to add this to a prev function)
    determine areas where both overlap - boolean mask
        (both rasters have data in location)
    call elev_change
    call calc_volume
    save total change map as a geotiff
    visualise with rasterio

call quantify change(boundedDEM2009, boundedDEM2015, -o)
'''

