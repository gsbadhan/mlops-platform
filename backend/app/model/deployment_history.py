import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.enums.stages import DeploymentEvent
from app.enums.stages import DeploymentState


class DeploymentHistory(Base):
    __tablename__ = "deployment_history"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    deployment_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("deployments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event: Mapped[DeploymentEvent] = mapped_column(
        Enum(DeploymentEvent),
        nullable=False,
    )

    old_status: Mapped[DeploymentState | None] = mapped_column(
        Enum(DeploymentState),
        nullable=True,
    )

    new_status: Mapped[DeploymentState] = mapped_column(
        Enum(DeploymentState),
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    deployment: Mapped["Deployment"] = relationship(back_populates="history")
