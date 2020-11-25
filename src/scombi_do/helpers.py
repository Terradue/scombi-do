from pystac import Catalog, extensions
import gdal 
import osr
from urllib.parse import urlparse
import os
import numpy as np
from collections import Counter
gdal.UseExceptions()

def set_env():
    
    if not 'PREFIX' in os.environ.keys():
    
        os.environ['PREFIX'] = '/opt/anaconda/envs/env_vi'

        os.environ['GDAL_DATA'] =  os.path.join(os.environ['PREFIX'], 'share/gdal')
        os.environ['PROJ_LIB'] = os.path.join(os.environ['PREFIX'], 'share/proj')

def fix_asset_href(uri):

    parsed = urlparse(uri)
    
    if parsed.scheme.startswith('http'):
        
        return '/vsicurl/{}'.format(uri)
    
    else:
        
        return uri
        
def get_item(catalog):
    
    cat = Catalog.from_file(catalog) 
    
    try:
        
        collection = next(cat.get_children())
        item = next(collection.get_items())
        
    except StopIteration:

        item = next(cat.get_items())
        
    return item

def get_band_asset_href(item, band):
    
    asset_ref = None
    
    eo_item = extensions.eo.EOItemExt(item)
    
    if (eo_item.bands) is not None:

        for _band in eo_item.bands:
            
             if _band.common_name in [band]:

                asset_ref = fix_asset_href(item.assets[_band.name].get_absolute_href())
                
    return asset_ref

def get_band_asset(item, band):
    
    asset = None
    
    eo_item = extensions.eo.EOItemExt(item)
    
    if (eo_item.bands) is not None:

        for _band in eo_item.bands:
            
             if _band.common_name in [band]:

                asset = item.assets[_band.name]
                
    return asset


def cog(input_tif, output_tif, no_data=None):
    
    translate_options = gdal.TranslateOptions(gdal.ParseCommandLine('-co TILED=YES ' \
                                                                    '-co COPY_SRC_OVERVIEWS=YES ' \
                                                                    '-co COMPRESS=DEFLATE '))
    
    if no_data != None:
        translate_options = gdal.TranslateOptions(gdal.ParseCommandLine('-co TILED=YES ' \
                                                                        '-co COPY_SRC_OVERVIEWS=YES ' \
                                                                        '-co COMPRESS=DEFLATE '\
                                                                        '-a_nodata {}'.format(no_data)))
    ds = gdal.Open(input_tif, gdal.OF_READONLY)

    gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
    ds.BuildOverviews('NEAREST', [2,4,8,16,32])
    
    ds = None

    del(ds)
    
    ds = gdal.Open(input_tif)
    gdal.Translate(output_tif,
                   ds, 
                   options=translate_options)
    ds = None

    del(ds)
    
    if os.path.exists('{}.ovr'.format(input_tif)):
        # not using the mem driver, clean-up
        os.remove('{}.ovr'.format(input_tif))
        os.remove(input_tif)

def get_epsg(epsg, assets_href):

    # get an EPSG code if it hasn't been supplied
    epsg_codes = []

    for asset_href in assets_href:

        if asset_href is None:
  
            epsg_codes.append(None)
            continue
        
        ds = gdal.Open(asset_href)
        proj = osr.SpatialReference(wkt=ds.GetProjection()).GetAttrValue('AUTHORITY',1)
      
        epsg_codes.append(f'EPSG:{proj}')

    if epsg is None:
        # get the most represented code
        epsg = Counter([code for code in epsg_codes if code]).most_common(1)[0][0] 

    return epsg, epsg_codes

def get_mbb(geometries):

    for index, g in enumerate(geometries):
        
        if index == 0:
            mbb = g
        else:
            mbb = mbb.intersection(g)

    return mbb