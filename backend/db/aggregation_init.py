import clickhouse_connect
import os

client = clickhouse_connect.get_client(
    host=os.getenv("CLICKHOUSE_HOST"),
    port=int(os.getenv("CLICKHOUSE_PORT")),
    username=os.getenv("CLICKHOUSE_USER"),
    password=os.getenv("CLICKHOUSE_PASSWORD")
)

def init_aggregation():
    print("🚀 Initializing ClickHouse AGGREGATION TABLES + MATERIALIZED VIEWS...")

    # ---------------------------------------------------------------------
    # 0) RAW EVENTS TABLE (MUST be created first)
    # ---------------------------------------------------------------------
    analytics_events_table = """
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
        ORDER BY (timestamp);
    """

    try:
        client.command(analytics_events_table)
        print("✅ Created base table: analytics_events")
    except Exception as e:
        print("⚠️ Error creating analytics_events:", e)

    # ---------------------------------------------------------------------
    # 1) AGGREGATION TABLES
    # ---------------------------------------------------------------------
    base_tables = [

        # Daily Events Table
        """
        CREATE TABLE IF NOT EXISTS analytics_events_daily (
            date Date,
            total_events UInt64
        )
        ENGINE = SummingMergeTree()
        ORDER BY date;
        """,

        # Business Summary Table 
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

        # Top Keywords Table
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

    for q in base_tables:
        try:
            client.command(q)
            print("✅ Created table:", q.split("\n")[1].strip())
        except Exception as e:
            print("⚠️ Table exists / Error:", e)

    # ---------------------------------------------------------------------
    # 2) MATERIALIZED VIEWS
    # ---------------------------------------------------------------------
    mvs = [

        # MV 1 — Daily Events Summary
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_events_daily
        TO analytics_events_daily
        AS
        SELECT
            toDate(timestamp) AS date,
            count() AS total_events
        FROM analytics_events
        GROUP BY date;
        """,

        # MV 2 — Business Summary with arrayJoin
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_business_summary
        TO analytics_business_summary
        AS
        SELECT
            toDate(timestamp) AS date,
            arrayJoin(business_id) AS business_id,
            countIf(event_type = 'click') AS total_clicks,
            countIf(event_type = 'view') AS total_views,
            countIf(event_type = 'call') AS total_calls
        FROM analytics_events
        GROUP BY date, business_id;
        """,

        # MV 3 — Top Keywords Summary
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_top_keywords
        TO analytics_top_keywords
        AS
        SELECT
            toDate(timestamp) AS date,
            search_query AS keyword,
            count() AS total_searches
        FROM analytics_events
        WHERE search_query != '' AND search_query != 'not_found'
        GROUP BY date, keyword;
        """
    ]

    for q in mvs:
        try:
            client.command(q)
            print("✅ Created MV:", q.split("\n")[1].strip())
        except Exception as e:
            print("⚠️ MV exists / Error:", e)

    print("🎉 Aggregation system initialized successfully!")

if __name__ == "__main__":
    init_aggregation()
