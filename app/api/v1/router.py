from fastapi import APIRouter

from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.clients import router as client_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["User"])
router.include_router(client_router, prefix="/client", tags=["Client"])
