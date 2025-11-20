import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # -----------------------------
    # RabbitMQ / Celery
    # -----------------------------
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_BACKEND = os.getenv("CELERY_BACKEND")

    # -----------------------------
    # ClickHouse
    # -----------------------------
    CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
    CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT"))
    CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER")
    CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
    CLICKHOUSE_DB=os.getenv("CLICKHOUSE_DB")
    CLICKHOUSE_SECURE=os.getenv("CLICKHOUSE_SECURE")
    


settings = Settings()
