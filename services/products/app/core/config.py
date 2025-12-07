import os
from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from decouple import config

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Determine which env file to load based on ENV variable
# Default to local if ENV is not set
env_file = BASE_DIR / ".env.local"
env_type = os.environ.get("ENV", "local").lower()
if env_type == "prod":
    env_file = BASE_DIR / ".env.prod"

print(f"Loading environment: {env_type} from {env_file}")

class Settings(BaseSettings):
    # Environment info
    ENV: str = env_type
    IS_PRODUCTION: bool = False

    # App metadata
    PROJECT_NAME: str = "FastAPI - User Microservice"
    PROJECT_VERSION: str = "1.0.0"
    PORT: int = 8000

    # Database settings
    DB_URL:str= os.environ.get("DATABASE_URL", "postgresql+asyncpg://admin:PassW0rd@localhost:5432/ecommerce_products")

    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "PassW0rd"
    POSTGRES_DB: str = "ecommerce_products"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    model_config = ConfigDict(extra="forbid")

# Load settings
settings = Settings()
settings.IS_PRODUCTION = settings.ENV.lower() == "prod"

# Example usage
print(f"App running in {'production' if settings.IS_PRODUCTION else 'local'} mode")
print(f"Database URL: {settings.DB_URL}")
