import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class APILogRequestMiddleware(BaseHTTPMiddleware):
    def _get_client_ip(self, request: Request) -> str:
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def _log_request(self, request: Request) -> None:
        logger.info(
            f"[Request] {request.method} {request.url.path} | "
            f"Query: {dict(request.query_params)} | "
            f"IP: {self._get_client_ip(request)} | "
            f"User-Agent: {request.headers.get('User-Agent', '')} | "
            f"Accept: {request.headers.get('Accept', '')} | "
            f"Content-Type: {request.headers.get('Content-Type', '')}"
        )

    def _log_response(self, request: Request, response: Response) -> None:
        logger.info(
            f"[Response] {request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Content-Type: {response.headers.get('Content-Type', '')}"
        )

    async def dispatch(self, request: Request, call_next):
        self._log_request(request)
        response = await call_next(request)
        self._log_response(request, response)
        return response
