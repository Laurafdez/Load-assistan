from sqlalchemy import Column, String, Float, Integer, Enum, ForeignKey
from app.database_engine.base_class import Base
import enum


class CallOutcomeEnum(str, enum.Enum):
    accepted = "accepted"
    rejected = "rejected"
    failed_negotiation = "failed_negotiation"
    no_response = "no_response"


class SentimentEnum(str, enum.Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class CallSummary(Base):
    __tablename__ = "call_summaries"

    id = Column(Integer, primary_key=True, index=True)
    load_id = Column(String, ForeignKey("loads.load_id"))
    agreed_price = Column(Float)
    comments = Column(String(500))
    special_conditions = Column(String(255))
    outcome = Column(Enum(CallOutcomeEnum))
    sentiment = Column(Enum(SentimentEnum))
