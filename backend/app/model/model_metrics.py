import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class ModelMetrics(Base):
    __tablename__ = "model_metrics"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    model_version_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("model_versions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    accuracy: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    precision: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    recall: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    f1_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    model_version: Mapped["ModelVersion"] = relationship(
        back_populates="metrics",
    )
