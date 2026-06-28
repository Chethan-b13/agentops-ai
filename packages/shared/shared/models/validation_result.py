from sqlalchemy import (
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


class ValidationResult(Base):
    __tablename__ = "validation_results"

    id: Mapped[int] = mapped_column(primary_key=True)

    incident_id: Mapped[str] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    findings: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
    )

    recommendations: Mapped[list[str]] = mapped_column(
        ARRAY(String),
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