import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import Union, List
from cassandra.cqlengine.management import sync_table

from app.core.config import get_settings
from app.db import get_session
from app.models import Product, ProductScrapeEvent
from app.schema import ProductSchema, ProductScrapeEventDetailSchema


# Set up logging for better debugging and error messages
logging.basicConfig(level=logging.INFO)

# Retrieve the application settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    session = get_session()
    app.state.session = session
    try:
        logging.info("Starting table synchronization...")
        sync_table(Product)
        sync_table(ProductScrapeEvent)
        logging.info("Table synchronization completed successfully.")
        yield
    finally:
        session.shutdown()
        app.state.session = None
        logging.info("Session connections closed gracefully.")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "description": settings.PROJECT_DESC,
        "author": settings.PROJECT_AUTHOR,
    }


@app.get("/products", response_model=List[ProductSchema])
def get_all_products():
    return list(Product.objects.all())


@app.get("/products/{asin}")
def find_product_by_asin(asin: str):
    data = dict(Product.objects.get(asin=asin))
    events = list(ProductScrapeEvent.objects().filter(asin=asin))
    events = [ProductScrapeEventDetailSchema(**x) for x in events]
    data["events"] = events
    return data
