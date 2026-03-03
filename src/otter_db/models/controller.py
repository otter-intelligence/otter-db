from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Double,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ControllerHealthMetric(Base):
    __tablename__ = "controller_health_metrics"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="controller_health_metrics_pkey"),
        UniqueConstraint("timestamp", name="controller_health_metrics_timestamp_key"),
        Index("idx_controller_health_status", "health_status", postgresql_include=[]),
        Index(
            "idx_controller_health_timestamp",
            text("timestamp DESC"),
            postgresql_include=[],
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(True), nullable=False)
    total_samples: Mapped[int | None] = mapped_column(Integer)
    valid_samples: Mapped[int | None] = mapped_column(Integer)
    invalid_sensor_pct: Mapped[float | None] = mapped_column(Double(53))
    fb_saturated_pct: Mapped[float | None] = mapped_column(Double(53))
    mean_error: Mapped[float | None] = mapped_column(Double(53))
    std_error: Mapped[float | None] = mapped_column(Double(53))
    mean_fb_trim: Mapped[float | None] = mapped_column(Double(53))
    mean_total_dosage: Mapped[float | None] = mapped_column(Double(53))
    min_total_dosage: Mapped[float | None] = mapped_column(Double(53))
    max_total_dosage: Mapped[float | None] = mapped_column(Double(53))
    health_status: Mapped[str | None] = mapped_column(Text)
    rmse_to_setpoint: Mapped[float | None] = mapped_column(Double(53))
    time_above_setpoint_pct: Mapped[float | None] = mapped_column(Double(53))
    exceedance_severity: Mapped[float | None] = mapped_column(Double(53))
    effluent_variability_mad: Mapped[float | None] = mapped_column(Double(53))
    sign_changes_total: Mapped[int | None] = mapped_column(Integer)
    sign_changes_per_hour: Mapped[float | None] = mapped_column(Double(53))
    avg_d_ff: Mapped[float | None] = mapped_column(Double(53))
    avg_d_fb: Mapped[float | None] = mapped_column(Double(53))
    avg_d_total: Mapped[float | None] = mapped_column(Double(53))
    avg_d_polymer_rounded: Mapped[float | None] = mapped_column(Double(53))
    dose_variability_mad: Mapped[float | None] = mapped_column(Double(53))
    fb_contribution_ratio: Mapped[float | None] = mapped_column(Double(53))
    integral_drift: Mapped[float | None] = mapped_column(Double(53))
    windup_during_saturation: Mapped[float | None] = mapped_column(Double(53))
    ff_sensitivity_corr: Mapped[float | None] = mapped_column(Double(53))
    residual_correlation: Mapped[float | None] = mapped_column(Double(53))
    ff_saturated_pct: Mapped[float | None] = mapped_column(Double(53))
    ff_saturated_max_pct: Mapped[float | None] = mapped_column(Double(53))
    ff_saturated_min_pct: Mapped[float | None] = mapped_column(Double(53))
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(True), server_default=text("now()")
    )


class ControllerHeartbeat(Base):
    __tablename__ = "controller_heartbeat"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="controller_heartbeat_pkey"),
        UniqueConstraint("timestamp", name="controller_heartbeat_timestamp_key"),
        Index("idx_controller_heartbeat_run_id", "run_id", postgresql_include=[]),
        Index(
            "idx_controller_heartbeat_timestamp",
            text("timestamp DESC"),
            postgresql_include=[],
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(True), nullable=False)
    run_id: Mapped[str | None] = mapped_column(String(255))
    samples_processed: Mapped[int | None] = mapped_column(Integer)
    execution_duration_ms: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(True), server_default=text("now()")
    )


class ControllerOutput(Base):
    __tablename__ = "controller_output"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="controller_output_pkey"),
        UniqueConstraint("timestamp", name="controller_output_timestamp_key"),
        Index(
            "idx_controller_output_created_at",
            text("created_at DESC"),
            postgresql_include=[],
        ),
        Index(
            "idx_controller_output_saturated",
            "output_saturated",
            postgresql_include=[],
            postgresql_where="(output_saturated = true)",
        ),
        Index(
            "idx_controller_output_sensors_valid",
            "all_sensors_valid",
            postgresql_include=[],
        ),
        Index(
            "idx_controller_output_timestamp",
            text("timestamp DESC"),
            postgresql_include=[],
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(True), nullable=False)
    d_coag_ff: Mapped[float] = mapped_column(Double(53), nullable=False)
    d_coag_total: Mapped[float] = mapped_column(Double(53), nullable=False)
    ntu_in: Mapped[float | None] = mapped_column(Double(53))
    ntu_in_filtered: Mapped[float | None] = mapped_column(Double(53))
    ntu_eff: Mapped[float | None] = mapped_column(Double(53))
    ntu_eff_filtered: Mapped[float | None] = mapped_column(Double(53))
    flow: Mapped[float | None] = mapped_column(Double(53))
    d_fb_trim: Mapped[float | None] = mapped_column(
        Double(53), server_default=text("0.0")
    )
    d_coag_total_rounded: Mapped[float | None] = mapped_column(Double(53))
    d_polymer: Mapped[float | None] = mapped_column(
        Double(53), server_default=text("0.0")
    )
    d_polymer_rounded: Mapped[float | None] = mapped_column(
        Double(53), server_default=text("0.0")
    )
    all_sensors_valid: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("true")
    )
    pH: Mapped[float | None] = mapped_column(Double(53))
    SAX: Mapped[float | None] = mapped_column(Double(53))
    PAX: Mapped[float | None] = mapped_column(Double(53))
    sax_pax_ratio: Mapped[float | None] = mapped_column(Double(53))
    setpoint: Mapped[float | None] = mapped_column(Double(53))
    error: Mapped[float | None] = mapped_column(Double(53))
    proportional: Mapped[float | None] = mapped_column(Double(53))
    integral: Mapped[float | None] = mapped_column(Double(53))
    antiwindup_correction: Mapped[float | None] = mapped_column(Double(53))
    pi_output_unconstrained: Mapped[float | None] = mapped_column(Double(53))
    min_constraint: Mapped[float | None] = mapped_column(Double(53))
    max_constraint: Mapped[float | None] = mapped_column(Double(53))
    output_saturated: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("false")
    )
    sat_fb_trim: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("false")
    )
    sat_step_change: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("false")
    )
    sat_max_int: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("false")
    )
    sat_max_dos: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("false")
    )
    kp: Mapped[float | None] = mapped_column(Double(53))
    theta: Mapped[float | None] = mapped_column(Double(53))
    tau: Mapped[float | None] = mapped_column(Double(53))
    lambda_: Mapped[float | None] = mapped_column("lambda", Double(53))
    sp_ntu_eff: Mapped[float | None] = mapped_column(Double(53))
    kc: Mapped[float | None] = mapped_column(Double(53))
    ti: Mapped[float | None] = mapped_column(Double(53))
    kaw: Mapped[float | None] = mapped_column(Double(53))
    model_type: Mapped[str | None] = mapped_column(String(20))
    d_coag_ff_min: Mapped[float | None] = mapped_column(Double(53))
    d_coag_ff_max: Mapped[float | None] = mapped_column(Double(53))
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(True), server_default=text("now()")
    )
    startup_phase: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("false")
    )
    startup_lookback_minutes: Mapped[float | None] = mapped_column(Double(53))
    minutes_since_flow_turned_on: Mapped[float | None] = mapped_column(Double(53))
