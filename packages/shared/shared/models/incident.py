from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from shared.database.base import Base


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    alarm_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    service: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    region: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    metric_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    threshold: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    current_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="unknown",
    )

    source: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="cloudwatch",
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="new",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )