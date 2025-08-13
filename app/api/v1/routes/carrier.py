from fastapi import APIRouter, Path
from app.schemas.carrier import VerifyMCResponse
import httpx
import os
from app.core.config import settings
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


@router.get(
    "/carriers/fmcsa/{mc_number}",
    tags=["Carriers"],
    summary="Get carrier info from FMCSA API by MC number",
)
async def get_carrier_from_fmcsa(
    mc_number: str = Path(
        ..., min_length=5, max_length=8, description="Motor Carrier number"
    ),
):
    """
    Calls the FMCSA API to retrieve carrier details for a given MC number.
    """
    url = settings.FMCSA_URL.format(mc_number=mc_number, web_key=settings.WEB_KEY)
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
