from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.core.exceptions import DatabaseException
from backend.models.recommendation import Recommendation
from backend.schemas.recommendation import (
    RecommendationCreate,
    RecommendationUpdate,
)
from backend.utils.resource_validator import ResourceValidator


class RecommendationService:

    @staticmethod
    def create(
        db: Session,
        data: RecommendationCreate,
    ) -> Recommendation:

        # Validate Facility → Building → Device
        # and optional Alert relationship
        ResourceValidator.validate_recommendation_relationships(
            db,
            data.facility_id,
            data.building_id,
            data.device_id,
            data.alert_id,
        )

        recommendation = Recommendation(
            facility_id=data.facility_id,
            building_id=data.building_id,
            device_id=data.device_id,
            alert_id=data.alert_id,
            recommendation_type=data.recommendation_type,
            priority=data.priority,
            title=data.title,
            description=data.description,
            status=data.status,
        )

        try:
            db.add(recommendation)
            db.commit()
            db.refresh(recommendation)

            return recommendation

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to create recommendation"
            ) from exc

    @staticmethod
    def get_by_id(
        db: Session,
        recommendation_id: UUID,
    ) -> Recommendation | None:

        statement = select(Recommendation).where(
            Recommendation.id == recommendation_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Recommendation]:

        statement = select(Recommendation).order_by(
            Recommendation.created_at.desc()
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_facility(
        db: Session,
        facility_id: UUID,
    ) -> list[Recommendation]:

        statement = (
            select(Recommendation)
            .where(
                Recommendation.facility_id == facility_id
            )
            .order_by(Recommendation.created_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_alert(
        db: Session,
        alert_id: UUID,
    ) -> list[Recommendation]:

        statement = (
            select(Recommendation)
            .where(
                Recommendation.alert_id == alert_id
            )
            .order_by(Recommendation.created_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_status(
        db: Session,
        status: str,
    ) -> list[Recommendation]:

        statement = (
            select(Recommendation)
            .where(
                Recommendation.status == status
            )
            .order_by(Recommendation.created_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def update(
        db: Session,
        recommendation: Recommendation,
        data: RecommendationUpdate,
    ) -> Recommendation:

        update_data = data.model_dump(
            exclude_unset=True
        )

        # Determine the final relationship values
        # after applying this update.
        facility_id = update_data.get(
            "facility_id",
            recommendation.facility_id,
        )

        building_id = update_data.get(
            "building_id",
            recommendation.building_id,
        )

        device_id = update_data.get(
            "device_id",
            recommendation.device_id,
        )

        alert_id = update_data.get(
            "alert_id",
            recommendation.alert_id,
        )

        # Validate the resulting relationships.
        ResourceValidator.validate_recommendation_relationships(
            db,
            facility_id,
            building_id,
            device_id,
            alert_id,
        )

        for field, value in update_data.items():
            setattr(recommendation, field, value)

        try:
            db.commit()
            db.refresh(recommendation)

            return recommendation

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to update recommendation"
            ) from exc

    @staticmethod
    def delete(
        db: Session,
        recommendation: Recommendation,
    ) -> None:

        try:
            db.delete(recommendation)
            db.commit()

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to delete recommendation"
            ) from exc