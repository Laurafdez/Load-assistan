from fastapi import APIRouter, Path
from app.schemas.carrier import VerifyMCResponse

router = APIRouter()


@router.get(
    "/carriers/authorization/{mc_number}",
    tags=["Carriers"],
    response_model=VerifyMCResponse,
    summary="Get carrier authorization status by MC number",
)
def get_carrier_authorization_status(
    mc_number: str = Path(
        ..., min_length=5, max_length=8, description="Motor Carrier number"
    ),
):
    """
    Returns the FMCSA-style authorization status for a given carrier MC number.

    - Starts with '5' → authorized.
    - Others → non-authorized.
    """
    if mc_number.startswith("5"):
        return VerifyMCResponse(
            status="authorized",
            carrier_name=f"Carrier MC-{mc_number}",
            operation="Interstate",
        )
    return VerifyMCResponse(
        status="non-authorized",
        carrier_name="None",
        operation="None",
    )
