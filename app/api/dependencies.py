from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from app.core.config import settings

# Configurar header y validación
api_key_header = APIKeyHeader(name=settings.AUTH_HEADER_KEY, auto_error=False)


async def verify_api_key(api_key: str = Depends(api_key_header)) -> str:
    if api_key != settings.AUTH_API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid or missing API Key"
        )
    return api_key


# Tipo anotado reutilizable
APIKeyDep = Annotated[str, Depends(verify_api_key)]
