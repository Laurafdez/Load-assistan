from fastapi import APIRouter, Depends, Request, status, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Union
import logging

from app.api.dependencies import APIKeyDep
from app.database_engine.session import get_db
from app.schemas.load import LoadBase, LoadFilter, LoadResponse
from app.business.load import get_best_load
from app.utils.parsing import safe_parse_datetime
from app.utils.normalization import (
    normalize_numeric_param,
    normalize_city,
)
from app.core.config import constants

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/loads",
    tags=["Loads"],
)


@router.get(
    path="",
    name="Search Loads",
    summary="Search for available loads using multiple filters",
    response_model=Union[LoadResponse, dict],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error. Query parameters malformed or conflicting."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Unexpected error during filtering or DB access."
        },
    },
)
def search_loads(
    request: Request,
    token: APIKeyDep,
    db: Session = Depends(get_db),
    origin: Optional[str] = Query(None),
    destination: Optional[str] = Query(None),
    equipment_type: Optional[str] = Query(None),
    pickup_datetime_from: Optional[str] = Query(None),
    pickup_datetime_to: Optional[str] = Query(None),
    commodity_type: Optional[str] = Query(None),
    min_weight: Optional[str] = Query(None),
    max_weight: Optional[str] = Query(None),
    min_rate: Optional[str] = Query(None),
    max_rate: Optional[str] = Query(None),
    min_miles: Optional[str] = Query(None),
    max_miles: Optional[str] = Query(None),
) -> Union[LoadBase, dict]:
    """
    Search for the most suitable load based on filter parameters.
    If no exact match is found, the search is relaxed using business rules.

    Returns the highest-priority matching load or a message if none found.
    """

    try:
        # --- Normalize and clean inputs ---
        normalized_origin = normalize_city(origin)
        normalized_destination = normalize_city(destination)

        normalized_equipment_type = normalize_numeric_param(
            equipment_type, "equipment_type"
        )
        normalized_commodity_type = normalize_numeric_param(
            commodity_type, "commodity_type"
        )

        pickup_from = safe_parse_datetime(pickup_datetime_from)
        pickup_to = safe_parse_datetime(pickup_datetime_to)

        normalized_min_weight = normalize_numeric_param(min_weight, "min_weight")
        normalized_max_weight = normalize_numeric_param(max_weight, "max_weight")
        normalized_min_rate = normalize_numeric_param(min_rate, "min_rate")
        normalized_max_rate = normalize_numeric_param(max_rate, "max_rate")
        normalized_min_miles = normalize_numeric_param(min_miles, "min_miles")
        normalized_max_miles = normalize_numeric_param(max_miles, "max_miles")

        # --- Construct domain-specific filter object ---
        filters = LoadFilter(
            origin=normalized_origin,
            destination=normalized_destination,
            equipment_type=normalized_equipment_type,
            pickup_datetime_from=pickup_from,
            pickup_datetime_to=pickup_to,
            commodity_type=normalized_commodity_type,
            min_weight=normalized_min_weight,
            max_weight=normalized_max_weight,
            min_rate=normalized_min_rate,
            max_rate=normalized_max_rate,
            min_miles=normalized_min_miles,
            max_miles=normalized_max_miles,
        )

        # --- Business logic: retrieve best load ---
        best_load = get_best_load(db, filters)

        logger.debug(f"[LOAD SEARCH] Constructed LoadFilter: {filters}")

        # --- Business logic: retrieve best load ---
        best_load = get_best_load(db, filters)

        if not best_load:
            logger.info("[LOAD SEARCH - OUTPUT] No matching loads found.")
            return {"message": constants.NO_LOADS_FOUND_MSG}

        logger.info(f"[LOAD SEARCH - OUTPUT] Best load found: {best_load}")
        return best_load

    except Exception as e:
        logger.error(f"[LOAD SEARCH - ERROR] {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error searching loads.",
        )
