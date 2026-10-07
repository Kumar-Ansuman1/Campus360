import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base


class AirQuality(Base):
    __tablename__ = "air_quality_records"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    facility_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("facilities.id"),
        nullable=False,
        index=True,
    )

    building_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("buildings.id"),
        nullable=False,
        index=True,
    )

    device_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("devices.id"),
        nullable=False,
        index=True,
    )

    pm25: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    pm10: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    co2: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    temperature: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    humidity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    aqi: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )