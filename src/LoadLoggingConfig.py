import logging.config
import yaml


def load_logging_config() :
    try :
        # Încarcă configurația din fișierul YAML
        with open('../logging_config.yml', 'r') as config_file :
            config = yaml.safe_load(config_file.read())
            logging.config.dictConfig(config)
    except FileNotFoundError as e :
        RuntimeError("Error: Logging configuration file not found:", e)
    except yaml.YAMLError as e :
        RuntimeError("Error: Error parsing YAML configuration:", e)
    except Exception as e :
        RuntimeError("An error occurred during logging configuration:", e)
