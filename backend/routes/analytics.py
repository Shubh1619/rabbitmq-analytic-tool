from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from backend.celery_app.tasks import process_event


router = APIRouter()

class TrackEvent(BaseModel):
    client_id: str
    user_id: str
    event_type: str
    search_type: str
    search_query: str
    business_id: List[str]          # <-- IMPORTANT: ARRAY
    latitude: float
    longitude: float
    timestamp: str                  # ISO string

@router.post("/track-event")
def track_event(event: TrackEvent):
    event_data = event.dict()
    process_event.delay(event_data)
    return {"status": "queued", "event": event_data}
