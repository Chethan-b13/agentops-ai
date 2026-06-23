from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import Base


class IncidentEvidence(Base):
    __tablename__ = "incident_evidence"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )