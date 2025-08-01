from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database_engine.session import get_db
from app.api.dependencies import APIKeyDep
from app.crud.call_summary import create_call_summary, get_call_summary_by_load_id
from app.schemas.call_summary import CallSummaryCreate, CallSummaryResponse

router = APIRouter()


@router.post(
    "/call-summary",
    response_model=CallSummaryResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["CallSummary"],
)
def add_call_summary(
    token: APIKeyDep, payload: CallSummaryCreate, db: Session = Depends(get_db)
):
    return create_call_summary(db, payload)


@router.get(
    "/call-summary/{load_id}", response_model=CallSummaryResponse, tags=["CallSummary"]
)
def get_summary_by_load_id(
    token: APIKeyDep, load_id: str, db: Session = Depends(get_db)
):
    summary = get_call_summary_by_load_id(db, load_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Call summary not found")
    return summary
