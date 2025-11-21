# /mnt/data/database.py
import clickhouse_connect
from backend.config import settings

def get_clickhouse_client():
    """
    Returns a shared clickhouse client instance configured for bulk inserts.
    Use this function from all modules instead of creating ad-hoc clients.
    """
    client = clickhouse_connect.get_client(
        host=settings.CLICKHOUSE_HOST,
        port=settings.CLICKHOUSE_PORT,
        username=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASSWORD,
        secure=settings.CLICKHOUSE_SECURE,
        database=settings.CLICKHOUSE_DATABASE,
        connect_timeout=5,
        send_receive_timeout=30,
        compress=False,
        settings={"async_insert": 1, "wait_for_async_insert": 1},
    )
    return client


def init_db():
    """
    Initialize analytics_events table with Array(String) for business_id.
    """
    client = get_clickhouse_client()

    create = """
    CREATE TABLE IF NOT EXISTS analytics_events (
        client_id String,
        user_id String,
        event_type String,
        search_type String,
        search_query String,
        business_id Array(String), 
        latitude Float64,
        longitude Float64,
        timestamp DateTime
    ) ENGINE = MergeTree()
    ORDER BY (timestamp)
    """
    client.command(create)
