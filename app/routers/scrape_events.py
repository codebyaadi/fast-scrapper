from fastapi import APIRouter
from typing import List

from app import crud
from app.models import ProductScrapeEvent
from app.schema import ProductListSchema, ProductScrapeEventDetailSchema

router = APIRouter(prefix="/scrape-events", tags=["scrape-events"])


@router.post("/scrape")
def create_scrape_event(data: ProductListSchema):
    product, _ = crud.add_scrape_event(data.model_dump())
    return product


@router.get("/{asin}/list", response_model=List[ProductScrapeEventDetailSchema])
def list_all_events(asin: str):
    events = list(ProductScrapeEvent.objects().filter(asin=asin))
    events = [ProductScrapeEventDetailSchema(**x) for x in events]
    return events
