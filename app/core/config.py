import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App settings
    PROJECT_NAME: str = "UniCollector"
    PROJECT_DESCRIPTION: str ="A production-ready FastAPI backend with authentication, database integration, and more"
    PROJECT_VERSION: str ="1.0.0"


    # API settings
    API_V1_ROUTE: str = "/api/v1"


    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["*"]  # In production, replace with specific origins

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    # DEBUG: bool = ENVIRONMENT == "development"

    # Mongo settings
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DATABASE_NAME: str = os.getenv("MONGO_DATABASE_NAME")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        case_sensitive = True
        env_file = ".env"