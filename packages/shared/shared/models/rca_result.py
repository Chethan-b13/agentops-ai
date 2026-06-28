from sqlalchemy import (
    Float,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from shared.database.base import Base


class RCAResult(Base):

    __tablename__ = "rca_results"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    incident_id: Mapped[str] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=False,
        index=True,
    )

    root_cause: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    explanation: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    supporting_evidence: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
    )