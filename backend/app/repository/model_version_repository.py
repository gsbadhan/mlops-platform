from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model.model_version import ModelVersion
from app.repository.base_repository import BaseRepository


class ModelVersionRepository(BaseRepository[ModelVersion]):

    def __init__(self):
        super().__init__(ModelVersion)

    def find_by_model(self, db: Session, model_id: str) -> list[ModelVersion]:
        stmt = (
            select(ModelVersion)
            .where(ModelVersion.model_id == model_id)
            .order_by(ModelVersion.created_at.desc())
        )

        return list(db.scalars(stmt).all())

    def find_by_version(
        self, db: Session, model_id: str, version: str
    ) -> ModelVersion | None:

        stmt = select(ModelVersion).where(
            ModelVersion.model_id == model_id, ModelVersion.version == version
        )
        return db.scalar(stmt)

    def find_by_version_id(self, db: Session, version_id: str) -> ModelVersion | None:
        return db.scalar(select(ModelVersion).where(ModelVersion.id == version_id))

    def find_by_model_and_version_id(
        self, db: Session, model_id: str, version_id: str
    ) -> ModelVersion | None:
        return db.scalar(
            select(ModelVersion).where(
                ModelVersion.id == version_id,
                ModelVersion.model_id == model_id,
            )
        )
