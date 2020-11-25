import os
import gdal
import numpy as np
from PIL import Image
from io import BytesIO
from base64 import b64encode
from shapely.geometry import shape
from ipyleaflet import ImageOverlay
from urllib.parse import urlparse
import requests
from requests.auth import HTTPBasicAuth
from pystac import STAC_IO

def my_read_method(uri):
    
    parsed = urlparse(uri)
    
    if parsed.scheme.startswith('http'):
    
        if os.environ.get('STAGEIN_PASSWORD') is None:
            
            return requests.get(uri).text
            
        else:
            
            return requests.get(uri, 
                                auth=HTTPBasicAuth(os.environ.get('STAGEIN_USERNAME'), 
                                                   os.environ.get('STAGEIN_PASSWORD'))
                               ).text
    else:
        return STAC_IO.default_read_text_method(uri)

def item_to_img_overlay(item):
    
    dsw = gdal.Warp('/vsimem/warp.tif',
              item.get_assets()['rgb'].get_absolute_href(), 
              dstSRS='EPSG:4326',
              format='GTiff',
               dstAlpha=True)

    ds = gdal.Open('/vsimem/warp.tif')

    _bands = []
    for band_index in [1,2,3,4]:

        band = ds.GetRasterBand(band_index)
        w = band.XSize
        h = band.YSize
        _bands.append(band.ReadAsArray().astype(np.uint8))

    rgb_uint8 = np.dstack(_bands).astype(np.uint8)

    im = Image.fromarray(rgb_uint8)

    f = BytesIO()

    im.save(f, 'png')
    data = b64encode(f.getvalue())

    ds = None
    dsw = None
    del(ds)
    del(dsw)
    
    return ImageOverlay(
            url=b'data:image/png;base64,' + data,
            bounds=((shape(item.geometry).bounds[1], 
                     shape(item.geometry).bounds[0]), 
                    (shape(item.geometry).bounds[3], 
                     shape(item.geometry).bounds[2]))
        )