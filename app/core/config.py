from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Fast Scrapper"
    PROJECT_DESC: str = (
        "A high-performance web scraping API for extracting data from e-commerce sites."
    )
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_AUTHOR: str = "codebyaadi"

    ASTRA_DB_CLIENT_ID: str
    ASTRA_DB_SECRET: str
    ASTRA_DB_TOKEN: str
    ASTRA_DB_BUNDLE_PATH: str
    ASTRA_DB_API_ENDPOINT: str

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
