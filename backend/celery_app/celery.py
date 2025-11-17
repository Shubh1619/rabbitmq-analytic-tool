from celery import Celery
from backend.config import settings

celery_app = Celery(
    "analytics_tasks",
    broker=settings.RABBIT_URL,
    backend=settings.CELERY_BACKEND,
    include=["backend.celery_app.tasks"]
)
