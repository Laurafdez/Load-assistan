from pydantic import BaseModel
from datetime import datetime


class LoadBase(BaseModel):
    load_id: str
    origin: str
    destination: str
    pickup_datetime: datetime
    delivery_datetime: datetime
    equipment_type: str
    loadboard_rate: float
    notes: str | None = None
    weight: float
    commodity_type: str
    num_of_pieces: int
    miles: float
    dimensions: str

    class Config:
        orm_mode = True
