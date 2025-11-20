from celery import Celery
from backend.config import settings

celery_app = Celery(
    "analytics_tasks",
    broker=settings.CELERY_BROKER_URL,   # ✅ FIXED
    backend=settings.CELERY_BACKEND,     # ✅ SAME
    include=["backend.celery_app.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
