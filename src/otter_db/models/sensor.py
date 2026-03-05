from datetime import datetime

from sqlalchemy import (
    DateTime,
    Double,
    PrimaryKeyConstraint,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AvailableSensors(Base):
    __tablename__ = "available_sensors"
    __table_args__ = (PrimaryKeyConstraint("sensor_id", name="aquaworks_sensors_pkey"),)

    sensor_id: Mapped[str] = mapped_column(String(255), primary_key=True)


class SensorData(Base):
    __tablename__ = "aquaworks_data"
    __table_args__ = (
        PrimaryKeyConstraint("sensor_id", "timestamp", name="aquaworks_data_pkey"),
    )

    sensor_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(True), primary_key=True)
    value: Mapped[float] = mapped_column(Double(53), nullable=False)


class SensorTranslation(Base):
    __tablename__ = "sensor_translation"
    __table_args__ = (
        PrimaryKeyConstraint("sensor_id", name="sensor_translation_pkey"),
    )

    sensor_id: Mapped[str] = mapped_column(Text, primary_key=True)
    display_name: Mapped[str] = mapped_column(Text, nullable=False)
    unit: Mapped[str | None] = mapped_column(Text)
