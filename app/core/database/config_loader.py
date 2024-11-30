import os
from configparser import ConfigParser
from pathlib import Path
from functools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent.parent


@lru_cache()
def get_config(environment: str = None) -> ConfigParser:
    """
    Read a config file base on the environment
    the default environment is dev

    :param environment: environment name
    :return:
    Object of ConfigParser
    """
    environment = environment or os.getenv("APP_ENV", "dev")
    config_file = BASE_DIR / f"config/config.{environment}.ini"

    if not config_file.exists():  # Check if the configuration file does not exist
        raise FileNotFoundError(f"Configuration file '{config_file}' not found")

    config = ConfigParser()
    config.read(config_file)

    return config


def get_setting(section: str, key: str) -> str:
    """
    get a value from configParser

    :param section:
    :param key:
    :return:
    str: a config value
    """
    config = get_config()
    return config.get(section, key)



