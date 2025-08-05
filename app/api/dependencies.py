from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from app.core.config import settings

# Define the API key header to be extracted from incoming requests
api_key_header = APIKeyHeader(
    name=settings.AUTH_HEADER_KEY,
    auto_error=False,  # Don't raise automatic error; handle manually
)


async def verify_api_key(api_key: str = Depends(api_key_header)) -> str:
    """
    Verifies the provided API key against the expected key in settings.

    Args:
        api_key (str): The API key extracted from the request header.

    Raises:
        HTTPException: If the API key is invalid or missing.

    Returns:
        str: The validated API key.
    """
    if api_key != settings.AUTH_API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid or missing API Key"
        )
    return api_key


# Annotated type alias for dependency injection of the API key
APIKeyDep = Annotated[str, Depends(verify_api_key)]
