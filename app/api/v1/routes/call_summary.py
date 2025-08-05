import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database_engine.session import get_db
from app.api.dependencies import APIKeyDep
from app.crud.call_summary import create_call_summary, get_all_call_summaries
from app.schemas.call_summary import CallSummaryCreate, CallSummaryResponse

router = APIRouter(tags=["Call Summary"])

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@router.post(
    "/call-summary",
    response_model=CallSummaryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log a new call summary",
    description=(
        "Log a carrier interaction summarizing the outcome, sentiment, pricing, and any relevant metadata. "
        "This endpoint captures all negotiation details including counter offers, special conditions, and sentiment."
    ),
)
def add_call_summary(
    token: APIKeyDep,
    payload: CallSummaryCreate,
    db: Session = Depends(get_db),
) -> CallSummaryResponse:
    """
    Create a new call summary record.

    Args:
        token (APIKeyDep): Secured API access.
        payload (CallSummaryCreate): Summary data to be logged.
        db (Session): Active database session.

    Returns:
        CallSummaryResponse: Saved record with database-generated ID and timestamp.
    """
    logger.info(f"[CALL SUMMARY - INPUT] Payload received: {payload.dict()}")

    result = create_call_summary(db, payload)

    logger.info(f"[CALL SUMMARY - OUTPUT] Summary stored: {result}")

    return result


@router.get(
    "/call-summary",
    response_model=List[CallSummaryResponse],
    summary="Get all call summaries",
    description=(
        "Retrieve all logged carrier call summaries from the system. "
        "Includes outcome, sentiment, satisfaction, counter offers, and more."
    ),
)
def get_summary(
    token: APIKeyDep,
    db: Session = Depends(get_db),
) -> List[CallSummaryResponse]:
    """
    Retrieve all stored call summaries.

    Args:
        token (APIKeyDep): Secured API access.
        db (Session): Active database session.

    Raises:
        HTTPException: If no records are found.

    Returns:
        List[CallSummaryResponse]: List of all call summary records.
    """
    summaries = get_all_call_summaries(db)
    if not summaries:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No call summaries found",
        )
    return summaries
