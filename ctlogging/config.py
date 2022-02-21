import logging
import yaml
import logging.config

APP_LOGGER_NAME = "App"


def set_logger(config: dict):
    logging.config.dictConfig(config)
    global APP_LOGGER_NAME
    root_logger_name = config["root_logger_name"]
    APP_LOGGER_NAME = root_logger_name
    logger = logging.getLogger(root_logger_name)
    return logger


def set_logger_from_yaml(yamlfilepath: str = None):
    with open(yamlfilepath, "r") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    return set_logger(config)


def get_logger(module_name):
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)
