from celery import Celery

from app.core.config import get_settings

# Retrieve the application settings
settings = get_settings()

celery_app = Celery(__name__)

celery_app.conf.broker_url = settings.REDIS_URL
celery_app.conf.result_backend = settings.REDIS_URL

@celery_app.task
def random_task():
    print("The Random Task")