from pydantic import BaseModel


class SentimentSummary(BaseModel):
    positive: int
    neutral: int
    negative: int


class MetricsResponse(BaseModel):
    total_loads: int
    total_calls: int
    accepted: int
    rejected: int
    pending: int
    avg_agreed_price: float
    sentiment_summary: SentimentSummary
