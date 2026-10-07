from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.exceptions import ResourceNotFoundException
from backend.schemas.common import ApiResponse
from backend.schemas.facility import (
    FacilityCreate,
    FacilityResponse,
    FacilityUpdate,
)
from backend.services.facility_service import FacilityService


router = APIRouter(
    prefix="/facilities",
    tags=["Facilities"],
)


@router.post(
    "",
    response_model=ApiResponse[FacilityResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_facility(
    data: FacilityCreate,
    db: Session = Depends(get_db),
):
    facility = FacilityService.create(db, data)

    return ApiResponse(
        status="SUCCESS",
        message="Facility created successfully",
        data=facility,
    )


@router.get(
    "",
    response_model=ApiResponse[list[FacilityResponse]],
)
def get_facilities(
    db: Session = Depends(get_db),
):
    facilities = FacilityService.get_all(db)

    return ApiResponse(
        status="SUCCESS",
        message="Facilities retrieved successfully",
        data=facilities,
    )


@router.get(
    "/{facility_id}",
    response_model=ApiResponse[FacilityResponse],
)
def get_facility(
    facility_id: UUID,
    db: Session = Depends(get_db),
):
    facility = FacilityService.get_by_id(db, facility_id)

    if facility is None:
        raise ResourceNotFoundException(
            f"Facility not found: {facility_id}"
        )

    return ApiResponse(
        status="SUCCESS",
        message="Facility retrieved successfully",
        data=facility,
    )


@router.put(
    "/{facility_id}",
    response_model=ApiResponse[FacilityResponse],
)
def update_facility(
    facility_id: UUID,
    data: FacilityUpdate,
    db: Session = Depends(get_db),
):
    facility = FacilityService.get_by_id(db, facility_id)

    if facility is None:
        raise ResourceNotFoundException(
            f"Facility not found: {facility_id}"
        )

    updated_facility = FacilityService.update(
        db,
        facility,
        data,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Facility updated successfully",
        data=updated_facility,
    )


@router.delete(
    "/{facility_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_facility(
    facility_id: UUID,
    db: Session = Depends(get_db),
):
    facility = FacilityService.get_by_id(db, facility_id)

    if facility is None:
        raise ResourceNotFoundException(
            f"Facility not found: {facility_id}"
        )

    FacilityService.delete(db, facility)