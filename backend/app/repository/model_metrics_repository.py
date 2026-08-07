from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.model.model_metrics import ModelMetrics
from app.model.model_version import ModelVersion
from app.repository.base_repository import BaseRepository


class ModelMetricsRepository(BaseRepository[ModelMetrics]):

    def __init__(self):
        super().__init__(ModelMetrics)

    def find_by_model(self, db: Session, model_id: str) -> list[ModelMetrics]:
        stmt = (
            select(ModelMetrics)
            .join(ModelVersion, ModelMetrics.model_version_id == ModelVersion.id)
            .where(ModelVersion.model_id == model_id)
            .options(joinedload(ModelMetrics.model_version))
            .order_by(ModelVersion.created_at.desc())
        )
        return list(db.scalars(stmt).all())
