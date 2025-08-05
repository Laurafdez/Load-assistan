import uuid
from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database_engine.base_class import Base


class Load(Base):
    """
    SQLAlchemy ORM model representing a transportation load.

    This table holds the necessary attributes to describe a freight load
    that can be assigned to a carrier via the AI assistant.

    Attributes:
        id (UUID): Universally unique identifier for the load.
        origin (str): Pickup location of the load.
        destination (str): Delivery location of the load.
        pickup_datetime (datetime): Scheduled pickup date and time.
        delivery_datetime (datetime): Scheduled delivery date and time.
        equipment_type (str): Required equipment for the load.
        loadboard_rate (float): Offered rate on the load board (USD).
        notes (str): Optional comments or special instructions.
        weight (float): Load weight (pounds).
        commodity_type (str): Type of goods being transported.
        num_of_pieces (int): Number of pieces/packages.
        miles (float): Total distance in miles.
        dimensions (str): Load dimensions (e.g., "48x40x60").
    """

    __tablename__ = "loads"

    load_id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    pickup_datetime = Column(DateTime, nullable=False)
    delivery_datetime = Column(DateTime, nullable=False)
    equipment_type = Column(String(50), nullable=False)
    loadboard_rate = Column(Float, nullable=True)
    notes = Column(String(255), nullable=True)
    weight = Column(Float, nullable=True)
    commodity_type = Column(String(100), nullable=True)
    num_of_pieces = Column(Integer, nullable=True)
    miles = Column(Float, nullable=True)
    dimensions = Column(String(100), nullable=True)
