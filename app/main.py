from fastapi import FastAPI
from app.api.v1.routes import call_summary, health, load, metrics

app = FastAPI(title="Load Assistant API", version="1.0.0")

# Public route (sin API key)
app.include_router(health.router, prefix="/health", tags=["Healthcheck"])

# Secure route (con API key requerida)
app.include_router(load.router, prefix="", tags=["Loads"])
app.include_router(call_summary.router, prefix="", tags=["CallSummary"])
app.include_router(metrics.router, prefix="", tags=["Metrics"])
