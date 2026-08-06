from uuid import UUID

from sqlalchemy.orm import Session
from app.exception.model_not_found_exception import ModelNotFoundException
from app.exception.duplicate_version_exception import DuplicateVersionException
from app.exception.InvalidTransitionException import InvalidTransitionException
from app.exception.version_not_found_exception import VersionNotFoundException
from app.enums.stages import ModelRegistryStages
from app.model.model_version import ModelVersion
from app.repository.ml_model_repository import MLModelRepository
from app.repository.model_version_repository import ModelVersionRepository


class ModelVersionService:

    def __init__(self):
        self.model_repository = MLModelRepository()
        self.version_repository = ModelVersionRepository()

    def register_version(self, db: Session, version: ModelVersion) -> ModelVersion:
        model = self.model_repository.get_by_id(db, version.model_id)
        if model is None:
            raise ModelNotFoundException(model_id=version.model_id)

        existing = self.version_repository.find_by_version(
            db, version.model_id, version.version
        )

        if existing:
            raise DuplicateVersionException(
                model_id=version.model_id, version=version.version
            )

        version.stage = ModelRegistryStages.DRAFT
        version.approved = False
        return self.version_repository.create(db, version)

    def list_versions(self, db: Session, model_id: UUID) -> list[ModelVersion]:
        version = self.version_repository.find_by_model(db, model_id)
        if version is None or not version:
            raise ModelNotFoundException(model_id=model_id)
        return version

    def change_stage(
        self,
        db: Session,
        model_id: UUID,
        version_id: UUID,
        new_stage: ModelRegistryStages,
    ) -> ModelVersion:
        version = self.version_repository.find_by_model_and_version_id(
            db, model_id=model_id, version_id=version_id
        )

        if version is None:
            raise VersionNotFoundException(version_id=version_id)

        self.validate_transition(version.stage, new_stage)
        version.stage = new_stage
        if new_stage is ModelRegistryStages.APPROVED:
            version.approved = True
        return self.version_repository.update(db, version)

    @staticmethod
    def validate_transition(
        current: ModelRegistryStages, target: ModelRegistryStages
    ) -> None:
        allowed = {
            ModelRegistryStages.DRAFT: [
                ModelRegistryStages.VALIDATED,
            ],
            ModelRegistryStages.VALIDATED: [
                ModelRegistryStages.APPROVED,
            ],
            ModelRegistryStages.APPROVED: [
                ModelRegistryStages.STAGING,
            ],
            ModelRegistryStages.STAGING: [
                ModelRegistryStages.PRODUCTION,
            ],
            ModelRegistryStages.PRODUCTION: [
                ModelRegistryStages.ARCHIVED,
            ],
            ModelRegistryStages.ARCHIVED: [],
        }

        if target not in allowed[current]:
            raise InvalidTransitionException(current=current.name, target=target.name)
