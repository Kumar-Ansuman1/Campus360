from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.core.exceptions import DatabaseException
from backend.models.device import Device
from backend.schemas.device import DeviceCreate, DeviceUpdate
from backend.utils.resource_validator import ResourceValidator


class DeviceService:

    @staticmethod
    def create(
        db: Session,
        data: DeviceCreate,
    ) -> Device:

        ResourceValidator.validate_building(
            db,
            data.building_id,
        )

        device = Device(
            device_code=data.device_code,
            building_id=data.building_id,
            name=data.name,
            device_type=data.device_type,
            category=data.category,
            unit=data.unit,
            status=data.status,
        )

        try:
            db.add(device)
            db.commit()
            db.refresh(device)

            return device

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to create device"
            ) from exc

    @staticmethod
    def get_by_id(
        db: Session,
        device_id: UUID,
    ) -> Device | None:

        statement = select(Device).where(
            Device.id == device_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Device]:

        statement = select(Device).order_by(
            Device.created_at.desc()
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_building(
        db: Session,
        building_id: UUID,
    ) -> list[Device]:

        statement = (
            select(Device)
            .where(Device.building_id == building_id)
            .order_by(Device.created_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_category(
        db: Session,
        category: str,
    ) -> list[Device]:

        statement = (
            select(Device)
            .where(Device.category == category)
            .order_by(Device.created_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def update(
        db: Session,
        device: Device,
        data: DeviceUpdate,
    ) -> Device:

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "building_id" in update_data:
            ResourceValidator.validate_building(
                db,
                update_data["building_id"],
            )

        for field, value in update_data.items():
            setattr(device, field, value)

        try:
            db.commit()
            db.refresh(device)

            return device

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to update device"
            ) from exc

    @staticmethod
    def delete(
        db: Session,
        device: Device,
    ) -> None:

        try:
            db.delete(device)
            db.commit()

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to delete device"
            ) from exc