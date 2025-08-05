from fastapi import APIRouter, Depends
from app.business.healthcheck import HealthcheckManager

router = APIRouter()


@router.get(
    "/",
    tags=["Healthcheck"],
    summary="Check API health status",
    description="Returns the current health status of the API. Useful for monitoring and uptime checks.",
    response_model=dict,
)
def health(manager: HealthcheckManager = Depends()) -> dict:
    """
    Healthcheck endpoint.

    Returns the system's current health status as determined by the HealthcheckManager.

    Args:
        manager (HealthcheckManager): Dependency that encapsulates health check logic.

    Returns:
        dict: Dictionary containing health status details.
    """
    return manager.status()
