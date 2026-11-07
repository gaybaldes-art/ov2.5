from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .engine import forecast

app = FastAPI(title="MATCHLAB API", version="0.1.0")


class ForecastRequest(BaseModel):
    home_xg: float = Field(ge=0, le=8, description="Expected goals for the home team")
    away_xg: float = Field(ge=0, le=8, description="Expected goals for the away team")
    max_goals: int = Field(default=10, ge=3, le=20)


@app.get("/health")
def health():
    return {"status": "ok", "service": "matchlab-api"}


@app.post("/api/v1/forecast")
def create_forecast(request: ForecastRequest):
    try:
        return forecast(request.home_xg, request.away_xg, request.max_goals)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/v1/analyst")
def analyst_unconfigured():
    raise HTTPException(
        status_code=503,
        detail="Analyst AI non ancora configurato. La chiave del provider deve essere impostata esclusivamente sul server.",
    )
