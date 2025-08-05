from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class LoadBase(BaseModel):
    """
    Shared structure for load entities.
    Used for data serialization between layers.
    """

    load_id: UUID = Field(..., description="Unique identifier of the load")
    origin: str = Field(..., description="Pickup location")
    destination: str = Field(..., description="Delivery location")
    pickup_datetime: datetime = Field(..., description="Scheduled pickup date and time")
    delivery_datetime: datetime = Field(
        ..., description="Scheduled delivery date and time"
    )
    equipment_type: str = Field(..., description="Required equipment for the load")
    loadboard_rate: float = Field(..., description="Rate offered for this load")
    notes: Optional[str] = Field(None, description="Special instructions or comments")
    weight: float = Field(..., description="Total weight of the load (lbs)")
    commodity_type: str = Field(..., description="Category of the goods")
    num_of_pieces: int = Field(..., description="Number of packages or items")
    miles: float = Field(..., description="Total mileage for the route")
    dimensions: str = Field(..., description="Load size in LxWxH format")

    class Config:
        orm_mode = True


class LoadCreate(BaseModel):
    """
    Payload structure used when creating a new load.
    The load_id will be generated server-side.
    """

    origin: str
    destination: str
    pickup_datetime: datetime
    delivery_datetime: datetime
    equipment_type: str
    loadboard_rate: float
    notes: Optional[str] = None
    weight: float
    commodity_type: str
    num_of_pieces: int
    miles: float
    dimensions: str


class LoadResponse(LoadBase):
    """
    Response schema for returning enriched load data via the API.
    """

    first_offer: Optional[float] = Field(None, description="AI-generated initial offer")
    max_rate: Optional[float] = Field(None, description="Maximum possible rate")
    rate_per_mile: Optional[float] = Field(None, description="Rate per mile")


class LoadFilter(BaseModel):
    """
    Filters used for querying available loads.
    All fields are optional.
    """

    origin: Optional[str] = Field(None, description="Filter by pickup city/state")
    destination: Optional[str] = Field(
        None, description="Filter by delivery city/state"
    )
    equipment_type: Optional[str] = Field(None, description="Required equipment type")
    pickup_datetime_from: Optional[datetime] = Field(
        None, description="Earliest acceptable pickup time"
    )
    pickup_datetime_to: Optional[datetime] = Field(
        None, description="Latest acceptable pickup time"
    )
    min_weight: Optional[float] = Field(None, description="Minimum allowed weight")
    max_weight: Optional[float] = Field(None, description="Maximum allowed weight")
    commodity_type: Optional[str] = Field(None, description="Type of commodity")
    min_rate: Optional[float] = Field(None, description="Minimum rate")
    max_rate: Optional[float] = Field(None, description="Maximum rate")
    min_miles: Optional[float] = Field(None, description="Minimum trip distance")
    max_miles: Optional[float] = Field(None, description="Maximum trip distance")
