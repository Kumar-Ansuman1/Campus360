from uuid import UUID

from sqlalchemy.orm import Session

from backend.core.exceptions import (
    ResourceNotFoundException,
    ResourceValidationException,
)
from backend.models.alert import Alert
from backend.models.building import Building
from backend.models.device import Device
from backend.models.facility import Facility


class ResourceValidator:

    @staticmethod
    def validate_facility(
        db: Session,
        facility_id: UUID,
    ) -> Facility:
        facility = db.get(Facility, facility_id)

        if facility is None:
            raise ResourceNotFoundException(
                f"Facility not found: {facility_id}"
            )

        return facility

    @staticmethod
    def validate_building(
        db: Session,
        building_id: UUID,
        facility_id: UUID | None = None,
    ) -> Building:
        building = db.get(Building, building_id)

        if building is None:
            raise ResourceNotFoundException(
                f"Building not found: {building_id}"
            )

        if (
            facility_id is not None
            and building.facility_id != facility_id
        ):
            raise ResourceValidationException(
                "Building does not belong to the specified facility"
            )

        return building

    @staticmethod
    def validate_device(
        db: Session,
        device_id: UUID,
        building_id: UUID | None = None,
    ) -> Device:
        device = db.get(Device, device_id)

        if device is None:
            raise ResourceNotFoundException(
                f"Device not found: {device_id}"
            )

        if (
            building_id is not None
            and device.building_id != building_id
        ):
            raise ResourceValidationException(
                "Device does not belong to the specified building"
            )

        return device

    @staticmethod
    def validate_hierarchy(
        db: Session,
        facility_id: UUID,
        building_id: UUID,
        device_id: UUID,
    ) -> None:
        ResourceValidator.validate_facility(
            db,
            facility_id,
        )

        ResourceValidator.validate_building(
            db,
            building_id,
            facility_id,
        )

        ResourceValidator.validate_device(
            db,
            device_id,
            building_id,
        )

    @staticmethod
    def validate_alert_relationships(
        db: Session,
        facility_id: UUID,
        building_id: UUID | None = None,
        device_id: UUID | None = None,
    ) -> None:
        ResourceValidator.validate_facility(
            db,
            facility_id,
        )

        if building_id is not None:
            ResourceValidator.validate_building(
                db,
                building_id,
                facility_id,
            )

        if device_id is not None:
            ResourceValidator.validate_device(
                db,
                device_id,
                building_id,
            )

    @staticmethod
    def validate_recommendation_relationships(
        db: Session,
        facility_id: UUID,
        building_id: UUID | None = None,
        device_id: UUID | None = None,
        alert_id: UUID | None = None,
    ) -> None:
        ResourceValidator.validate_facility(
            db,
            facility_id,
        )

        if building_id is not None:
            ResourceValidator.validate_building(
                db,
                building_id,
                facility_id,
            )

        if device_id is not None:
            ResourceValidator.validate_device(
                db,
                device_id,
                building_id,
            )

        if alert_id is not None:
            alert = db.get(Alert, alert_id)

            if alert is None:
                raise ResourceNotFoundException(
                    f"Alert not found: {alert_id}"
                )

            if alert.facility_id != facility_id:
                raise ResourceValidationException(
                    "Alert does not belong to the specified facility"
                )