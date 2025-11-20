from backend.celery_app.celery import celery_app
import clickhouse_connect
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# ClickHouse connection
client = clickhouse_connect.get_client(
    host=os.getenv("CLICKHOUSE_HOST", "clickhouse"),
    port=int(os.getenv("CLICKHOUSE_PORT", 8123)),
    username=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", "")
)

# Create table if not exists
client.command("""
CREATE TABLE IF NOT EXISTS analytics_events (
    client_id String,
    user_id String,
    event_type String,
    search_type String,
    search_query String,
    business_id String,
    latitude Float64,
    longitude Float64,
    timestamp DateTime
) ENGINE = MergeTree()
ORDER BY timestamp
""")

@celery_app.task
def process_event(event: dict):

    # ----------------------------------------
    # ✅ Fix: Always convert business_id to String
    # ----------------------------------------
    business_id = event.get("business_id")

    if isinstance(business_id, list):
        # Convert list → comma-separated string
        business_id = ",".join([str(x) for x in business_id])
    elif business_id in [None, "", [], {}, "not_found"]:
        business_id = "not_found"
    else:
        business_id = str(business_id)

    # ----------------------------------------
    # ✅ Fix: Convert timestamp string → datetime
    # ----------------------------------------
    raw_ts = event.get("timestamp")

    if not raw_ts or raw_ts == "string":
        timestamp = datetime.utcnow()
    else:
        try:
            timestamp = datetime.fromisoformat(raw_ts.replace("Z", "+00:00"))
        except:
            timestamp = datetime.utcnow()

    # ----------------------------------------
    # Insert into ClickHouse
    # ----------------------------------------
    client.insert(
        "analytics_events",
        [[
            event.get("client_id", ""),
            event.get("user_id", ""),
            event.get("event_type", ""),
            event.get("search_type", ""),
            event.get("search_query", ""),
            business_id,                      # <--- FIXED
            float(event.get("latitude", 0)),
            float(event.get("longitude", 0)),
            timestamp
        ]],
        column_names=[
            "client_id", "user_id", "event_type", "search_type",
            "search_query", "business_id", "latitude", "longitude", "timestamp"
        ]
    )

    return {"status": "stored_in_clickhouse"}
