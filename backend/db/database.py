import clickhouse_connect
import os

client = clickhouse_connect.get_client(
    host=os.getenv("CLICKHOUSE_HOST", "clickhouse"),
    port=int(os.getenv("CLICKHOUSE_PORT", 8123)),
    username=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", "")
)

def init_db():
    client.command("""
        CREATE TABLE IF NOT EXISTS analytics_events (
            id UUID DEFAULT generateUUIDv4(),
            user_id String,
            event_type String,
            search_query String,
            business_id Array(String),
            latitude Float64,
            longitude Float64,
            timestamp DateTime DEFAULT now()
        )
        ENGINE = MergeTree()
        ORDER BY timestamp
    """)
