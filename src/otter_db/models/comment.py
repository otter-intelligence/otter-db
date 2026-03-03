import enum
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class WarningLevelEnum(enum.Enum):
    info = "info"
    warning = "warning"
    critical = "critical"


class Comment(Base):
    __tablename__ = "aquaworks_comments"
    __table_args__ = (PrimaryKeyConstraint("id", name="aquaworks_comments_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    start_day: Mapped[datetime] = mapped_column(DateTime(True), nullable=False)
    end_day: Mapped[datetime] = mapped_column(DateTime(True), nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(True), server_default=text("CURRENT_TIMESTAMP")
    )
    sensor_id: Mapped[str | None] = mapped_column(String(255))
    warning_level: Mapped[WarningLevelEnum | None] = mapped_column(
        ENUM("info", "warning", "critical", name="warning_level_enum")
    )
