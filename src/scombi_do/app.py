import os
import sys
import logging
import click
import gdal
from .helpers import *

logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')


@click.command()
@click.option('--red-channel-input', '-r', 'red_channel_input', help='')
@click.option('--green-channel-input', '-g', 'green_channel_input', help='')
@click.option('--blue-channel-input', '-b', 'blue_channel_input', help='')
@click.option('--red-band', 'red_band', help='')
@click.option('--green-band', 'green_band', help='')
@click.option('--blue-band', 'blue_band', help='')
@click.option('--aoi', '-a', 'aoi', default=None, help='')
def entry(red_channel_input, green_channel_input, blue_channel_input, red_band, green_band, blue_band, aoi):
    
    main(red_channel_input, 
         green_channel_input, 
         blue_channel_input, 
         red_band, 
         green_band, 
         blue_band, 
         aoi)


def main(red_channel_input, green_channel_input, blue_channel_input, red_band, green_band, blue_band, aoi):

    logging.info('Scombidooo!')
    
    bands = [red_band, green_band, blue_band]
    
    items = []
    assets = []
    rescaled = []
    
    for index, input_path in enumerate([red_channel_input, green_channel_input, blue_channel_input]):
    
        item = get_item(os.path.join(input_path, 'catalog.json')) 
        
        logging.info(item)
        
        items.append(item)
        
        assets.append(get_band_asset(item, bands[index]))
    
    
    logging.info('Rescaling and COG for input assets')
    rescaled = []
    for index, asset in enumerate(assets):
        
        ds = gdal.Translate(f'/vsimem/inmem_{index}.vrt', 
                            asset, 
                            scaleParams=[[0,3000,0,255]])
        
        ds = gdal.Translate('_{}.tif'.format(bands[index]), 
                            asset)
        
        cog('_{}.tif'.format(bands[index]),
            '{}.tif'.format(bands[index]))
        
        rescaled.append(ds)
    
    vrt = 'temp.vrt'
    
    logging.info('Build VRT')

    ds = gdal.BuildVRT(vrt,
                       rescaled,
                       srcNodata=0,
                       resolution='highest', 
                       separate=True)

    ds.FlushCache()

    ds = None

    del(ds)
    
    #tif = '_result.tif'

    temp_mem = '/vsimem/inmem'
    
    logging.info('COG and saving results')
    
    if aoi is not None:
        
        min_lon, min_lat, max_lon, max_lat = loads(aoi['value']).bounds
    
        gdal.Translate(temp_mem,
                       vrt,
                       outputType=gdal.GDT_Int16,
                       projWin=[min_lon, max_lat, max_lon, min_lat],
                       projWinSRS='EPSG:4326')
    
    else:
    
        gdal.Translate(temp_mem,
                       vrt,
                       outputType=gdal.GDT_Byte)
    
    os.remove(vrt)
    
    cog(temp_mem, 'result.tif')
    
    logging.info('Done!')
    
if __name__ == '__main__':
    entry()
