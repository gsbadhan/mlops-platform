from uuid import UUID

from sqlalchemy.orm import Session

from app.model.ml_model import MLModel
from app.repository.ml_model_repository import MLModelRepository
from app.exception.duplicate_model_exception import DuplicateModelException
from app.exception.model_not_found_exception import ModelNotFoundException


class MLModelService:

    def __init__(self):
        self.repository = MLModelRepository()

    def create_model(self, db: Session, model: MLModel) -> MLModel:
        existing = self.repository.find_by_name(db, model.name)
        if existing:
            raise DuplicateModelException(model_name=model.name)
        return self.repository.create(db, model)

    def get_model(self, db: Session, model_id: UUID) -> MLModel:
        model = self.repository.get_by_id(db, model_id)
        if model is None:
            raise ModelNotFoundException(model_id=model_id)
        return model

    def list_models(self, db: Session) -> list[MLModel]:
        return self.repository.find_all(db)
