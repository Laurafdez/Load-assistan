from fastapi import APIRouter
from app.api.v1.routes import (
    call_summary,
    carrier,
    healthcheck,
    load,
    metrics,
    negotations,
)

# Create the main API router for version v1
api_router = APIRouter()

# Public routes (do not require API key authentication)
api_router.include_router(healthcheck.router, prefix="/health", tags=["Healthcheck"])

# Secured routes (API key required via middleware or route-level dependency)
api_router.include_router(load.router, prefix="", tags=["Loads"])

api_router.include_router(call_summary.router, prefix="", tags=["Call Summary"])

api_router.include_router(metrics.router, prefix="", tags=["Metrics"])

api_router.include_router(carrier.router, prefix="", tags=["Carriers"])

api_router.include_router(negotations.router, prefix="", tags=["Negotiations"])
