from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class CallOutcomeEnum(str, Enum):
    """
    Enum representing the possible outcomes of a call.
    """

    accepted = "accepted"
    rejected = "rejected"
    failed_negotiation = "failed_negotiation"
    no_response = "no_response"
    interested_follow_up = "interested_follow_up"


class SentimentEnum(str, Enum):
    """
    Enum representing the detected sentiment during the call.
    """

    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class CallSummaryCreate(BaseModel):
    """
    Schema for creating a new call summary entry.
    All fields are optional except `load_id`. Defaults are applied where applicable.
    """

    load_id: UUID = Field(..., description="UUID of the load associated with the call")
    agreed_price: Optional[float] = Field(
        default=None, description="Final price agreed with the carrier"
    )
    comments: Optional[str] = Field(
        default=None, description="Any additional notes from the call"
    )
    special_conditions: Optional[str] = Field(
        default=None, description="Special agreements discussed during the call"
    )
    outcome: Optional[CallOutcomeEnum] = Field(
        default=None, description="Outcome of the call with the carrier"
    )
    sentiment: Optional[SentimentEnum] = Field(
        default=None, description="Detected sentiment of the carrier during the call"
    )
    call_duration_sec: Optional[int] = Field(
        default=0, description="Total duration of the call in seconds"
    )
    attempts: Optional[int] = Field(
        default=1, description="Number of call attempts made to the carrier"
    )
    counter_offers: Optional[int] = Field(
        default=0, description="Number of counter offers proposed by the carrier"
    )
    satisfaction: Optional[bool] = Field(
        default=None, description="Whether the carrier found the interaction helpful"
    )


class CallSummaryResponse(CallSummaryCreate):
    """
    Schema for returning a call summary entry from the API.
    Extends CallSummaryCreate by including the unique database ID.
    """

    id: int = Field(..., description="Unique ID of the call summary entry")

    class Config:
        from_attributes = True
