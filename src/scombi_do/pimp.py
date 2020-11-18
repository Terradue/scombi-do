from rio_color.operations import parse_operations
import numpy as np
import gdal
from time import sleep
import os


def me(in_tif, out_tif, ops='Gamma RGB 3.5 Saturation 1.4 Sigmoidal RGB 15 0.45'):
    
    scaling_factor = 10000
    
    ds = gdal.Open(in_tif)
    
    width = ds.RasterXSize
    height = ds.RasterYSize

    input_geotransform = ds.GetGeoTransform()
    input_georef = ds.GetProjectionRef()
    #for _input in inputs:
        
    #    ds.append(gdal.Open(_input))
    
        
    arr = np.stack([ds.GetRasterBand(b).ReadAsArray() / scaling_factor for b in [1, 2, 3]])
    
    ds = None
    
    del(ds)
    
    if ops is not None:
        
        arr = np.clip(arr, 0, 1)

        assert arr.shape[0] == 3
        assert arr.min() >= 0
        assert arr.max() <= 1


        for func in parse_operations(ops):
            arr = func(arr) 
        
    # save
    driver = gdal.GetDriverByName('GTiff')

    output = driver.Create(out_tif, 
                           width, 
                           height, 
                           3, 
                           gdal.GDT_Byte)

    output.SetGeoTransform(input_geotransform)
    output.SetProjection(input_georef)
    output.GetRasterBand(1).WriteArray((arr[0] * 255).astype(np.int))
    output.GetRasterBand(2).WriteArray((arr[1] * 255).astype(np.int))
    output.GetRasterBand(3).WriteArray((arr[2] * 255).astype(np.int))
    output.FlushCache()

    sleep(5)

    output = None

    del(output)
   
    
    return True