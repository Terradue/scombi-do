import os
import sys
import logging
import click
import gdal
from pystac import *
from shapely.wkt import loads
from .helpers import *
from .conf import read_configuration
from . import pimp 

logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')


@click.command()
@click.option('--red-channel-input', '-r', 'red_channel_input', help='')
@click.option('--green-channel-input', '-g', 'green_channel_input', default=None, help='')
@click.option('--blue-channel-input', '-b', 'blue_channel_input', default=None, help='')
@click.option('--red-band', 'red_band', help='')
@click.option('--green-band', 'green_band', default=None, help='')
@click.option('--blue-band', 'blue_band', default=None, help='')
@click.option('--aoi', '-a', 'aoi', default=None, help='')
@click.option('--conf', default=None)
@click.option('--resolution', 'resolution', default='highest', help='highest, lowest, average')
@click.option('--color_expression', 'color', default=None, help='Color expression')
@click.option('--profile', 'profile', default=None, help='Profile')
@click.option('--lut', 'lut', default=None, help='Matplotlib colormap')
@click.option('--s_expression', 's_expression', multiple=True, default=None)
def entry(red_channel_input, green_channel_input, blue_channel_input, red_band, green_band, blue_band, aoi, resolution, conf, color, profile, lut, s_expression):
    
    logging.info('Scombidooo!')

    configuration = read_configuration(conf)

    s_expressions = None

    if s_expression:

        s_expressions = list(s_expression)
        logging.info('Using s expressions: {}'.format(','.join(s_expressions)))

    if not s_expressions: 

        if profile:

            try: 
                s_expressions = configuration['profiles'][profile]['expression']
                if s_expressions is not None:
                    logging.info('Using s expressions from profile: {}'.format(','.join(s_expressions)))
            except KeyError:
                
                print('Provide a profile or one or more s expressions')
                sys.exit(1)
        else:

            print('Provide a profile or one or more s expressions')
            sys.exit(1)

    print(s_expressions)

    # get the color profile via CLI parameter or via configuration
    if color is None:
        
        try: 
            color = configuration['profiles'][profile]['color']
            logging.info('Using color enhancement for profile "{}" from configuration: {}'.format(profile, color))
        except KeyError:
            logging.info('No profile or color expression provided, results are provided without enhancement')

    # read the inputs: bands, items and assets
    bands = [red_band, green_band, blue_band]

    channel_inputs = [red_channel_input, green_channel_input, blue_channel_input]

    # an empty string AOI becomes None (CWL params policy) 
    if aoi == '': 
        aoi = None

    print('channel_inputs ', channel_inputs)
    print('bands ', bands)
    print('profile ', profile)
    print('color ', color)


    main(channel_inputs=channel_inputs,
         bands=bands,
         configuration=configuration,
         s_expressions=s_expressions, 
         resolution=resolution,
         aoi=aoi, 
         color=color,
         profile=profile,
         lut=lut)

def main(channel_inputs, bands, configuration, s_expressions, resolution='highest', aoi=None, color=None, profile=None, lut=None):

    target_dir = 'combi'
    
    if not os.path.exists(target_dir):
    
        os.mkdir(target_dir)
        
    items = []
    assets_href = []
    rescaled = []
    
    for index, input_path in enumerate(channel_inputs):
    #for index, input_path in enumerate([red_channel_input, green_channel_input, blue_channel_input]):
    
        if input_path is None:
            
            items.append(None)
            assets_href.append(None)
            continue
            
        item = get_item(os.path.join(input_path, 'catalog.json')) 
        
        logging.info(item)
        
        items.append(item)
        assets_href.append(get_band_asset_href(item, bands[index]))
    
    # rescale and get the original assets (these are part of the output)
    logging.info('Rescaling and COG for input assets')
    rescaled = []
    
    for index, asset in enumerate(assets_href):

        if asset is None:
            
            rescaled.append(None)
            
            continue
            
        logging.info('Getting band {} from {}'.format(bands[index], asset))
        
        output_name = '{}/{}_{}.tif'.format(target_dir, index+1, bands[index])

        if aoi is not None:

            min_lon, min_lat, max_lon, max_lat = loads(aoi).bounds
            
            ds = gdal.Translate(output_name, 
                                asset, 
                                outputType=gdal.GDT_Int16,
                                projWin=[min_lon, max_lat, max_lon, min_lat],
                                projWinSRS='EPSG:4326')
        
        else:
            ds = gdal.Translate(output_name, 
                                asset, 
                                outputType=gdal.GDT_Int16)

        rescaled.append(ds)
    
    # build a VRT with the rescaled assets with the selected resolution mode
    logging.info('Build VRT')
    vrt = 'temp.vrt'
    ds = gdal.BuildVRT(vrt,
                       [ds for ds in rescaled if ds],
                       srcNodata=0,
                       resolution=resolution, 
                       separate=True)

    ds.FlushCache()
    
    logging.info('Pimp me')
    # (in_tif, out_tif, bands, s_expressions, ops)
    pimp.me(vrt, f'{target_dir}/combi.tif', bands, s_expressions, color, lut)
    
    logging.info('COGify and saving results')
    
    ds = None
    del(ds)
    
    # to STAC
    logging.info('STAC')
    cat = Catalog(id='scombidooo',
                  description="Combined RGB composite") 
    
    # TODO fix geometry, bbox
    item = Item(id='combi',
                geometry=items[0].geometry,
                bbox=items[0].bbox,
                datetime=items[0].datetime,
                properties={}) #items[0].properties)

    # TODO fix gsd
    item.common_metadata.set_gsd(10)

    eo_item = extensions.eo.EOItemExt(item)

    for index, asset in enumerate(assets_href):
        if asset is None:
            continue
        _asset =  get_band_asset(items[index],
                                 bands[index]) 
      
        _asset.href = './{}_{}.tif'.format(index+1, bands[index])

        item.add_asset('{}_{}'.format(index+1, bands[index]), _asset)

        
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
