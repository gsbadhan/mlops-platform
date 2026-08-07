import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.enums.stages import DeploymentEnvironment
from app.enums.stages import DeploymentState


class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    model_version_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("model_versions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    environment: Mapped[DeploymentEnvironment] = mapped_column(
        Enum(DeploymentEnvironment),
        nullable=False,
    )

    status: Mapped[DeploymentState] = mapped_column(
        Enum(DeploymentState),
        default=DeploymentState.REQUESTED,
        nullable=False,
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    failure_reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    idempotency_key: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    model_version: Mapped["ModelVersion"] = relationship(back_populates="deployments")

    history: Mapped[list["DeploymentHistory"]] = relationship(
        back_populates="deployment",
        cascade="all, delete-orphan",
        order_by="DeploymentHistory.created_at",
    )
