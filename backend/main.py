from fastapi import FastAPI
from backend.routes.analytics import router as analytics_router
from backend.db.database import init_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()  # Creates tables

app.include_router(analytics_router, prefix="/analytics")
