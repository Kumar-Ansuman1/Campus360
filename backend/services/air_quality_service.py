from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.core.exceptions import DatabaseException
from backend.models.air_quality import AirQuality
from backend.schemas.air_quality import AirQualityCreate
from backend.utils.resource_validator import ResourceValidator


class AirQualityService:

    @staticmethod
    def create(
        db: Session,
        data: AirQualityCreate,
    ) -> AirQuality:

        # Validate Facility → Building → Device hierarchy
        ResourceValidator.validate_hierarchy(
            db,
            data.facility_id,
            data.building_id,
            data.device_id,
        )

        air_quality = AirQuality(
            facility_id=data.facility_id,
            building_id=data.building_id,
            device_id=data.device_id,
            pm25=data.pm25,
            pm10=data.pm10,
            co2=data.co2,
            temperature=data.temperature,
            humidity=data.humidity,
            aqi=data.aqi,
            recorded_at=data.recorded_at,
        )

        try:
            db.add(air_quality)
            db.commit()
            db.refresh(air_quality)

            return air_quality

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to create air quality record"
            ) from exc

    @staticmethod
    def get_by_id(
        db: Session,
        air_quality_id: UUID,
    ) -> AirQuality | None:

        statement = select(AirQuality).where(
            AirQuality.id == air_quality_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_by_facility(
        db: Session,
        facility_id: UUID,
    ) -> list[AirQuality]:

        statement = (
            select(AirQuality)
            .where(AirQuality.facility_id == facility_id)
            .order_by(AirQuality.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_building(
        db: Session,
        building_id: UUID,
    ) -> list[AirQuality]:

        statement = (
            select(AirQuality)
            .where(AirQuality.building_id == building_id)
            .order_by(AirQuality.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_device(
        db: Session,
        device_id: UUID,
    ) -> list[AirQuality]:

        statement = (
            select(AirQuality)
            .where(AirQuality.device_id == device_id)
            .order_by(AirQuality.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_time_range(
        db: Session,
        start_time: datetime,
        end_time: datetime,
    ) -> list[AirQuality]:

        statement = (
            select(AirQuality)
            .where(
                AirQuality.recorded_at >= start_time,
                AirQuality.recorded_at <= end_time,
            )
            .order_by(AirQuality.recorded_at.asc())
        )

        return list(db.scalars(statement).all())