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
    # 1) BASE TABLES (these MUST exist before MVs)
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

        # Business Summary Table (business_id is String for arrayJoin)
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
    # 2) MATERIALIZED VIEWS (use arrayJoin for business_id)
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

        # MV 3 — Top Keywords Summary (typo fixed)
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
