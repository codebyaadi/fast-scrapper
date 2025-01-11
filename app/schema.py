from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, model_validator
from typing import Optional

from app.utils.time import uuid1_time_to_datetime


class ProductSchema(BaseModel):
    """
    Schema for representing a product.

    Attributes:
        asin (str): The Amazon Standard Identification Number (ASIN) of the product.
        title (Optional[str]): The title of the product. This field is optional.
    """

    asin: str
    title: Optional[str]


class ProductScrapeEventSchema(BaseModel):
    """
    Schema for representing a product scrape event.

    Attributes:
        uuid (UUID): A unique identifier for the scraping event.
        asin (str): The Amazon Standard Identification Number (ASIN) of the product associated with the scrape event.
        title (Optional[str]): The title of the product at the time of scraping. This field is optional.
    """

    uuid: UUID
    asin: str
    title: Optional[str]


class ProductScrapeEventDetailSchema(BaseModel):
    """
    Schema for product scrape event details.

    Attributes:
        asin (str): The Amazon Standard Identification Number of the product.
        title (Optional[str]): The title of the product.
        price_str (Optional[str]): The price of the product as a string.
        created_at (Optional[datetime]): The timestamp when the event was created, extracted from the UUID.

    Methods:
        extract_time_from_uuid(cls, values):
            Extracts the creation time from the UUID and sets it to the created_at attribute.
    """

    asin: str
    title: Optional[str]
    price_str: Optional[str]
    created_at: Optional[datetime] = None

    @model_validator(mode="before")
    def extract_time_from_uuid(cls, values):
        values["created_at"] = uuid1_time_to_datetime(values["uuid"].time)
        return values
