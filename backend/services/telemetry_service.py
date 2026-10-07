from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.core.exceptions import DatabaseException
from backend.models.telemetry import Telemetry
from backend.schemas.telemetry import TelemetryCreate
from backend.utils.resource_validator import ResourceValidator


class TelemetryService:

    @staticmethod
    def create(
        db: Session,
        data: TelemetryCreate,
    ) -> Telemetry:

        ResourceValidator.validate_device(
            db,
            data.device_id,
        )

        telemetry = Telemetry(
            device_id=data.device_id,
            metric=data.metric,
            value=data.value,
            unit=data.unit,
            timestamp=data.timestamp,
        )

        try:
            db.add(telemetry)
            db.commit()
            db.refresh(telemetry)

            return telemetry

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to create telemetry record"
            ) from exc

    @staticmethod
    def get_by_id(
        db: Session,
        telemetry_id: UUID,
    ) -> Telemetry | None:

        statement = select(Telemetry).where(
            Telemetry.id == telemetry_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_by_device(
        db: Session,
        device_id: UUID,
    ) -> list[Telemetry]:

        statement = (
            select(Telemetry)
            .where(Telemetry.device_id == device_id)
            .order_by(Telemetry.timestamp.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_metric(
        db: Session,
        metric: str,
    ) -> list[Telemetry]:

        statement = (
            select(Telemetry)
            .where(Telemetry.metric == metric)
            .order_by(Telemetry.timestamp.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_time_range(
        db: Session,
        start_time: datetime,
        end_time: datetime,
    ) -> list[Telemetry]:

        statement = (
            select(Telemetry)
            .where(
                Telemetry.timestamp >= start_time,
                Telemetry.timestamp <= end_time,
            )
            .order_by(Telemetry.timestamp.desc())
        )

        return list(db.scalars(statement).all())