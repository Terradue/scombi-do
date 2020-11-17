import os
import sys
import logging
import click
import gdal
from pystac import *
from shapely.wkt import loads
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
    
    target_dir = 'combi'
    
    if not os.path.exists(target_dir):
    
        os.mkdir(target_dir)
    
    
    bands = [red_band, green_band, blue_band]
    
    items = []
    assets_href = []
    rescaled = []
    
    for index, input_path in enumerate([red_channel_input, green_channel_input, blue_channel_input]):
    
        item = get_item(os.path.join(input_path, 'catalog.json')) 
        
        logging.info(item)
        
        items.append(item)
        assets_href.append(get_band_asset_href(item, bands[index]))
    
    
    logging.info('Rescaling and COG for input assets')
    rescaled = []
    for index, asset in enumerate(assets_href):
        
        #ds = gdal.Translate(f'/vsimem/inmem_{index}.vrt', 
        ds = gdal.Translate('__{}.tif'.format(bands[index]),  
                            asset, 
                            scaleParams=[[0,3000,0,255]],
                            outputType=gdal.GDT_Byte)
        
        ds = gdal.Translate('_{}.tif'.format(bands[index]), 
                            asset)
        
        cog('_{}.tif'.format(bands[index]),
            '{}/{}.tif'.format(target_dir, bands[index]))
        
        rescaled.append('__{}.tif'.format(bands[index]))
    
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
        
        min_lon, min_lat, max_lon, max_lat = loads(aoi).bounds
    
        gdal.Translate(temp_mem,
                       vrt,
                       outputType=gdal.GDT_Byte,
                       projWin=[min_lon, max_lat, max_lon, min_lat]) #,
                       #projWinSRS='EPSG:4326')
    
    else:
    
        gdal.Translate(temp_mem,
                       vrt,
                       outputType=gdal.GDT_Byte)
    
    # clean-up
    for f in rescaled:
    
        os.remove(f)
        
    os.remove(vrt)
    
    cog(temp_mem, f'{target_dir}/result.tif')
    
    # to STAC
    logging.info('STAC')
    cat = Catalog(id='scombidooo',
                  description="Combined RGB composite") 
    
    item = Item(id='item_name',
            geometry=items[0].geometry,
            bbox=items[0].bbox,
            datetime=items[0].datetime,
            properties=items[0].properties)

    item.common_metadata.set_gsd(10)

    eo_item = extensions.eo.EOItemExt(item)

    for index, asset in enumerate(assets_href):

        _asset =  get_band_asset(items[index],
                                 bands[index]) #.clone()
        print(_asset)
        _asset.href = './{}.tif'.format(bands[index])

        item.add_asset(bands[index], _asset)

        
    # add the result.tif Asset
    item.add_asset(key='combi',
                   asset=Asset(href='./result.tif',
                               media_type=MediaType.GEOTIFF))
        
    cat.add_items([item])
    
    catalog.normalize_and_save(root_href='./',
                               catalog_type=CatalogType.SELF_CONTAINED)
        
    logging.info('Done!')
    
if __name__ == '__main__':
    entry()
