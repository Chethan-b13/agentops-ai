from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import Base


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )