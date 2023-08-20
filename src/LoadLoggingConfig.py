import logging.config
import yaml


def load_logging_config() :
    # Încarcă configurația din fișierul YAML
    with open('../logging_config.yml', 'r') as config_file :
        config = yaml.safe_load(config_file.read())
        logging.config.dictConfig(config)