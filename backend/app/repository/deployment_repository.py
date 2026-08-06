from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session, joinedload

from app.model.deployment import Deployment
from app.repository.base_repository import BaseRepository
from app.model.deployment_history import DeploymentHistory
from app.model.model_version import ModelVersion


class DeploymentRepository(BaseRepository[Deployment]):

    def __init__(self):
        super().__init__(Deployment)

    def find_by_id(self, db: Session, deployment_id: str) -> Deployment | None:
        return db.get(Deployment, deployment_id)

    def find_all(self, db: Session) -> list[Deployment]:
        stmt = select(Deployment).order_by(Deployment.created_at.desc())
        return list(db.scalars(stmt).all())

    def find_by_idempotency_key(self, db: Session, key: str) -> Deployment | None:
        stmt = select(Deployment).where(Deployment.idempotency_key == key)
        return db.scalar(stmt)

    def find_all_with_latest_history(
        self, db: Session
    ) -> list[tuple[Deployment, DeploymentHistory]]:

        latest_history = (
            select(
                DeploymentHistory.deployment_id,
                func.max(DeploymentHistory.created_at).label("latest_created_at"),
            )
            .group_by(DeploymentHistory.deployment_id)
            .subquery()
        )

        stmt = (
            select(Deployment, DeploymentHistory)
            .join(
                latest_history,
                Deployment.id == latest_history.c.deployment_id,
            )
            .join(
                DeploymentHistory,
                and_(
                    DeploymentHistory.deployment_id == latest_history.c.deployment_id,
                    DeploymentHistory.created_at == latest_history.c.latest_created_at,
                ),
            )
            .options(
                joinedload(Deployment.model_version).joinedload(ModelVersion.ml_model)
            )
            .order_by(Deployment.created_at.desc())
        )

        return db.execute(stmt).all()
