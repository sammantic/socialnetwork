from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    name: str
    host: str
    port: int
    user_db: str
    password: str

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/config/.env")


@lru_cache()
def get_config() -> Settings:
    """
    Read a config file base on the environment
    the default environment is dev

    :return:
    Object of ConfigParser
    """

    config_file = BASE_DIR / f"config/.env"

    if not config_file.exists():  # Check if the configuration file does not exist
        raise FileNotFoundError(f"Configuration file '{config_file}' not found")

    config = Settings()

    return config

