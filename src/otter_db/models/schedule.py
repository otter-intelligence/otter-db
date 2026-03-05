from datetime import date, time

from sqlalchemy import (
    Date,
    Double,
    Integer,
    PrimaryKeyConstraint,
    String,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class DailyDosingSchedule(Base):
    __tablename__ = "daily_dosing_schedule"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="daily_dosing_schedule_pkey"),
        UniqueConstraint("date", "time_slot", name="unique_date_timeslot"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    day_name: Mapped[str] = mapped_column(String(20), nullable=False)
    time_slot: Mapped[str] = mapped_column(String(20), nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    coagulant_percentage: Mapped[int] = mapped_column(Integer, nullable=False)
    coagulant_mg_per_l: Mapped[float] = mapped_column(Double(53), nullable=False)
    coagulant_l_per_h: Mapped[float] = mapped_column(Double(53), nullable=False)
    polymer_l_per_h: Mapped[float] = mapped_column(Double(53), nullable=False)
    avg_influent_turbidity_ntu: Mapped[float] = mapped_column(
        Double(53), nullable=False
    )
