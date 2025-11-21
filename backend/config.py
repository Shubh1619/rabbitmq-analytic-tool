from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # -------------------------
    # RabbitMQ (from .env)
    # -------------------------
    RABBIT_HOST: str = os.getenv("RABBIT_HOST")
    RABBIT_USER: str = os.getenv("RABBIT_USER")
    RABBIT_PASS: str = os.getenv("RABBIT_PASS")

    # -------------------------
    # Celery (from .env)
    # -------------------------
    CELERY_BROKER_URL: str | None = os.getenv("CELERY_BROKER_URL")
    CELERY_BACKEND: str = os.getenv("CELERY_BACKEND")

    # -------------------------
    # ClickHouse (from .env)
    # -------------------------
    CLICKHOUSE_HOST: str = os.getenv("CLICKHOUSE_HOST")
    CLICKHOUSE_PORT: int = int(os.getenv("CLICKHOUSE_PORT"))
    CLICKHOUSE_USER: str = os.getenv("CLICKHOUSE_USER")
    CLICKHOUSE_PASSWORD: str = os.getenv("CLICKHOUSE_PASSWORD")
    CLICKHOUSE_DATABASE: str = os.getenv("CLICKHOUSE_DB")
    CLICKHOUSE_SECURE: bool = os.getenv("CLICKHOUSE_SECURE").lower() == "true"

    # -------------------------
    # FastAPI ENV
    # -------------------------
    APP_ENV: str = os.getenv("APP_ENV")

    # -------------------------
    # Batching
    # -------------------------
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE"))
    FLUSH_INTERVAL: float = float(os.getenv("FLUSH_INTERVAL"))

    # -------------------------
    # Celery Worker Tuning
    # -------------------------
    CELERY_WORKER_PREFETCH_MULTIPLIER: int = int(os.getenv("CELERY_WORKER_PREFETCH_MULTIPLIER"))
    CELERY_TASK_ACKS_LATE: bool = os.getenv("CELERY_TASK_ACKS_LATE").lower() == "true"
    CELERY_TASK_REJECT_ON_WORKER_LOST: bool = os.getenv("CELERY_TASK_REJECT_ON_WORKER_LOST").lower() == "true"
    CELERY_BROKER_POOL_LIMIT: int = int(os.getenv("CELERY_BROKER_POOL_LIMIT"))
    CELERY_WORKER_MAX_TASKS_PER_CHILD: int = int(os.getenv("CELERY_WORKER_MAX_TASKS_PER_CHILD"))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )


settings = Settings()

# Build broker if not provided
if not settings.CELERY_BROKER_URL:
    settings.CELERY_BROKER_URL = (
        f"amqp://{settings.RABBIT_USER}:{settings.RABBIT_PASS}"
        f"@{settings.RABBIT_HOST}:5672/"
    )
