from fastapi import APIRouter
from pydantic import BaseModel
from backend.celery_app.tasks import process_event

router = APIRouter()

class TrackEvent(BaseModel):
    client_id: str
    user_id: str
    event_type: str
    search_type: str | None = None
    search_query: str | None = None
    business_id: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    timestamp: str | None = None


@router.post("/track-event")
def track_event(event: TrackEvent):
    event_data = event.dict()
    process_event.delay(event_data)  # Send to Celery worker
    return {"status": "queued", "event": event_data}
