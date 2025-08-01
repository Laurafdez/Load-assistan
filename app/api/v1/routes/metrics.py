from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database_engine.session import get_db
from app.models.call_summary import CallSummary
from app.models.load import Load
from app.schemas.metrics import MetricsResponse, SentimentSummary

router = APIRouter()


@router.get("/metrics", response_model=MetricsResponse, tags=["Metrics"])
def get_metrics(db: Session = Depends(get_db)):
    total_loads = db.query(Load).count()
    total_calls = db.query(CallSummary).count()
    accepted = db.query(CallSummary).filter(CallSummary.outcome == "accepted").count()
    rejected = db.query(CallSummary).filter(CallSummary.outcome == "rejected").count()
    pending = total_calls - accepted - rejected

    prices = (
        db.query(CallSummary.agreed_price).filter(CallSummary.agreed_price > 0).all()
    )
    avg_price = round(sum(p[0] for p in prices) / len(prices), 2) if prices else 0

    sentiment_summary = SentimentSummary(
        positive=db.query(CallSummary)
        .filter(CallSummary.sentiment == "positive")
        .count(),
        neutral=db.query(CallSummary)
        .filter(CallSummary.sentiment == "neutral")
        .count(),
        negative=db.query(CallSummary)
        .filter(CallSummary.sentiment == "negative")
        .count(),
    )

    return MetricsResponse(
        total_loads=total_loads,
        total_calls=total_calls,
        accepted=accepted,
        rejected=rejected,
        pending=pending,
        avg_agreed_price=avg_price,
        sentiment_summary=sentiment_summary,
    )
