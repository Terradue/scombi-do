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

    logging.info('Hello World!')
    
    bands = [red_band, green_band, blue_band]
    
    items = []
    assets = []
    
    for index, input_path in enumerate([red_channel_input, green_channel_input, blue_channel_input]):
    
        item = get_item(os.path.join(input_path, 'catalog.json')) 
        
        logging.info(item)
        
        items.append(item)
        
        assets.append(get_band_asset(item, bands[index]))
    
    vrt = 'temp.vrt'
    
    ds = gdal.BuildVRT(vrt,
                       assets,
                       srcNodata=0,
                       resolution='highest', 
                       separate=True)

    ds.FlushCache()

    ds = None

    del(ds)
    
    tif = '_result.tif'

    if aoi is not None:
        
        min_lon, min_lat, max_lon, max_lat = loads(aoi['value']).bounds
    
        gdal.Translate(tif,
                       vrt,
                       outputType=gdal.GDT_Int16,
                       projWin=[min_lon, max_lat, max_lon, min_lat],
                       projWinSRS='EPSG:4326')
    
    else:
    
        gdal.Translate(tif,
                       vrt,
                       outputType=gdal.GDT_Byte)
    
    os.remove(vrt)
    
    cog('_result.tif', 'result.tif')
    
    logging.info('Done!')
    
if __name__ == '__main__':
    entry()
