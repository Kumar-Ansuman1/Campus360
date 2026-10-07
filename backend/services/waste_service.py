from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.core.exceptions import DatabaseException
from backend.models.waste import Waste
from backend.schemas.waste import WasteCreate
from backend.utils.resource_validator import ResourceValidator


class WasteService:

    @staticmethod
    def create(
        db: Session,
        data: WasteCreate,
    ) -> Waste:

        # Validate Facility → Building → Device hierarchy
        ResourceValidator.validate_hierarchy(
            db,
            data.facility_id,
            data.building_id,
            data.device_id,
        )

        waste = Waste(
            facility_id=data.facility_id,
            building_id=data.building_id,
            device_id=data.device_id,
            waste_type=data.waste_type,
            quantity=data.quantity,
            unit=data.unit,
            recorded_at=data.recorded_at,
        )

        try:
            db.add(waste)
            db.commit()
            db.refresh(waste)

            return waste

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to create waste record"
            ) from exc

    @staticmethod
    def get_by_id(
        db: Session,
        waste_id: UUID,
    ) -> Waste | None:

        statement = select(Waste).where(
            Waste.id == waste_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_by_facility(
        db: Session,
        facility_id: UUID,
    ) -> list[Waste]:

        statement = (
            select(Waste)
            .where(Waste.facility_id == facility_id)
            .order_by(Waste.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_building(
        db: Session,
        building_id: UUID,
    ) -> list[Waste]:

        statement = (
            select(Waste)
            .where(Waste.building_id == building_id)
            .order_by(Waste.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_device(
        db: Session,
        device_id: UUID,
    ) -> list[Waste]:

        statement = (
            select(Waste)
            .where(Waste.device_id == device_id)
            .order_by(Waste.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_type(
        db: Session,
        waste_type: str,
    ) -> list[Waste]:

        statement = (
            select(Waste)
            .where(Waste.waste_type == waste_type)
            .order_by(Waste.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_time_range(
        db: Session,
        start_time: datetime,
        end_time: datetime,
    ) -> list[Waste]:

        statement = (
            select(Waste)
            .where(
                Waste.recorded_at >= start_time,
                Waste.recorded_at <= end_time,
            )
            .order_by(Waste.recorded_at.asc())
        )

        return list(db.scalars(statement).all())