from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from backend.core.exceptions import (
    DatabaseException,
    ResourceConflictException,
)
from backend.models.facility import Facility
from backend.schemas.facility import FacilityCreate, FacilityUpdate


class FacilityService:

    @staticmethod
    def create(
        db: Session,
        data: FacilityCreate,
    ) -> Facility:

        facility = Facility(
            facility_code=data.facility_code,
            name=data.name,
            location=data.location,
            city=data.city,
            state=data.state,
            country=data.country,
        )

        try:
            db.add(facility)
            db.commit()
            db.refresh(facility)

            return facility

        except IntegrityError as exc:
            db.rollback()
            raise ResourceConflictException(
                f"Facility code already exists: {data.facility_code}"
            ) from exc

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to create facility"
            ) from exc

    @staticmethod
    def get_by_id(
        db: Session,
        facility_id: UUID,
    ) -> Facility | None:

        statement = select(Facility).where(
            Facility.id == facility_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Facility]:

        statement = select(Facility).order_by(
            Facility.created_at.desc()
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def update(
        db: Session,
        facility: Facility,
        data: FacilityUpdate,
    ) -> Facility:

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(facility, field, value)

        try:
            db.commit()
            db.refresh(facility)

            return facility

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to update facility"
            ) from exc

    @staticmethod
    def delete(
        db: Session,
        facility: Facility,
    ) -> None:

        try:
            db.delete(facility)
            db.commit()

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to delete facility"
            ) from exc