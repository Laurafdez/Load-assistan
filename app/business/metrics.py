from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.call_summary import CallSummary
from app.models.load import Load
from app.schemas.metrics import (
    MetricsResponse,
    SentimentSummary,
    SatisfactionStats,
)


def calculate_metrics(db: Session) -> MetricsResponse:
    """
    Calculate operational metrics from the database.

    This function aggregates key statistics from the `Load` and `CallSummary`
    tables to generate insights into system usage and carrier negotiations.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        MetricsResponse: A structured object containing computed metrics such as:
            - total loads and calls
            - call outcomes (accepted, rejected, etc.)
            - average agreed price
            - average call duration
            - average number of attempts and counter-offers
            - sentiment breakdown
            - satisfaction statistics
    """

    # Aggregate general counts
    total_loads = db.query(Load).count()
    total_calls = db.query(CallSummary).count()

    # Count different negotiation outcomes
    accepted = db.query(CallSummary).filter(CallSummary.outcome == "accepted").count()
    rejected = db.query(CallSummary).filter(CallSummary.outcome == "rejected").count()
    failed_negotiation = (
        db.query(CallSummary)
        .filter(CallSummary.outcome == "failed_negotiation")
        .count()
    )
    no_response = (
        db.query(CallSummary).filter(CallSummary.outcome == "no_response").count()
    )
    follow_ups = (
        db.query(CallSummary)
        .filter(CallSummary.outcome == "interested_follow_up")
        .count()
    )

    # Compute average agreed price
    prices = (
        db.query(CallSummary.agreed_price)
        .filter(CallSummary.agreed_price.isnot(None))
        .all()
    )
    avg_price = round(sum(p[0] for p in prices) / len(prices), 2) if prices else 0

    # Compute averages
    avg_duration = db.query(func.avg(CallSummary.call_duration_sec)).scalar() or 0
    avg_attempts = db.query(func.avg(CallSummary.attempts)).scalar() or 0
    avg_counter_offers = db.query(func.avg(CallSummary.counter_offers)).scalar() or 0

    # Satisfaction counts
    satisfied = db.query(CallSummary).filter(CallSummary.satisfaction.is_(True)).count()
    unsatisfied = (
        db.query(CallSummary).filter(CallSummary.satisfaction.is_(False)).count()
    )
    unknown_satisfaction = total_calls - satisfied - unsatisfied

    # Sentiment breakdown
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

    # Construct and return full metrics response
    return MetricsResponse(
        total_loads=total_loads,
        total_calls=total_calls,
        accepted=accepted,
        rejected=rejected,
        failed_negotiation=failed_negotiation,
        no_response=no_response,
        interested_follow_up=follow_ups,
        avg_agreed_price=avg_price,
        avg_call_duration_sec=round(avg_duration, 2),
        avg_attempts=round(avg_attempts, 2),
        avg_counter_offers=round(avg_counter_offers, 2),
        sentiment_summary=sentiment_summary,
        satisfaction_summary=SatisfactionStats(
            satisfied=satisfied,
            unsatisfied=unsatisfied,
            unknown=unknown_satisfaction,
        ),
    )
