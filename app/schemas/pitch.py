from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LoadPitchResponse(BaseModel):
    load_id: str
    origin: str
    destination: str
    pickup_datetime: datetime
    delivery_datetime: datetime
    equipment_type: Optional[str]
    loadboard_rate: Optional[float]
    notes: Optional[str]
    weight: Optional[float]
    commodity_type: Optional[str]
    num_of_pieces: Optional[int]
    miles: Optional[float]
    dimensions: Optional[str]
