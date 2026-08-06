from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model.deployment_history import DeploymentHistory
from app.repository.base_repository import BaseRepository


class DeploymentHistoryRepository(BaseRepository[DeploymentHistory]):

    def __init__(self):
        super().__init__(DeploymentHistory)

    def find_by_id(self, db: Session, id: str) -> DeploymentHistory | None:
        return db.get(DeploymentHistory, id)

    def find_all(self, db: Session) -> list[DeploymentHistory]:
        stmt = select(DeploymentHistory).order_by(DeploymentHistory.created_at.desc())
        return list(db.scalars(stmt).all())

    def find_latest_by_deployment(
        self, db: Session, deployment_id: str
    ) -> DeploymentHistory | None:
        stmt = (
            select(DeploymentHistory)
            .where(DeploymentHistory.deployment_id == deployment_id)
            .order_by(DeploymentHistory.created_at.desc())
            .limit(1)
        )
        return db.scalar(stmt)
