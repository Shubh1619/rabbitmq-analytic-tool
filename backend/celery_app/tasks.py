from backend.celery_app.celery import celery_app
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL connection
pg_conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("POSTGRES_PORT")
)
pg_cur = pg_conn.cursor()

@celery_app.task
def process_event(event: dict):

    pg_cur.execute("""
        INSERT INTO analytics_events 
        (client_id, user_id, event_type, search_type, search_query,
         business_id, latitude, longitude, timestamp)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        event.get("client_id"),
        event.get("user_id"),
        event.get("event_type"),
        event.get("search_type"),
        event.get("search_query"),
        event.get("business_id"),
        event.get("latitude"),
        event.get("longitude"),
        event.get("timestamp")
    ))

    pg_conn.commit()
