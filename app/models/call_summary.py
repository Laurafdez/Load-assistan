from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Enum,
    ForeignKey,
    Boolean,
)
from app.database_engine.base_class import Base
import enum


class CallOutcomeEnum(str, enum.Enum):
    """Enumeration of possible outcomes for a carrier call."""

    accepted = "accepted"
    rejected = "rejected"
    failed_negotiation = "failed_negotiation"
    no_response = "no_response"
    interested_follow_up = "interested_follow_up"  # Indicates future interest


class SentimentEnum(str, enum.Enum):
    """Enumeration of detected sentiment in the call."""

    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class CallSummary(Base):
    """
    SQLAlchemy model representing a summary of a call with a carrier.

    This table stores key information about the interaction, including outcome,
    sentiment, pricing, and engagement metrics that can be used for analytics
    and operational improvements.
    """

    __tablename__ = "call_summaries"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key for the call summary record.",
    )
    load_id = Column(
        UUID(as_uuid=True),
        ForeignKey("loads.load_id"),
        nullable=False,
        doc="Reference to the associated load.",
    )

    agreed_price = Column(Float, doc="Final agreed price if the load was accepted.")
    comments = Column(String(500), doc="Additional comments or notes from the call.")
    special_conditions = Column(
        String(255), doc="Any special conditions discussed during the call."
    )

    outcome = Column(Enum(CallOutcomeEnum), doc="Final outcome of the call.")
    sentiment = Column(
        Enum(SentimentEnum),
        doc="Overall sentiment detected from the carrier during the call.",
    )

    call_duration_sec = Column(
        Integer, nullable=True, doc="Duration of the call in seconds."
    )
    attempts = Column(
        Integer, default=1, doc="Number of engagement attempts made with the carrier."
    )
    counter_offers = Column(
        Integer, default=0, doc="Number of counter offers made by the carrier."
    )
    satisfaction = Column(
        Boolean,
        nullable=True,
        doc="Indicates whether the carrier found the call helpful.",
    )
