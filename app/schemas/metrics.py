from pydantic import BaseModel, Field


class SentimentSummary(BaseModel):
    """
    Breakdown of detected sentiment from carrier calls.
    """

    positive: int = Field(..., description="Number of calls with positive sentiment")
    neutral: int = Field(..., description="Number of calls with neutral sentiment")
    negative: int = Field(..., description="Number of calls with negative sentiment")


class SatisfactionStats(BaseModel):
    """
    Summary of carrier satisfaction metrics.
    """

    satisfied: int = Field(..., description="Number of carriers that were satisfied")
    unsatisfied: int = Field(
        ..., description="Number of carriers that were unsatisfied"
    )
    unknown: int = Field(
        ..., description="Number of calls with unknown satisfaction status"
    )


class MetricsResponse(BaseModel):
    """
    Aggregated operational metrics related to loads and call interactions.
    """

    total_loads: int = Field(..., description="Total number of loads created")
    total_calls: int = Field(..., description="Total number of calls logged")
    accepted: int = Field(..., description="Total number of accepted calls")
    rejected: int = Field(..., description="Total number of rejected calls")
    failed_negotiation: int = Field(
        ..., description="Total calls with failed negotiations"
    )
    no_response: int = Field(
        ..., description="Total calls with no response from carriers"
    )
    interested_follow_up: int = Field(
        ..., description="Total calls with follow-up interest"
    )

    avg_agreed_price: float = Field(
        ..., description="Average agreed price across all accepted calls"
    )
    avg_call_duration_sec: float = Field(
        ..., description="Average duration of calls in seconds"
    )
    avg_attempts: float = Field(
        ..., description="Average number of call attempts made per load"
    )
    avg_counter_offers: float = Field(
        ..., description="Average number of counter offers received"
    )

    sentiment_summary: SentimentSummary = Field(
        ..., description="Distribution of detected sentiments"
    )
    satisfaction_summary: SatisfactionStats = Field(
        ..., description="Overview of carrier satisfaction levels"
    )
