from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import Base


class IncidentEvidence(Base):
    __tablename__ = "incident_evidence"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    incident_id: Mapped[str] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=False,
    )

    evidence_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    raw_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    summary_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )