from celery import Celery
from backend.config import settings

celery_app = Celery(
    "consumer",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND,              # <-- add backend for stability
    include=["backend.celery_app.tasks"]          # <-- correct tasks path
)

celery_app.conf.update(
    # Serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    # Timezone
    timezone="UTC",
    enable_utc=True,

    # IMPORTANT — prevent double-execution
    task_acks_late=False,   # settings.CELERY_TASK_ACKS_LATE is ignored; force=False
    task_reject_on_worker_lost=False,
    worker_prefetch_multiplier=1,    # BEST for preventing duplicates
    broker_pool_limit=settings.CELERY_BROKER_POOL_LIMIT,
    worker_max_tasks_per_child=settings.CELERY_WORKER_MAX_TASKS_PER_CHILD,

    # Performance tuning
    task_default_queue="celery",
)
