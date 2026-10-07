from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.core.exceptions import DatabaseException
from backend.models.water import Water
from backend.schemas.water import WaterCreate
from backend.utils.resource_validator import ResourceValidator


class WaterService:

    @staticmethod
    def create(
        db: Session,
        data: WaterCreate,
    ) -> Water:

        # Validate Facility → Building → Device hierarchy
        ResourceValidator.validate_hierarchy(
            db,
            data.facility_id,
            data.building_id,
            data.device_id,
        )

        water = Water(
            facility_id=data.facility_id,
            building_id=data.building_id,
            device_id=data.device_id,
            consumption=data.consumption,
            unit=data.unit,
            recorded_at=data.recorded_at,
        )

        try:
            db.add(water)
            db.commit()
            db.refresh(water)

            return water

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to create water record"
            ) from exc

    @staticmethod
    def get_by_id(
        db: Session,
        water_id: UUID,
    ) -> Water | None:

        statement = select(Water).where(
            Water.id == water_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_by_facility(
        db: Session,
        facility_id: UUID,
    ) -> list[Water]:

        statement = (
            select(Water)
            .where(Water.facility_id == facility_id)
            .order_by(Water.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_building(
        db: Session,
        building_id: UUID,
    ) -> list[Water]:

        statement = (
            select(Water)
            .where(Water.building_id == building_id)
            .order_by(Water.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_device(
        db: Session,
        device_id: UUID,
    ) -> list[Water]:

        statement = (
            select(Water)
            .where(Water.device_id == device_id)
            .order_by(Water.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_time_range(
        db: Session,
        start_time: datetime,
        end_time: datetime,
    ) -> list[Water]:

        statement = (
            select(Water)
            .where(
                Water.recorded_at >= start_time,
                Water.recorded_at <= end_time,
            )
            .order_by(Water.recorded_at.asc())
        )

        return list(db.scalars(statement).all())