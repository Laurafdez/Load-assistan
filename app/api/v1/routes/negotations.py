import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database_engine.session import get_db
from app.schemas.negotiations import CounterOfferRequest, CounterOfferResponse
from app.business.negotiation import evaluate_counter_offer

router = APIRouter(tags=["Negotiations"])

logger = logging.getLogger(__name__)


@router.post("/counteroffer", response_model=CounterOfferResponse)
def counteroffer_endpoint(
    req: CounterOfferRequest,
    db: Session = Depends(get_db),
):
    """
    Process a carrier's counteroffer and return an appropriate business response.

    Delegates to negotiation logic for decision-making based on rules.
    """
    logger.info(f"[NEGOTIATION - INPUT] Counteroffer request received: {req}")

    response = evaluate_counter_offer(req)

    logger.info(f"[NEGOTIATION - OUTPUT] Evaluation result: {response}")

    return response
