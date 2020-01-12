import logging
import yaml

class Config(object):

    def __init__(self):
        # logging.info('Starting Car, system info: ' + sys.version)

        # self.file

        with open(r'data/config.yaml', 'r') as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            # config = yaml.load(file, Loader=yaml.FullLoader)

            self.config_dict = yaml.load(file)

    # def get_dict(self):
    #     return self.config_dict

    def get(self, key, base_key = None):
        result = self.config_dict

        if base_key is not None:
            key = base_key + "." + key
        
        arr = key.split(".")
        for k in arr:
            result = result[k]

        return result
            

    def save(self):
        with open(r'data/config.yaml', 'w') as file:
            yaml.dump(self.config_dict, file)

        
