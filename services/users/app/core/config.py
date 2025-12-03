# Generate a configuration object to be used across the application, including settings like environment type and application metadata.
import secrets
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from decouple import config

class Configuration(BaseSettings):
    IS_PRODUCTION: bool = False if config("ENV", default='local') == 'local' else True
    PROJECT_NAME: str = "FastAPI - User Microservice"
    PROJECT_VERSION: str = "1.0.0"
    PORT: int = 8000

configuration = Configuration()

class Settings(BaseSettings):

    ENV: str
    DATABASE_URL: str

    POSTGRES_USER: str = config("POSTGRES_USER", default="postgres")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="password")
    POSTGRES_DB: str = config("POSTGRES_DB", default="fastapi_db")
    POSTGRES_HOST: str = config("POSTGRES_HOST", default="localhost")
    POSTGRES_PORT: int = config("POSTGRES_PORT", default=5432)
    DB_URL: Optional[str] = config("DB_URL", default=f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
    PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI Microservices")
    PROJECT_VERSION: str = config("PROJECT_VERSION", default="1.0.0")
    
    REDIS_HOST: str = config("REDIS_HOST", default="localhost")
    REDIS_PORT: int = config("REDIS_PORT", default=6379)
    REDIS_DB: int = config("REDIS_DB", default=0)
    REDIS_URL: Optional[str] = config("REDIS_URL", default=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")

    # JWT Settings
    JWT_SECRET: str = config("JWT_SECRET", default=secrets.token_urlsafe(32))
    JWT_ALGORITHM: str = config("JWT_ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=60)

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()