import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import Union
from cassandra.cqlengine.management import sync_table

from app.models import Product, ProductScrapeEvent
from app.db import get_session


# Set up logging for better debugging and error messages
logging.basicConfig(level=logging.INFO)


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
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
