from fastapi import APIRouter

from app.api.v1 import health, models, model_version, deployment, model_metrics

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(health.router)
api_v1_router.include_router(models.router)
api_v1_router.include_router(model_version.router)
api_v1_router.include_router(deployment.router)
api_v1_router.include_router(model_metrics.router)
