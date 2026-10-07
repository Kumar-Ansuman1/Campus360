from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.core.exceptions import DatabaseException
from backend.models.asset import Asset
from backend.schemas.asset import AssetCreate, AssetUpdate
from backend.utils.resource_validator import ResourceValidator


class AssetService:

    @staticmethod
    def create(
        db: Session,
        data: AssetCreate,
    ) -> Asset:

        # Validate Facility → Building relationship
        ResourceValidator.validate_building(
            db,
            data.building_id,
            data.facility_id,
        )

        asset = Asset(
            facility_id=data.facility_id,
            building_id=data.building_id,
            asset_code=data.asset_code,
            name=data.name,
            asset_type=data.asset_type,
            status=data.status,
            manufacturer=data.manufacturer,
            model_number=data.model_number,
            installed_at=data.installed_at,
        )

        try:
            db.add(asset)
            db.commit()
            db.refresh(asset)

            return asset

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to create asset"
            ) from exc

    @staticmethod
    def get_by_id(
        db: Session,
        asset_id: UUID,
    ) -> Asset | None:

        statement = select(Asset).where(
            Asset.id == asset_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Asset]:

        statement = select(Asset).order_by(
            Asset.created_at.desc()
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_facility(
        db: Session,
        facility_id: UUID,
    ) -> list[Asset]:

        statement = (
            select(Asset)
            .where(Asset.facility_id == facility_id)
            .order_by(Asset.created_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_building(
        db: Session,
        building_id: UUID,
    ) -> list[Asset]:

        statement = (
            select(Asset)
            .where(Asset.building_id == building_id)
            .order_by(Asset.created_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_type(
        db: Session,
        asset_type: str,
    ) -> list[Asset]:

        statement = (
            select(Asset)
            .where(Asset.asset_type == asset_type)
            .order_by(Asset.created_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def update(
        db: Session,
        asset: Asset,
        data: AssetUpdate,
    ) -> Asset:

        update_data = data.model_dump(
            exclude_unset=True
        )

        # Determine the final relationship values
        # after applying this update.
        facility_id = update_data.get(
            "facility_id",
            asset.facility_id,
        )

        building_id = update_data.get(
            "building_id",
            asset.building_id,
        )

        # Validate the final Facility → Building relationship.
        ResourceValidator.validate_building(
            db,
            building_id,
            facility_id,
        )

        for field, value in update_data.items():
            setattr(asset, field, value)

        try:
            db.commit()
            db.refresh(asset)

            return asset

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to update asset"
            ) from exc

    @staticmethod
    def delete(
        db: Session,
        asset: Asset,
    ) -> None:

        try:
            db.delete(asset)
            db.commit()

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to delete asset"
            ) from exc