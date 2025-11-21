import threading
import time
from datetime import datetime, timezone
from celery.utils.log import get_task_logger

from backend.celery_app.celery import celery_app    # FIXED
from backend.config import settings                 # FIXED (requires pydantic-settings fix)
from backend.db.database import get_clickhouse_client

logger = get_task_logger(__name__)

_lock = threading.Lock()
_buffer = []
_thread_started = False
_client = None


def _get_client():
    global _client
    if _client is None:
        _client = get_clickhouse_client()
    return _client


def _flush_buffer():
    global _buffer
    with _lock:
        if not _buffer:
            return
        rows = _buffer
        _buffer = []

    try:
        client = _get_client()
        client.insert(
            "analytics_events",
            rows,
            column_names=[
                "client_id", "user_id", "event_type", "search_type",
                "search_query", "business_id", "latitude", "longitude", "timestamp"
            ]
        )
        logger.info("Flushed %d rows to ClickHouse", len(rows))
    except Exception as e:
        logger.exception("ClickHouse batch insert failed: %s", e)
        try:
            client.insert(
                "analytics_events",
                rows,
                column_names=[
                    "client_id", "user_id", "event_type", "search_type",
                    "search_query", "business_id", "latitude", "longitude", "timestamp"
                ]
            )
            logger.info("Retry insert succeeded for %d rows", len(rows))
        except Exception:
            logger.exception("Retry insert failed; dropping batch")


def _flusher_loop():
    while True:
        time.sleep(settings.FLUSH_INTERVAL)
        try:
            _flush_buffer()
        except Exception:
            logger.exception("Error in flusher loop")


def _ensure_flusher():
    global _thread_started
    if not _thread_started:
        t = threading.Thread(target=_flusher_loop, daemon=True)
        t.start()
        _thread_started = True


@celery_app.task(bind=True, acks_late=settings.CELERY_TASK_ACKS_LATE)
def process_event(self, event: dict):
    _ensure_flusher()

    try:
        business_id = event.get("business_id")
        
        # Case 1 → already list
        if isinstance(business_id, list):
            business_id = [str(x) for x in business_id]
        
        # Case 2 → string
        elif isinstance(business_id, str) and business_id.strip() != "":
            business_id = [business_id]
        
        # Case 3 → empty or None
        else:
            business_id = ["not_found"]

        raw_ts = event.get("timestamp")
        try:
            timestamp = datetime.fromisoformat(raw_ts.replace("Z", "+00:00"))
        except:
            timestamp = datetime.now(timezone.utc)

        row = [
            event.get("client_id", ""),
            event.get("user_id", ""),
            event.get("event_type", ""),
            event.get("search_type", ""),
            event.get("search_query", ""),
            business_id,
            float(event.get("latitude", 0.0)),
            float(event.get("longitude", 0.0)),
            timestamp
        ]

        with _lock:
            _buffer.append(row)
            if len(_buffer) >= settings.BATCH_SIZE:
                _flush_buffer()

        return {"status": "queued_local_buffer"}

    except Exception as e:
        logger.exception("Error in process_event: %s", e)
        raise
