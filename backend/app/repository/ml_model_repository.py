from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model.ml_model import MLModel
from app.repository.base_repository import BaseRepository


class MLModelRepository(BaseRepository[MLModel]):

    def __init__(self):
        super().__init__(MLModel)

    def find_by_name(self, db: Session, name: str) -> MLModel | None:
        stmt = select(MLModel).where(MLModel.name == name)
        return db.scalar(stmt)

    def find_all(self, db: Session) -> list[MLModel]:
        stmt = select(MLModel).order_by(MLModel.created_at.desc())
        return list(db.scalars(stmt).all())
