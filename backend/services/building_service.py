from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.core.exceptions import DatabaseException
from backend.models.building import Building
from backend.schemas.building import BuildingCreate, BuildingUpdate
from backend.utils.resource_validator import ResourceValidator


class BuildingService:

    @staticmethod
    def create(
        db: Session,
        data: BuildingCreate,
    ) -> Building:

        ResourceValidator.validate_facility(
            db,
            data.facility_id,
        )

        building = Building(
            building_code=data.building_code,
            facility_id=data.facility_id,
            name=data.name,
            building_type=data.building_type,
            floor_count=data.floor_count,
            area_sq_m=data.area_sq_m,
        )

        try:
            db.add(building)
            db.commit()
            db.refresh(building)

            return building

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to create building"
            ) from exc

    @staticmethod
    def get_by_id(
        db: Session,
        building_id: UUID,
    ) -> Building | None:

        statement = select(Building).where(
            Building.id == building_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Building]:

        statement = select(Building).order_by(
            Building.created_at.desc()
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_facility(
        db: Session,
        facility_id: UUID,
    ) -> list[Building]:

        statement = (
            select(Building)
            .where(Building.facility_id == facility_id)
            .order_by(Building.created_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def update(
        db: Session,
        building: Building,
        data: BuildingUpdate,
    ) -> Building:

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "facility_id" in update_data:
            ResourceValidator.validate_facility(
                db,
                update_data["facility_id"],
            )

        for field, value in update_data.items():
            setattr(building, field, value)

        try:
            db.commit()
            db.refresh(building)

            return building

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to update building"
            ) from exc

    @staticmethod
    def delete(
        db: Session,
        building: Building,
    ) -> None:

        try:
            db.delete(building)
            db.commit()

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to delete building"
            ) from exc