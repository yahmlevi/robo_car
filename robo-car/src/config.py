import logging
import yaml

class Config(object):

    def __init__(self):
        # logging.info('Starting Car, system info: ' + sys.version)

        with open(r'data/config.yaml') as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            # config = yaml.load(file, Loader=yaml.FullLoader)

            self.config_dict = yaml.load(file)

    def get_dict(self):
        return self.config_dict

        
