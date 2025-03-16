from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse

from app.core.dependencies import get_settings, get_mongo_client, get_logger

settings = get_settings()
logger = get_logger()


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:

    logger.info("Starting up")

    # mongo_client = get_mongo_client()

    logger.info("Initializing Mongo DB client")
    # mongo_client.init_db()

    yield
    logger.info("Closing Mongo DB client connection")
    # await mongo_client.close_connection()

    logger.info("Shutting down")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": app.version
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred."},
    )