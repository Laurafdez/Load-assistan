from enum import Enum
from pydantic import BaseModel, Field


class FinalStatus(str, Enum):
    """
    Enumeration of possible negotiation outcomes.
    """

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COUNTER = "counter"
    LIMIT_REACHED = "limit_reached"


class CounterOfferRequest(BaseModel):
    """
    Schema for a carrier's counteroffer request during a load negotiation.
    """

    carrier_offer: float = Field(
        ..., gt=0, description="Offer proposed by the carrier in USD"
    )
    last_offer: float = Field(..., gt=0, description="Our previous proposal in USD")
    negotiation_round: int = Field(
        ..., ge=1, le=3, description="Current negotiation round (1-3)"
    )
    max_rate: float = Field(..., gt=0, description="Maximum allowable rate in USD")


class CounterOfferResponse(BaseModel):
    """
    Schema for the response to a counteroffer request.
    """

    final_status: FinalStatus = Field(
        ..., description="One of: accepted, rejected, counter, limit_reached"
    )
    counter_suggestion: float | None = Field(
        None, description="Next counteroffer price in USD if negotiation continues"
    )
    rounds_left: int = Field(..., description="Number of negotiation rounds remaining")
    message: str = Field(
        ..., description="Human-friendly text to present to the carrier"
    )
