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


def me(in_tif, out_tif, bands, s_expressions, ops): #='Gamma RGB 3.5 Saturation 1.4 Sigmoidal RGB 15 0.45'):

    bands = [band for band in bands if band]

    logging.info(len(bands))
    # read the input tif, it's the VRT
    ds = gdal.Open(in_tif)
    width = ds.RasterXSize
    height = ds.RasterYSize

    input_geotransform = ds.GetGeoTransform()
    input_georef = ds.GetProjectionRef()

    # the lenght of bands (same as ds.RasterCount) tells us how many inputs we have
    ctx = dict()
    
    ctx['v1'] = ds.GetRasterBand(1).ReadAsArray() 

    if len(bands) > 1:

        ctx['v2'] = ds.GetRasterBand(2).ReadAsArray()

    if len(bands) == 3:

        ctx['v3'] = ds.GetRasterBand(3).ReadAsArray()

    logging.info(ctx)

    ds = None
    
    del(ds)

    # apply the expressions to the bands
    arr = np.stack([snuggs.eval(s_expression, **ctx) for s_expression in s_expressions])

    # apply the color operations using rio color
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
                           len(s_expressions), 
                           gdal.GDT_Byte)

    output.SetGeoTransform(input_geotransform)
    output.SetProjection(input_georef)

    for index in range(1, len(s_expressions)+1):

        logging.info('Adding band {} of {}'.format(index, len(s_expressions)))

        output.GetRasterBand(index).WriteArray((arr[index-1] * 255).astype(np.int))

    output.FlushCache()

    sleep(5)

    output = None

    del(output)

    return True