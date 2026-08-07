from sqlalchemy.orm import Session

from app.repository.model_metrics_repository import ModelMetricsRepository


class ModelMetricsService:

    def __init__(self, repository: ModelMetricsRepository):
        self.repository = repository

    def get_model_metrics(self, db: Session, model_id: str):
        return self.repository.find_by_model(db=db, model_id=model_id)
