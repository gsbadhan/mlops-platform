from app.service.ml_model_service import MLModelService
from app.service.model_version_service import ModelVersionService
from app.service.deployment_service import DeploymentService
from app.repository.deployment_repository import DeploymentRepository
from app.repository.model_version_repository import ModelVersionRepository
from app.repository.deployment_history_repository import DeploymentHistoryRepository


def get_ml_model_service() -> MLModelService:
    return MLModelService()


def get_model_version_service() -> ModelVersionService:
    return ModelVersionService()


def get_deployment_service():
    return DeploymentService(
        DeploymentRepository(), ModelVersionRepository(), DeploymentHistoryRepository()
    )
