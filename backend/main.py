from fastapi import FastAPI,Response
from backend.routes.analytics import router as analytics_router
from backend.db.database import init_db
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles


app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)

app.include_router(analytics_router, prefix="/analytics")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

@app.get("/dashboard", response_class=HTMLResponse)
def open_dashboard():
    html_path = Path("/app/frontend/dashboard.html")

    if not html_path.exists():
        return HTMLResponse(
            f"<h1>dashboard.html NOT found at {html_path}</h1>",
            status_code=404
        )

    return HTMLResponse(html_path.read_text())
