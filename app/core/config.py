from datetime import datetime
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pydantic import validator
import json


class Settings(BaseSettings):
    # Core
    PROJECT_NAME: str = "Load Assistant API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    TESTING: bool = False

    # Security
    AUTH_HEADER_KEY: str = "X-API-Key"
    AUTH_API_KEY: str = "my-secret-api-key-123"

    # External APIs
    FMCSA_API_KEY: str
    DATABASE_URL: str
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []
    FMCSA_URL: str
    WEB_KEY: str


    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def parse_cors(cls, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return [v.strip() for v in value.split(",")]
        return value

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


class Constants:
    # === Business Logic Constants ===
    # Word used to determine load urgency
    URGENT_KEYWORD: str = "urgent"

    # Fields to relax when strict filter returns no results
    RELAXED_FILTER_FIELDS: dict = {
        "pickup_datetime_from": None,
        "pickup_datetime_to": None,
        "min_miles": None,
        "max_miles": None,
    }
    BASE_RATE_PER_MILE = 2.75
    EQUIPMENT_PREMIUM = 0.20
    URGENCY_PREMIUM = 0.10
    MEDICAL_PREMIUM = 0.05
    FALLBACK_RATE_CAP = 3.25
    MIN_FIRST_OFFER_RATIO = 0.75
    DEFAULT_FIRST_OFFER_RATIO = 0.80
    MIN_MARGIN = 150
    NO_LOADS_FOUND_MSG = "No matching loads found with the provided filters."
    MAX_RATE_BONUS = 0.50
    MIN_MARGIN = 150
    DISCOUNT_RATE = 0.10

    # Default delivery date fallback if missing
    FALLBACK_DELIVERY_DATETIME: datetime = datetime.max
    MAX_NEGOTIATION_ROUNDS = 3
    ROUNDING_STEP = 10
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
constants = Constants()
