from app.service.ml_model_service import MLModelService
from app.service.model_version_service import ModelVersionService


def get_ml_model_service() -> MLModelService:
    return MLModelService()


def get_model_version_service() -> ModelVersionService:
    return ModelVersionService()
