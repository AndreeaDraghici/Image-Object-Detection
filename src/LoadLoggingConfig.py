import logging.config
import yaml


def load_logging_config() :
    try :
        # Load the configuration from the YAML file
        with open('../logging_config.yml', 'r') as config_file :
            # Read and parse the YAML configuration
            config = yaml.safe_load(config_file.read())
            # Configure the logging using the dictionary-based configuration
            logging.config.dictConfig(config)

    except FileNotFoundError as e :
        # Handle the case when the configuration file is not found
        raise RuntimeError("Error: Logging configuration file not found:", e)
    except yaml.YAMLError as e :
        # Handle YAML parsing errors
        raise RuntimeError("Error: Error parsing YAML configuration:", e)
    except Exception as e :
        # Handle other exceptions that might occur during configuration loading
        raise RuntimeError("An error occurred during logging configuration:", e)