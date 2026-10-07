from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.core.exceptions import DatabaseException
from backend.models.alert import Alert
from backend.schemas.alert import AlertCreate, AlertUpdate
from backend.utils.resource_validator import ResourceValidator


class AlertService:

    @staticmethod
    def create(
        db: Session,
        data: AlertCreate,
    ) -> Alert:

        # Validate Facility → Building → Device relationships
        ResourceValidator.validate_alert_relationships(
            db,
            data.facility_id,
            data.building_id,
            data.device_id,
        )

        alert = Alert(
            facility_id=data.facility_id,
            building_id=data.building_id,
            device_id=data.device_id,
            alert_type=data.alert_type,
            severity=data.severity,
            title=data.title,
            message=data.message,
            status=data.status,
            detected_at=data.detected_at,
        )

        try:
            db.add(alert)
            db.commit()
            db.refresh(alert)

            return alert

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to create alert"
            ) from exc

    @staticmethod
    def get_by_id(
        db: Session,
        alert_id: UUID,
    ) -> Alert | None:

        statement = select(Alert).where(
            Alert.id == alert_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Alert]:

        statement = select(Alert).order_by(
            Alert.detected_at.desc()
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_facility(
        db: Session,
        facility_id: UUID,
    ) -> list[Alert]:

        statement = (
            select(Alert)
            .where(Alert.facility_id == facility_id)
            .order_by(Alert.detected_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_status(
        db: Session,
        status: str,
    ) -> list[Alert]:

        statement = (
            select(Alert)
            .where(Alert.status == status)
            .order_by(Alert.detected_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_severity(
        db: Session,
        severity: str,
    ) -> list[Alert]:

        statement = (
            select(Alert)
            .where(Alert.severity == severity)
            .order_by(Alert.detected_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def update(
        db: Session,
        alert: Alert,
        data: AlertUpdate,
    ) -> Alert:

        update_data = data.model_dump(
            exclude_unset=True
        )

        # Determine the final relationship values
        # after applying this update.
        facility_id = update_data.get(
            "facility_id",
            alert.facility_id,
        )

        building_id = update_data.get(
            "building_id",
            alert.building_id,
        )

        device_id = update_data.get(
            "device_id",
            alert.device_id,
        )

        # Validate the resulting Facility → Building → Device hierarchy.
        ResourceValidator.validate_alert_relationships(
            db,
            facility_id,
            building_id,
            device_id,
        )

        for field, value in update_data.items():
            setattr(alert, field, value)

        try:
            db.commit()
            db.refresh(alert)

            return alert

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to update alert"
            ) from exc

    @staticmethod
    def resolve(
        db: Session,
        alert: Alert,
    ) -> Alert:

        alert.status = "RESOLVED"
        alert.resolved_at = datetime.utcnow()

        try:
            db.commit()
            db.refresh(alert)

            return alert

        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseException(
                "Failed to resolve alert"
            ) from exc