from __future__ import annotations

from typing import Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """
    Generic repository providing common CRUD operations.
    """

    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, db: Session, entity: T) -> T:
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def get_by_id(self, db: Session, entity_id: str) -> T | None:
        return db.get(self.model, entity_id)

    def get_all(self, db: Session) -> list[T]:
        return list(db.scalars(select(self.model)).all())

    def update(self, db: Session, entity: T) -> T:
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def delete(self, db: Session, entity: T) -> None:
        db.delete(entity)
        db.commit()

    def exists(self, db: Session, entity_id: str) -> bool:
        return self.get_by_id(db, entity_id) is not None