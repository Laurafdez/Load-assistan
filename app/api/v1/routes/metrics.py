from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database_engine.session import get_db
from app.schemas.metrics import MetricsResponse
from app.business.metrics import calculate_metrics

router = APIRouter(tags=["Metrics"])


@router.get(
    "/metrics",
    response_model=MetricsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get system metrics",
    description=(
        "Returns detailed KPI metrics about load availability, call summaries, "
        "negotiation outcomes, sentiment trends, and user satisfaction."
    ),
    response_description="Metrics data successfully retrieved.",
)
def get_metrics(db: Session = Depends(get_db)) -> MetricsResponse:
    """
    Retrieve key performance indicators and analytics on calls and loads.

    This includes:
    - Total loads
    - Total and categorized call outcomes
    - Average prices, attempts, durations
    - Sentiment and satisfaction breakdowns
    """
    return calculate_metrics(db)
