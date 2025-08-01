from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.database_engine.session import get_db
from app.crud.load import get_all_loads
from app.schemas.load import LoadBase
from app.api.dependencies import APIKeyDep

router = APIRouter()


@router.get("/loads", response_model=list[LoadBase], tags=["Loads"])
def read_loads(
    token: APIKeyDep,
    db: Session = Depends(get_db),
    origin: Optional[str] = Query(None),
    destination: Optional[str] = Query(None),
    equipment_type: Optional[str] = Query(None),
    pickup_datetime: Optional[datetime] = Query(None),
):
    return get_all_loads(
        db,
        origin=origin,
        destination=destination,
        equipment_type=equipment_type,
        pickup_datetime=pickup_datetime,
    )
