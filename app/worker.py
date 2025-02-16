from celery import Celery
from celery.signals import beat_init, worker_process_init
from celery.schedules import crontab
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table

from app.core.config import get_settings
from app.db import get_cluster
from app.models import Product, ProductScrapeEvent

# Retrieve the application settings
settings = get_settings()

celery_app = Celery(__name__)

celery_app.conf.broker_url = settings.REDIS_URL
celery_app.conf.result_backend = settings.REDIS_URL


def celery_on_startup(*args, **kwargs):
    print("Celery Worker Started!!!")

    if connection.cluster is not None:
        connection.cluster.shutdown()

    if connection.session is not None:
        connection.session.shutdown()

    cluster = get_cluster()
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    sync_table(Product)
    sync_table(ProductScrapeEvent)


beat_init.connect(celery_on_startup)
worker_process_init.connect(celery_on_startup)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, *args, **kwargs):
    # sender.add_periodic_task(1, random_task)
    sender.add_periodic_task(crontab(minute="*/5"), scrape_products.s())


@celery_app.task
def random_task():
    print("The Random Task")


@celery_app.task
def scrape_asin(asin: str):
    print(asin)


@celery_app.task
def scrape_products():
    print("Scraping...")
    q = Product.objects().all().values_list("asin", flat=True)
    for asin in q:
        scrape_asin.delay(asin)
