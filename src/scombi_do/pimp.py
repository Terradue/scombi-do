from rio_color.operations import parse_operations
import numpy as np
import gdal
from time import sleep
import os
import sys
import snuggs
import logging

logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')

def pimp_3(ds, out_tif, s_expressions, ops):
    
    logging.info('Applying s expressions {}'.format(';'.join(s_expressions)))
    
    width = ds.RasterXSize
    height = ds.RasterYSize

    input_geotransform = ds.GetGeoTransform()
    input_georef = ds.GetProjectionRef()
    
    arr = np.stack([snuggs.eval(s_expressions[b], 
                                v=ds.GetRasterBand(b+1).ReadAsArray()) for b in [0, 1, 2]])
    
    print(ds.GetRasterBand(1).ReadAsArray())
    print(arr[0])
    ds = None
    
    del(ds)
    
    if ops is not None:
        
        #arr = np.clip(arr, 0, 1)

        assert arr.shape[0] == 3
        assert arr.min() >= 0
        assert arr.max() <= 1

        logging.info('Applying color operations: {}'.format(ops))
        
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

def pimp_2(ds, out_tif, s_expressions):
    
    logging.info('Applying s expressions {}'.format(';'.join(s_expressions)))
    
    width = ds.RasterXSize
    height = ds.RasterYSize

    input_geotransform = ds.GetGeoTransform()
    input_georef = ds.GetProjectionRef()
    
    arr = snuggs.eval(s_expressions[0], 
                      v1=ds.GetRasterBand(1).ReadAsArray(),
                      v2=ds.GetRasterBand(2).ReadAsArray())
    
    print(arr)
    # apply cmap
    # TODO
        
    # save
    driver = gdal.GetDriverByName('GTiff')

    output = driver.Create(out_tif, 
                           width, 
                           height, 
                           1, 
                           gdal.GDT_Byte)

    output.SetGeoTransform(input_geotransform)
    output.SetProjection(input_georef)
    output.GetRasterBand(1).WriteArray((arr * 255).astype(np.int))
    

    ct = gdal.ColorTable()
    for i in range(256):
        ct.SetColorEntry( i, (255, 255 - i, i, 255) )
    output.GetRasterBand(1).SetRasterColorTable( ct )
    
    output.FlushCache()
    sleep(5)

    output = None

    del(output)
    
    return True


def me(in_tif, out_tif, bands, configuration): #='Gamma RGB 3.5 Saturation 1.4 Sigmoidal RGB 15 0.45'):
    
    scaling_factor = 10000
    
    ds = gdal.Open(in_tif)
    
    
    
    print(ds.RasterCount)
    
    if ds.RasterCount == 3:
        
        pimp_3(ds, out_tif, s_expressions, ops)
        
        return True
    
    if ds.RasterCount == 2:
        
        pimp_2(ds, out_tif, s_expressions)
        
        return True
    
        
        #arr = np.stack([snuggs.eval(s_expressions[b], 
         #                           v=ds.GetRasterBand(b+1).ReadAsArray()) for b in [0, 1, 2]])
        
    #for _input in inputs:
        
    #    ds.append(gdal.Open(_input))
    
    # snuggs.eval("(+ (asarray 1 1) b)", b=np.array([2, 2]))
    
    # apply the s expression to numpy array 
    
    
    #arr = np.stack([ds.GetRasterBand(b).ReadAsArray() / scaling_factor for b in [1, 2, 3]])
    
    #ds = None
    
    #del(ds)
    
#     if ops is not None:
        
#         arr = np.clip(arr, 0, 1)

#         assert arr.shape[0] == 3
#         assert arr.min() >= 0
#         assert arr.max() <= 1


#         for func in parse_operations(ops):
#             arr = func(arr) 
        
#     # save
#     driver = gdal.GetDriverByName('GTiff')

#     output = driver.Create(out_tif, 
#                            width, 
#                            height, 
#                            3, 
#                            gdal.GDT_Byte)

#     output.SetGeoTransform(input_geotransform)
#     output.SetProjection(input_georef)
#     output.GetRasterBand(1).WriteArray((arr[0] * 255).astype(np.int))
#     output.GetRasterBand(2).WriteArray((arr[1] * 255).astype(np.int))
#     output.GetRasterBand(3).WriteArray((arr[2] * 255).astype(np.int))
#     output.FlushCache()

#     sleep(5)

#     output = None

#     del(output)
   
    
    return True