from fastapi import APIRouter
from typing import List

from app.models import Product, ProductScrapeEvent
from app.schema import ProductSchema, ProductScrapeEventDetailSchema

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductSchema])
def get_all_products():
    return list(Product.objects.all())


@router.get("/{asin}")
def find_product_by_asin(asin: str):
    data = dict(Product.objects.get(asin=asin))
    events = list(ProductScrapeEvent.objects().filter(asin=asin))
    events = [ProductScrapeEventDetailSchema(**x) for x in events]
    data["events"] = events
    return data
