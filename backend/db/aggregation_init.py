import clickhouse_connect
import os

client = clickhouse_connect.get_client(
    host=os.getenv("CLICKHOUSE_HOST", "clickhouse"),
    port=int(os.getenv("CLICKHOUSE_PORT", 8123)),
    username=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", "")
)

def init_aggregation():
    print("🚀 Initializing ClickHouse MATERIALIZED VIEWS (Real-Time Aggregation)...")

    queries = [

        # --------------------------------------------------
        # MV 1: Daily total events
        # --------------------------------------------------
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

        # --------------------------------------------------
        # MV 2: Business-level summary (FIXED — NO arrayJoin)
        # --------------------------------------------------
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_business_summary
        TO analytics_business_summary
        AS
        SELECT
            toDate(timestamp) AS date,
            business_id,   -- now String, no arrayJoin
            countIf(event_type = 'click') AS total_clicks,
            countIf(event_type = 'view') AS total_views,
            countIf(event_type = 'call') AS total_calls
        FROM analytics_events
        GROUP BY date, business_id;
        """,

        # --------------------------------------------------
        # MV 3: Keyword-level summary
        # --------------------------------------------------
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

    for q in queries:
        try:
            client.command(q)
            print("✅ Executed MV:", q.split("\n")[1].strip())
        except Exception as e:
            print("⚠️ MV exists / Error:", e)

    print("🎉 Materialized Views initialization complete.")


if __name__ == "__main__":
    init_aggregation()
