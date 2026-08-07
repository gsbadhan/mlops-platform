from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schema.model_metrics import ModelMetricsResponse
from app.service.model_metrics_service import ModelMetricsService
from app.service.dependencies import get_model_metrics_service

router = APIRouter(prefix="/models", tags=["Model Metrics"])


@router.get("/{model_id}/metrics", response_model=list[ModelMetricsResponse])
def get_model_metrics(
    model_id: UUID,
    db: Session = Depends(get_db),
    service: ModelMetricsService = Depends(get_model_metrics_service),
):
    return service.get_model_metrics(db=db, model_id=str(model_id))
