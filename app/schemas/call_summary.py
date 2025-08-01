from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class CallOutcomeEnum(str, Enum):
    accepted = "accepted"
    rejected = "rejected"
    failed_negotiation = "failed_negotiation"
    no_response = "no_response"


class SentimentEnum(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class CallSummaryCreate(BaseModel):
    load_id: str = Field(..., description="The ID of the load")
    agreed_price: Optional[float] = Field(None, description="Final agreed price")
    comments: Optional[str] = Field(None, description="Additional call comments")
    special_conditions: Optional[str] = Field(None, description="Any special agreement")
    outcome: CallOutcomeEnum = Field(..., description="Call outcome")
    sentiment: SentimentEnum = Field(..., description="Carrier sentiment")


class CallSummaryResponse(CallSummaryCreate):
    id: int

    class Config:
        from_attributes = True
