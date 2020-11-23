from rio_color.operations import parse_operations
import numpy as np
import gdal
from time import sleep
import os
import sys
import snuggs
import logging
from matplotlib import cm

logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')

def me(in_tif, out_tif, bands, s_expressions, ops, lut=None): 

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

    # apply the expressions to the bands
    arr = np.stack([snuggs.eval(s_expression, **ctx) for s_expression in s_expressions])

    # apply the color operations using rio color
    if ops is not None:

        assert arr.shape[0] == 3
        assert arr.min() >= 0
        assert arr.max() <= 1

        logging.info('Applying color operations: {}'.format(ops))
        
        for func in parse_operations(ops):

            arr = func(arr) 

    if lut is not None:
        logging.info('Applying look-up table')
        temp_arr = cm.get_cmap(lut)(arr)

        arr = np.array([temp_arr[0][:,:,0],
                        temp_arr[0][:,:,1],
                        temp_arr[0][:,:,2]])


    # save
    driver = gdal.GetDriverByName('GTiff')

    output = driver.Create(out_tif, 
                           width, 
                           height, 
                           arr.shape[0], 
                           gdal.GDT_Byte)

    output.SetGeoTransform(input_geotransform)
    output.SetProjection(input_georef)


    for index in range(1, arr.shape[0]+1):

        logging.info('Adding band {} of {}'.format(index, arr.shape[0]))

        output.GetRasterBand(index).WriteArray((arr[index-1] * 255).astype(np.int))

    output.FlushCache()

    sleep(5)

    output = None

    del(output)
    
    ds = None
    
    del(ds)

    return True