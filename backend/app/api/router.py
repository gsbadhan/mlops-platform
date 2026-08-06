from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.models import router as models_router
from app.api.v1.model_version import router as model_version_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health_router)
api_v1_router.include_router(models_router)
api_v1_router.include_router(model_version_router)
