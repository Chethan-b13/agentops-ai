from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import Base


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )