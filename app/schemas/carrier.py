from pydantic import BaseModel, Field


class VerifyMCResponse(BaseModel):
    """
    Response schema for MC number verification result.
    """

    status: str = Field(..., description="Authorization status of the carrier")
    carrier_name: str = Field(..., description="Registered name of the carrier")
    operation: str = Field(
        ..., description="Type of operation (e.g., Interstate, None)"
    )

    class Config:
        from_attributes = True
