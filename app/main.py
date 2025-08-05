import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.middlewares.api_log_request import APILogRequestMiddleware


def create_app() -> FastAPI:
    """
    Factory function that configures and returns the FastAPI application instance.

    Responsibilities:
    - Set up structured logging.
    - Register middlewares (CORS, request logging).
    - Register API routes.
    """

    # Configure global logging
    logging.basicConfig(
        level=logging.DEBUG if settings.TESTING else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger = logging.getLogger("uvicorn")

    # Instantiate FastAPI application
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        generate_unique_id_function=lambda route: f"{route.tags[0]}-{route.name}",
    )

    # Register request logging middleware
    app.add_middleware(APILogRequestMiddleware)

    # Register CORS middleware if configured
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                origin.strip("/") for origin in settings.BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Register API routes with version prefix
    app.include_router(api_router, prefix=settings.API_V1_STR)

    logger.info(
        "FastAPI application successfully configured and ready to serve requests."
    )
    return app


app = create_app()
