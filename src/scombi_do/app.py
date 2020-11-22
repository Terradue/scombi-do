import os
import sys
import logging
import click
import gdal
from pystac import *
from shapely.wkt import loads
from .helpers import *
from .conf import read_configuration
from .pimp import me

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
@click.option('--profile', 'profile', help='Profile')
def entry(red_channel_input, green_channel_input, blue_channel_input, red_band, green_band, blue_band, aoi, resolution, conf, color, profile):
    
    main(red_channel_input, 
         green_channel_input, 
         blue_channel_input, 
         red_band, 
         green_band, 
         blue_band, 
         aoi, 
         resolution,
         conf,
        color,
        profile)


def main(red_channel_input, green_channel_input, blue_channel_input, red_band, green_band, blue_band, aoi, resolution, conf, color, profile):
 

    configuration = read_configuration(conf)

    if aoi == '': 
        aoi = None
        
    logging.info('Scombidooo!')
    
    target_dir = 'combi'
    
    if not os.path.exists(target_dir):
    
        os.mkdir(target_dir)
    
    # read the inputs: bands, items and assets
    bands = [red_band, green_band, blue_band]
    
    # check the color profile:
    if color is None:
        
        try: 
            print(','.join([band for band in bands if band]))
            color = configuration['profiles'][','.join([band for band in bands if band])]['color']
            logging.info('Using profile for {} from configuration'.format(','.join([band for band in bands if band])))
        except KeyError:
            # no profile, stick to data automatic scaling to [0, 255]
            pass
    
    s_expressions = None
    
    try: 
        s_expressions = configuration['profiles'][profile]['expression']
        if s_expressions is not None:
            logging.info('Using s expressions from profile')
    except KeyError:
        pass
    
    if s_expressions is None:
        try: 
            s_expressions = [configuration[b] if b in configuration.keys() else None for b in bands]
            logging.info('Using s expressions from bands'.format(','.join([band for band in bands if band])))
        except KeyError:
            pass
        
    items = []
    assets_href = []
    rescaled = []
    
    for index, input_path in enumerate([red_channel_input, green_channel_input, blue_channel_input]):
    
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
        if aoi is not None:
        
            min_lon, min_lat, max_lon, max_lat = loads(aoi).bounds
        
            output_name = '{}/{}_{}.tif'.format(target_dir, index+1, bands[index])
            #vsi_mem = '/vsimem/{}_inmem_{}.vrt'.format(index, bands[index])
            ds = gdal.Translate(output_name, 
                                asset, 
                                #scaleParams=scaling_factors[index],
                                outputType=gdal.GDT_Int16,
                                projWin=[min_lon, max_lat, max_lon, min_lat],
                                projWinSRS='EPSG:4326')

 

            # copy the original bands to allow titiling 
            #ds = gdal.Translate('{}/{}_{}.tif'.format(target_dir, index+1, bands[index]), 
            #                    asset,
            #                    outputType=gdal.GDT_Int16,
            #                    projWin=[min_lon, max_lat, max_lon, min_lat],
            #                    projWinSRS='EPSG:4326')
        
        else:
            
            #vsi_mem = '/vsimem/{}_inmem_{}.vrt'.format(index, bands[index])
            ds = gdal.Translate(output_name, 
                                asset, 
                                #scaleParams=scaling_factors[index],
                                outputType=gdal.GDT_Int16)

        rescaled.append(ds)

            # copy the original bands to allow titiling 
            #ds = gdal.Translate('{}/{}_{}.tif'.format(target_dir, index+1, bands[index]), 
            #                    asset,
            #                    outputType=gdal.GDT_Int16)
    
    # build a VRT with the rescaled assets with the selected resolution mode
    
    
    logging.info('Build VRT')
    vrt = 'temp.vrt'
    ds = gdal.BuildVRT(vrt,
                       [ds for ds in rescaled if ds],
                       srcNodata=0,
                       resolution=resolution, 
                       separate=True)

    ds.FlushCache()

    ds = None

    del(ds)

    #translate_options = gdal.TranslateOptions(gdal.ParseCommandLine('-co TILED=YES ' \
    #                                                                '-co COPY_SRC_OVERVIEWS=YES ' \
    #                                                                '-co COMPRESS=DEFLATE '))
    
    #gdal.Translate(f'{target_dir}/_combi.tif',
    #               vrt,
    #               options=translate_options)
    
    logging.info('Pimp me')
    # (in_tif, out_tif, bands, s_expressions, ops)
    me(vrt, f'{target_dir}/combi.tif', bands, s_expressions, color)
    
    #temp_mem = '/vsimem/inmem'
    
    logging.info('COGify and saving results')
    
    
    
    #gdal.Translate(f'{target_dir}/combi.tif',
    #                   vrt,
    #                   outputType=gdal.GDT_Byte,
    #                   options=translate_options)
    
    

    #os.remove(vrt)
    
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
