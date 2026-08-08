from sqlalchemy.orm import Session

from app.repository.model_metrics_repository import ModelMetricsRepository
from app.schema.model_metrics import ModelMetricsResponse


class ModelMetricsService:

    def __init__(self, repository: ModelMetricsRepository):
        self.repository = repository

    def get_model_metrics(self, db: Session, model_id: str):
        rs = self.repository.find_by_model(db=db, model_id=model_id)
        return [
            ModelMetricsResponse(
                version=metric.model_version.version,
                accuracy=metric.accuracy,
                precision=metric.precision,
                recall=metric.recall,
                f1_score=metric.f1_score,
            )
            for metric in rs
        ]
