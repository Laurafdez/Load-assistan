from typing import Optional, List
from sqlalchemy.orm import Session
from app.schemas.load import LoadFilter, LoadResponse
from app.crud.load import filter_loads_from_db
from app.core.config import constants


def get_best_load(db: Session, filters: LoadFilter) -> Optional[LoadResponse]:
    """
    Retrieve the most relevant load based on filtering criteria and business rules.

    Steps:
    1. Apply strict filtering based on all provided fields.
    2. If no results, retry with relaxed filters (e.g., ignore time/miles).
    3. Prioritize loads with urgency and earlier delivery.
    4. Enrich the top load with calculated pricing data.

    Args:
        db (Session): SQLAlchemy database session.
        filters (LoadFilter): Filtering constraints provided by the user.

    Returns:
        Optional[LoadResponse]: The top prioritized load with pricing info,
                                or None if no loads matched.
    """
    strict_results = filter_loads_from_db(db, filters)

    if not strict_results:
        relaxed_filters = filters.copy(update=constants.RELAXED_FILTER_FIELDS)
        strict_results = filter_loads_from_db(db, relaxed_filters)

    if not strict_results:
        return None

    prioritized = prioritize_loads(strict_results)
    top_load = prioritized[0]
    return enrich_with_pricing(top_load)


def prioritize_loads(loads: List) -> List:
    """
    Rank loads based on urgency and delivery date.

    Prioritization rules:
    - Loads containing the keyword defined in URGENT_KEYWORD (e.g., "urgent")
      in the `notes` field are ranked first.
    - Within the same urgency level, loads are sorted by earliest delivery time.

    Args:
        loads (List): List of load objects (from the DB).

    Returns:
        List: Sorted list of loads from most to least priority.
    """
    return sorted(
        loads,
        key=lambda load: (
            constants.URGENT_KEYWORD not in (load.notes or "").lower(),
            load.delivery_datetime or constants.FALLBACK_DELIVERY_DATETIME,
        ),
    )


def enrich_with_pricing(load) -> LoadResponse:
    """
    Adds calculated pricing metadata (first_offer, max_rate, rate_per_mile)
    to the given load and returns it as a LoadResponse.

    Args:
        load: SQLAlchemy load object from the DB.

    Returns:
        LoadResponse: Load enriched with pricing details.
    """
    from app.schemas.load import LoadResponse

    pricing = _calculate_load_offer(
        miles=load.miles,
        equipment_type=load.equipment_type,
        notes=load.notes,
        commodity_type=load.commodity_type,
        loadboard_rate=load.loadboard_rate,
    )

    return LoadResponse(
        **load.__dict__,
        first_offer=pricing["first_offer"],
        max_rate=pricing["max_rate"],
        rate_per_mile=pricing["rate_per_mile"],
    )


def _calculate_load_offer(
    miles: float,
    equipment_type: str,
    notes: Optional[str] = "",
    commodity_type: Optional[str] = "",
    loadboard_rate: Optional[float] = 0.0,
) -> dict:
    """
    Compute pricing components (first_offer, max_rate, rate_per_mile) based
    on load attributes and business rules.

    Business logic:
    - Starts with a base rate per mile.
    - Adjusts rate based on equipment type, urgency, and commodity.
    - First offer is a discounted version of loadboard rate.
    - Max rate is the higher between loadboard rate and first_offer + minimum margin.

    Args:
        miles (float): Distance in miles for the load.
        equipment_type (str): Equipment type required.
        notes (Optional[str]): Notes possibly indicating urgency.
        commodity_type (Optional[str]): Type of goods.
        loadboard_rate (Optional[float]): Publicly listed rate for the load.

    Returns:
        dict: A dictionary with `first_offer`, `max_rate`, and `rate_per_mile`.
    """
    rate_per_mile = constants.BASE_RATE_PER_MILE

    if equipment_type.lower() in ["reefer", "flatbed"]:
        rate_per_mile += constants.EQUIPMENT_PREMIUM
    if notes and "urgent" in notes.lower():
        rate_per_mile += constants.URGENCY_PREMIUM
    if commodity_type and "medical" in commodity_type.lower():
        rate_per_mile += constants.MEDICAL_PREMIUM

    # First offer is a slight discount from listed price
    first_offer = loadboard_rate * (1 - constants.DISCOUNT_RATE)

    # Ensure max is not below public rate, add margin if needed
    calculated_max = first_offer + constants.MIN_MARGIN
    max_rate = max(loadboard_rate, calculated_max)

    return {
        "first_offer": round(first_offer),
        "max_rate": max_rate,
        "rate_per_mile": round(rate_per_mile, 2),
    }
