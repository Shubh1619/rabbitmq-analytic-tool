import clickhouse_connect
from backend.config import settings

client = clickhouse_connect.get_client(
    host=settings.CLICKHOUSE_HOST,
    port=settings.CLICKHOUSE_PORT,
    username=settings.CLICKHOUSE_USER,
    password=settings.CLICKHOUSE_PASSWORD,
    secure=True,                     # ⭐ REQUIRED FOR CLOUD
    verify=False                     # Disable SSL cert verify (optional)
)

def init_db():
    print("🚀 Initializing ClickHouse TABLES (NO aggregation)...")

    queries = [
        """
        CREATE TABLE IF NOT EXISTS analytics_events (
            id UUID DEFAULT generateUUIDv4(),
            client_id String,
            user_id String,
            event_type String,
            search_type String,
            search_query String,
            business_id Array(String),
            latitude Float64,
            longitude Float64,
            timestamp DateTime DEFAULT now()
        )
        ENGINE = MergeTree()
        ORDER BY timestamp;
        """,

        """
        CREATE TABLE IF NOT EXISTS analytics_events_daily (
            date Date,
            total_events UInt64
        )
        ENGINE = SummingMergeTree()
        ORDER BY date;
        """,

        """
        CREATE TABLE IF NOT EXISTS analytics_business_summary (
            date Date,
            business_id String,
            total_clicks UInt64,
            total_views UInt64,
            total_calls UInt64
        )
        ENGINE = SummingMergeTree()
        ORDER BY (date, business_id);
        """,

        """
        CREATE TABLE IF NOT EXISTS analytics_top_keywords (
            date Date,
            keyword String,
            total_searches UInt64
        )
        ENGINE = SummingMergeTree()
        ORDER BY (date, keyword);
        """
    ]

    for q in queries:
        try:
            client.command(q)
            print("✅ Executed Table:", q.split("\n")[1].strip())
        except Exception as e:
            print("⚠️ ClickHouse Error:", e)

    print("🎉 Table initialization complete (NO aggregation).")


if __name__ == "__main__":
    init_db()
