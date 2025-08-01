from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AUTH_HEADER_KEY: str = "X-API-Key"
    AUTH_API_KEY: str = "my-secret-api-key-123"
    FMCSA_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
