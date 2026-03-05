from datetime import datetime

from sqlalchemy import Boolean, DateTime, Double, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CostSaving(Base):
    __tablename__ = "cost_savings"
    __table_args__ = (PrimaryKeyConstraint("datetime", name="cost_savings_pkey"),)

    datetime: Mapped[datetime] = mapped_column(DateTime(True), primary_key=True)
    baseline_cost: Mapped[float] = mapped_column(Double(53), nullable=False)
    optimized_cost: Mapped[float] = mapped_column(Double(53), nullable=False)
    projected: Mapped[bool] = mapped_column(Boolean, nullable=False)
