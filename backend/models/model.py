from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func
from backend.db.database import Base


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(String(100), nullable=True)
    user_id = Column(String(100), nullable=True)

    event_type = Column(String(50), nullable=False)

    search_type = Column(String(100), nullable=True)
    search_query = Column(Text, nullable=True)

    business_id = Column(String(100), nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # user-provided timestamp
    timestamp = Column(DateTime(timezone=True), nullable=True)

    # server-generated timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
