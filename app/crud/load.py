from typing import List
from sqlalchemy.orm import Session
from app.models.load import Load
from app.schemas.load import LoadFilter


def filter_loads_from_db(db: Session, filters: LoadFilter) -> List[Load]:
    """
    Dynamically builds and applies filters to the Load table using SQLAlchemy.

    Filtering logic includes:
    - Case-insensitive partial matches for textual fields (e.g., origin,
    destination)
    - Inclusive range filtering for datetime, weight, rate, and miles

    Args:
        db (Session): SQLAlchemy DB session
        filters (LoadFilter): Filtering criteria received from query params

    Returns:
        List[Load]: All loads matching the given filters
    """
    query = db.query(Load)

    # --- Case-insensitive text filters using ILIKE ---
    if filters.origin:
        query = query.filter(Load.origin.ilike(f"%{filters.origin}%"))

    if filters.destination:
        query = query.filter(Load.destination.ilike(f"%{filters.destination}%"))

    if filters.equipment_type:
        query = query.filter(Load.equipment_type.ilike(f"%{filters.equipment_type}%"))

    if filters.commodity_type:
        query = query.filter(Load.commodity_type.ilike(f"%{filters.commodity_type}%"))

    # --- Datetime range filters ---
    if filters.pickup_datetime_from:
        query = query.filter(Load.pickup_datetime >= filters.pickup_datetime_from)

    if filters.pickup_datetime_to:
        query = query.filter(Load.pickup_datetime <= filters.pickup_datetime_to)

    # --- Numeric filters (inclusive ranges) ---
    if filters.min_weight is not None:
        query = query.filter(Load.weight >= filters.min_weight)

    if filters.max_weight is not None:
        query = query.filter(Load.weight <= filters.max_weight)

    if filters.min_rate is not None:
        query = query.filter(Load.loadboard_rate >= filters.min_rate)

    if filters.max_rate is not None:
        query = query.filter(Load.loadboard_rate <= filters.max_rate)

    if filters.min_miles is not None:
        query = query.filter(Load.miles >= filters.min_miles)

    if filters.max_miles is not None:
        query = query.filter(Load.miles <= filters.max_miles)

    return query.all()
