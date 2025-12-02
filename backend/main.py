from fastapi import FastAPI
from backend.routes.analytics import router as analytics_router
from backend.db.database import init_db
from pathlib import Path


app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()


app.include_router(analytics_router, prefix="/analytics")
