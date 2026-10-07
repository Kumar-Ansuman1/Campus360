from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.core.exceptions import DatabaseException
from backend.models.energy import Energy
from backend.schemas.energy import EnergyCreate
from backend.utils.resource_validator import ResourceValidator


class EnergyService:

    @staticmethod
    def create(
        db: Session,
        data: EnergyCreate,
    ) -> Energy:

        ResourceValidator.validate_hierarchy(
            db,
            data.facility_id,
            data.building_id,
            data.device_id,
        )

        energy = Energy(
            facility_id=data.facility_id,
            building_id=data.building_id,
            device_id=data.device_id,
            consumption=data.consumption,
            unit=data.unit,
            recorded_at=data.recorded_at,
        )

        try:
            db.add(energy)
            db.commit()
            db.refresh(energy)

            return energy

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to create energy record"
            ) from exc

    @staticmethod
    def get_by_id(
        db: Session,
        energy_id: UUID,
    ) -> Energy | None:

        statement = select(Energy).where(
            Energy.id == energy_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_by_facility(
        db: Session,
        facility_id: UUID,
    ) -> list[Energy]:

        statement = (
            select(Energy)
            .where(Energy.facility_id == facility_id)
            .order_by(Energy.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_building(
        db: Session,
        building_id: UUID,
    ) -> list[Energy]:

        statement = (
            select(Energy)
            .where(Energy.building_id == building_id)
            .order_by(Energy.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_device(
        db: Session,
        device_id: UUID,
    ) -> list[Energy]:

        statement = (
            select(Energy)
            .where(Energy.device_id == device_id)
            .order_by(Energy.recorded_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_time_range(
        db: Session,
        start_time: datetime,
        end_time: datetime,
    ) -> list[Energy]:

        statement = (
            select(Energy)
            .where(
                Energy.recorded_at >= start_time,
                Energy.recorded_at <= end_time,
            )
            .order_by(Energy.recorded_at.asc())
        )

        return list(db.scalars(statement).all())