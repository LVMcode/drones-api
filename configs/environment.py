from functools import lru_cache
from pydantic import BaseSettings


class EnvironmentSettings(BaseSettings):
    IMAGES_SERVER_PROTOCOL: str = "http"
    IMAGES_SERVER: str = "127.0.0.1"
    IMAGES_SERVER_PORT: int = 8000
    IMAGE_FILE_SIZE_LIMIT_MB: int = 3
    API_PORT: int = 8000
    DEBUG: bool = False

    class Config:
        env_file = "settings.env"
        env_file_encoding = "utf-8"


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()
