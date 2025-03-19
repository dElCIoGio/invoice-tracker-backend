from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from datetime import datetime

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.dependencies import get_settings, get_mongo_client, get_logger
from app.api.base_router import router as base_router
from app.middleware.ResponseMiddleware import ResponseFormatterMiddleware

settings = get_settings()
logger = get_logger()

@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:

    logger.info(f"App started in {settings.ENVIRONMENT} mode")

    mongo_client = get_mongo_client()

    logger.info("Initializing Mongo DB client")
    try:
        await mongo_client.init_db()
    except Exception as error:
        logger.error(error)

    yield
    logger.info("Closing Mongo DB client connection")
    await mongo_client.close_connection()

    logger.info("Shutting down")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ResponseFormatterMiddleware)

app.include_router(base_router, prefix=settings.API_BASE_ROUTE)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": app.version
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "success": False,
            "message": exc.detail,
            "data": None,
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            },
            "meta": None
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "success": False,
            "message": "Validation error",
            "data": None,
            "error": {
                "code": 422,
                "message": "Invalid request data",
                "details": exc.errors()
            },
            "meta": None
        }
    )