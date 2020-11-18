import pkg_resources
import yaml

def read_configuration(conf_file):
    
    if conf_file is None:
        
        conf_file = pkg_resources.resource_filename(__package__, 'assets/conf.yml')
    
    with open(conf_file) as file:
        
        return yaml.safe_load(file)