from typing import List
from sqlalchemy.orm import Session
from app.models.call_summary import CallSummary
from app.schemas.call_summary import CallSummaryCreate


def create_call_summary(db: Session, summary_data: CallSummaryCreate) -> CallSummary:
    """
    Create and persist a new CallSummary record in the database.

    Args:
        db (Session): SQLAlchemy database session.
        summary_data (CallSummaryCreate): Pydantic schema containing summary input data.

    Returns:
        CallSummary: The created and persisted call summary object.
    """
    summary = CallSummary(**summary_data.dict())
    db.add(summary)
    db.commit()
    db.refresh(summary)
    return summary


def get_all_call_summaries(db: Session) -> List[CallSummary]:
    """
    Retrieve all CallSummary records from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        List[CallSummary]: A list of all stored call summary objects.
    """
    return db.query(CallSummary).all()
