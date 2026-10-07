from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.core.exceptions import DatabaseException
from backend.models.traffic import Traffic
from backend.schemas.traffic import TrafficCreate
from backend.utils.resource_validator import ResourceValidator


class TrafficService:

    @staticmethod
    def create(
        db: Session,
        data: TrafficCreate,
    ) -> Traffic:

        # Validate Facility → Building → Device hierarchy
        ResourceValidator.validate_hierarchy(
            db,
            data.facility_id,
            data.building_id,
            data.device_id,
        )

        traffic = Traffic(
            facility_id=data.facility_id,
            building_id=data.building_id,
            device_id=data.device_id,
            vehicle_count=data.vehicle_count,
            parking_occupancy=data.parking_occupancy,
            average_speed=data.average_speed,
            recorded_at=data.recorded_at,
        )

        try:
            db.add(traffic)
            db.commit()
            db.refresh(traffic)

            return traffic

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to create traffic record"
            ) from exc

    @staticmethod
    def get_by_id(
        db: Session,
        traffic_id: UUID,
    ) -> Traffic | None:

        statement = select(Traffic).where(
            Traffic.id == traffic_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_by_facility(
        db: Session,
        facility_id: UUID,
    ) -> list[Traffic]:

        statement = (
            select(Traffic)
            .where(Traffic.facility_id == facility_id)
            .order_by(Traffic.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_building(
        db: Session,
        building_id: UUID,
    ) -> list[Traffic]:

        statement = (
            select(Traffic)
            .where(Traffic.building_id == building_id)
            .order_by(Traffic.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_device(
        db: Session,
        device_id: UUID,
    ) -> list[Traffic]:

        statement = (
            select(Traffic)
            .where(Traffic.device_id == device_id)
            .order_by(Traffic.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_time_range(
        db: Session,
        start_time: datetime,
        end_time: datetime,
    ) -> list[Traffic]:

        statement = (
            select(Traffic)
            .where(
                Traffic.recorded_at >= start_time,
                Traffic.recorded_at <= end_time,
            )
            .order_by(Traffic.recorded_at.asc())
        )

        return list(db.scalars(statement).all())