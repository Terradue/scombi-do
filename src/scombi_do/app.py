import os
import sys
import logging
import click
import gdal
from pystac import *
from shapely.wkt import loads
from .helpers import *
from .conf import read_configuration

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
@click.option('--conf', default=None)
@click.option('--resolution', 'resolution', default='highest', help='highest, lowest, average')
def entry(red_channel_input, green_channel_input, blue_channel_input, red_band, green_band, blue_band, aoi, resolution, conf):
    
    main(red_channel_input, 
         green_channel_input, 
         blue_channel_input, 
         red_band, 
         green_band, 
         blue_band, 
         aoi, 
         resolution,
         conf)


def main(red_channel_input, green_channel_input, blue_channel_input, red_band, green_band, blue_band, aoi, resolution, conf):
 

    configuration = read_configuration(conf)

    if aoi == '': 
        aoi = None
        
    logging.info('Scombidooo!')
    
    target_dir = 'combi'
    
    if not os.path.exists(target_dir):
    
        os.mkdir(target_dir)
    
    # read the inputs: bands, items and assets
    bands = [red_band, green_band, blue_band]
    
    scaling_factors = [configuration[b] if b in configuration.keys() else [[0, 3000, 0, 255]] for b in bands]
    
    items = []
    assets_href = []
    rescaled = []
    
    for index, input_path in enumerate([red_channel_input, green_channel_input, blue_channel_input]):
    
        item = get_item(os.path.join(input_path, 'catalog.json')) 
        
        logging.info(item)
        
        items.append(item)
        assets_href.append(get_band_asset_href(item, bands[index]))
    
    
    # rescale and get the original assets (these are part of the output)
    logging.info('Rescaling and COG for input assets')
    rescaled = []
    for index, asset in enumerate(assets_href):
        
        #ds = gdal.Translate(f'/vsimem/inmem_{index}.vrt', 
        ds = gdal.Translate('{}__{}.tif'.format(index, bands[index]),  
                            asset, 
                            scaleParams=scaling_factors[index],
                            outputType=gdal.GDT_Byte)
        
        ds = gdal.Translate('{}_{}.tif'.format(index, bands[index]), 
                            asset)
        
        cog('{}_{}.tif'.format(index, bands[index]),
            '{}/{}_{}.tif'.format(target_dir, index, bands[index]))
        
        rescaled.append('{}__{}.tif'.format(index, bands[index]))
    
    # build a VRT with the rescaled assets with the selected resolution mode
    vrt = 'temp.vrt'
    
    logging.info('Build VRT')

    ds = gdal.BuildVRT(vrt,
                       rescaled,
                       srcNodata=0,
                       resolution=resolution, 
                       separate=True)

    ds.FlushCache()

    ds = None

    del(ds)
    
    #tif = '_result.tif'

    temp_mem = '/vsimem/inmem'
    
    logging.info('COGify and saving results')
    
    if aoi is not None:
        
        min_lon, min_lat, max_lon, max_lat = loads(aoi).bounds
        print(min_lon, min_lat, max_lon, max_lat)
        print(loads(aoi).wkt)
        gdal.Translate(temp_mem,
                       vrt,
                       outputType=gdal.GDT_Byte,
                       projWin=[min_lon, max_lat, max_lon, min_lat],
                       projWinSRS='EPSG:4326')
    
    else:
    
        gdal.Translate(temp_mem,
                       vrt,
                       outputType=gdal.GDT_Byte)
    
    cog(temp_mem, f'{target_dir}/combi.tif')
    
    # clean-up
    for f in rescaled:
    
        os.remove(f)
        
    os.remove(vrt)
    
    # to STAC
    logging.info('STAC')
    cat = Catalog(id='scombidooo',
                  description="Combined RGB composite") 
    
    item = Item(id='combi',
            geometry=items[0].geometry,
            bbox=items[0].bbox,
            datetime=items[0].datetime,
            properties={}) #items[0].properties)

    item.common_metadata.set_gsd(10)

    eo_item = extensions.eo.EOItemExt(item)

    for index, asset in enumerate(assets_href):

        _asset =  get_band_asset(items[index],
                                 bands[index]) #.clone()
        print(_asset)
        _asset.href = './{}_{}.tif'.format(index, bands[index])

        item.add_asset('{}_{}'.format(index, bands[index]), _asset)

        
    # add the result.tif Asset
    item.add_asset(key='rgb',
                   asset=Asset(href='./combi.tif',
                               media_type=MediaType.COG))
        
    cat.add_items([item])
    
    cat.normalize_and_save(root_href='./',
                           catalog_type=CatalogType.SELF_CONTAINED)
        
    logging.info('Done!')
    
if __name__ == '__main__':
    entry()
