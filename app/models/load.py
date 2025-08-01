from sqlalchemy import Column, String, Float, Integer, DateTime
from app.database_engine.base_class import Base


class Load(Base):
    __tablename__ = "loads"

    load_id = Column(String(50), primary_key=True, index=True)
    origin = Column(String(100))
    destination = Column(String(100))
    pickup_datetime = Column(DateTime)
    delivery_datetime = Column(DateTime)
    equipment_type = Column(String(50))
    loadboard_rate = Column(Float)
    notes = Column(String(255))
    weight = Column(Float)
    commodity_type = Column(String(100))
    num_of_pieces = Column(Integer)
    miles = Column(Float)
    dimensions = Column(String(100))
