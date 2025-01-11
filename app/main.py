import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from cassandra.cqlengine.management import sync_table

from app.core.config import get_settings
from app.db import get_session
from app.models import Product, ProductScrapeEvent
from app.routers import product


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


app.include_router(product.router)
