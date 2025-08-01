from sqlalchemy.orm import Session
from app.models.call_summary import CallSummary
from app.schemas.call_summary import CallSummaryCreate


def create_call_summary(db: Session, summary_data: CallSummaryCreate) -> CallSummary:
    summary = CallSummary(**summary_data.dict())
    db.add(summary)
    db.commit()
    db.refresh(summary)
    return summary


def get_call_summary_by_load_id(db: Session, load_id: str) -> CallSummary | None:
    return db.query(CallSummary).filter(CallSummary.load_id == load_id).first()
