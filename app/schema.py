from uuid import UUID
from pydantic import BaseModel
from typing import Optional


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
