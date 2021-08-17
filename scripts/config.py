import os
import yaml


def fetch():

    # fetch yml config to read essential configurations
    config_file_name = os.environ["HOME"] + "/.wordpress-cli.yml"
    with open(config_file_name, 'r') as yml_file:
        cfg = yaml.load(yml_file, Loader=yaml.FullLoader)

    return cfg
