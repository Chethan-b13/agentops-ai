from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.sql import func

from shared.database.base import Base


class RemediationResult(Base):
    __tablename__ = "remediation_results"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    incident_id: Mapped[str] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    reasoning: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    recommended_actions: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
    )

    rollback_plan: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
    )

    risk: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    requires_downtime: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )