from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Fast Scrapper"
    ASTRA_DB_CLIENT_ID: str
    ASTRA_DB_SECRET: str
    ASTRA_DB_TOKEN: str
    ASTRA_DB_BUNDLE_PATH: str

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
