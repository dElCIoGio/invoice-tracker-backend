import logging
from functools import lru_cache

from app.core.config import Settings
from app.db.database import MongoDBClient
from app.schema.user import UserDocument
from app.schema.client import ClientDocument


@lru_cache()
def get_settings():
    return Settings()


@lru_cache()
def get_mongo_client():
    settings = get_settings()
    return MongoDBClient(
        mongo_uri=settings.MONGO_URI,
        database_name=settings.MONGO_DATABASE_NAME,
        document_models=[UserDocument, ClientDocument]
    )

def get_logger():
    """Returns a singleton logger instance."""
    logger = logging.getLogger("invoice-tracker")  # Unique logger name

    if not logger.handlers:  # Prevent duplicate handlers
        logger.setLevel(logging.INFO)

        # Define log format
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # File handler
        file_handler = logging.FileHandler("app.log")
        file_handler.setFormatter(formatter)

        # Console handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger