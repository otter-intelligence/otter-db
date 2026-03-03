from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    Index,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AlarmEpisodeAcknowledgment(Base):
    __tablename__ = "alarm_episode_acknowledgment"
    __table_args__ = (
        PrimaryKeyConstraint("episode_id", name="alarm_episode_acknowledgment_pkey"),
        UniqueConstraint(
            "sensor_id", "alarm_type", "episode_started_at", name="uq_ack_episode"
        ),
        Index(
            "idx_ack_active",
            "sensor_id",
            "alarm_type",
            postgresql_include=[],
            postgresql_where="(cleared_at IS NULL)",
        ),
        Index(
            "idx_ack_unacknowledged",
            text("created_at DESC"),
            postgresql_include=[],
            postgresql_where="(is_acknowledged = false)",
        ),
        {
            "comment": "Tracks operator acknowledgment per alarm episode (one row per "
            "episode). The sensor inserts rows when episodes are detected and "
            "marks cleared_at when they end. The Otter Portal sets "
            "is_acknowledged=TRUE via FastAPI using episode_id. "
            "Cleared-but-unacked episodes stay visible for operator "
            "accountability."
        },
    )

    episode_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sensor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    alarm_type: Mapped[str] = mapped_column(String(50), nullable=False)
    episode_started_at: Mapped[datetime] = mapped_column(DateTime(True), nullable=False)
    is_acknowledged: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(True), nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(True), nullable=False, server_default=text("now()")
    )
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(True))
    acknowledged_by: Mapped[str | None] = mapped_column(String(100))
    cleared_at: Mapped[datetime | None] = mapped_column(DateTime(True))


class NotificationLog(Base):
    __tablename__ = "notification_log"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="notification_log_pkey"),
        Index("idx_notif_recipient_time", "recipients", "sent_at"),
        Index(
            "idx_notif_sensor_alarm_sent",
            "sensor_id",
            "alarm_type",
            "status",
            text("sent_at DESC"),
        ),
        {
            "comment": "Audit log of alarm notification emails sent by the Dagster "
            "alarm_notification_sensor."
        },
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    alarm_type: Mapped[str] = mapped_column(String(50), nullable=False)
    sensor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    notification_type: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'email'::character varying")
    )
    recipients: Mapped[str] = mapped_column(Text, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(
        DateTime(True), nullable=False, server_default=text("now()")
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'sent'::character varying")
    )
    episode_started_at: Mapped[datetime] = mapped_column(DateTime(True), nullable=False)
    subject: Mapped[str | None] = mapped_column(Text)
    peak_value: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    threshold_value: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))


class SensorAlarmStatus(Base):
    __tablename__ = "sensor_alarm_status_test"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="sensor_alarm_status_test_pkey"),
        Index("idx_sensor_alarm_sensor_created", "sensor_id", text("created_at DESC")),
        Index("idx_sensor_alarm_sensor_id", "sensor_id"),
        Index("idx_sensor_alarm_status", "sensor_status"),
        Index("idx_sensor_alarm_timestamp", "timestamp"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(True), nullable=False)
    sensor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    sensor_name: Mapped[str | None] = mapped_column(String(100))
    sensor_status: Mapped[str | None] = mapped_column(String(50))
    current_value: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    flow_active: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("true")
    )
    analysis_timestamp: Mapped[datetime | None] = mapped_column(DateTime(True))
    classification_details: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(True), server_default=text("CURRENT_TIMESTAMP")
    )
