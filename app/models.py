from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

KEY_SPACE = "default_keyspace"

data = {"asin": "123", "title": "Marx Ladaf"}


class Product(Model):
    """
    Represents a product entity in the Cassandra Database

    Attributes:
        asin (columns.Text): The Amazon Standard Identification Number (ASIN) of the product, used as the primary key.
        title (columns.Text): The title of the product.
        price_str (columns.Text): The price of the product represented as a string. Defaults to "-100" if not provided.
    """

    __keyspace__ = KEY_SPACE
    asin = columns.Text(primary_key=True, required=True)
    title = columns.Text()
    price_str = columns.Text(default="-100")


class ProductScrapeEvent(Model):
    """
    Represents an event related to scraping product information.

    Attributes:
        uuid (columns.UUID): A unique identifier for the scraping event, used as the primary key.
        asin (columns.Text): The ASIN of the product associated with the scraping event. Indexed for faster lookups.
        title (columns.Text): The title of the product at the time of scraping.
        price_str (columns.Text): The price of the product as a string at the time of scraping. Defaults to "-100" if not provided.
    """

    __keyspace__ = KEY_SPACE
    uuid = columns.UUID(primary_key=True)
    asin = columns.Text(index=True)
    title = columns.Text()
    price_str = columns.Text(default="-100")
