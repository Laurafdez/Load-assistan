from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.models.load import Load


def get_all_loads(
    db: Session,
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    equipment_type: Optional[str] = None,
    pickup_datetime: Optional[datetime] = None,
):
    query = db.query(Load)

    if origin:
        query = query.filter(Load.origin.ilike(f"%{origin}%"))

    if destination:
        query = query.filter(Load.destination.ilike(f"%{destination}%"))

    if equipment_type:
        query = query.filter(Load.equipment_type == equipment_type)

    if pickup_datetime:
        query = query.filter(Load.pickup_datetime >= pickup_datetime)

    return query.all()
