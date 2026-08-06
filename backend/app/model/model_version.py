from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Enum, ForeignKey, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.enums.stages import ModelRegistryStages


class ModelVersion(Base):
    __tablename__ = "model_versions"

    __table_args__ = (
        UniqueConstraint(
            "model_id",
            "version",
            name="uq_model_version",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    model_id: Mapped[uuid.UUID] = mapped_column(
        String(36),
        ForeignKey("ml_models.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    version: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    artifact_uri: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    training_data_uri: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    stage: Mapped[ModelRegistryStages] = mapped_column(
        Enum(ModelRegistryStages),
        default=ModelRegistryStages.DRAFT,
        nullable=False,
    )

    approved: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    tags: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    ml_model: Mapped["MLModel"] = relationship(
        back_populates="versions",
    )

    deployments = relationship(
        "Deployment",
        back_populates="model_version",
        cascade="all, delete-orphan",
    )
