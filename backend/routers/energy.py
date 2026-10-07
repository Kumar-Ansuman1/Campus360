from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.exceptions import (
    ResourceNotFoundException,
    ResourceValidationException,
)
from backend.schemas.common import ApiResponse
from backend.schemas.energy import EnergyCreate, EnergyResponse
from backend.services.energy_service import EnergyService


router = APIRouter(
    prefix="/energy",
    tags=["Energy"],
)


@router.post(
    "",
    response_model=ApiResponse[EnergyResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_energy(
    data: EnergyCreate,
    db: Session = Depends(get_db),
):
    energy = EnergyService.create(
        db,
        data,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Energy record created successfully",
        data=energy,
    )


@router.get(
    "/facility/{facility_id}",
    response_model=ApiResponse[list[EnergyResponse]],
)
def get_energy_by_facility(
    facility_id: UUID,
    db: Session = Depends(get_db),
):
    energy = EnergyService.get_by_facility(
        db,
        facility_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Energy records retrieved successfully",
        data=energy,
    )


@router.get(
    "/building/{building_id}",
    response_model=ApiResponse[list[EnergyResponse]],
)
def get_energy_by_building(
    building_id: UUID,
    db: Session = Depends(get_db),
):
    energy = EnergyService.get_by_building(
        db,
        building_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Energy records retrieved successfully",
        data=energy,
    )


@router.get(
    "/device/{device_id}",
    response_model=ApiResponse[list[EnergyResponse]],
)
def get_energy_by_device(
    device_id: UUID,
    db: Session = Depends(get_db),
):
    energy = EnergyService.get_by_device(
        db,
        device_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Energy records retrieved successfully",
        data=energy,
    )


@router.get(
    "/range/{start_time}/{end_time}",
    response_model=ApiResponse[list[EnergyResponse]],
)
def get_energy_by_time_range(
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db),
):
    if start_time > end_time:
        raise ResourceValidationException(
            "start_time must be before end_time"
        )

    energy = EnergyService.get_by_time_range(
        db,
        start_time,
        end_time,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Energy records retrieved successfully",
        data=energy,
    )


@router.get(
    "/{energy_id}",
    response_model=ApiResponse[EnergyResponse],
)
def get_energy(
    energy_id: UUID,
    db: Session = Depends(get_db),
):
    energy = EnergyService.get_by_id(
        db,
        energy_id,
    )

    if energy is None:
        raise ResourceNotFoundException(
            f"Energy record not found: {energy_id}"
        )

    return ApiResponse(
        status="SUCCESS",
        message="Energy record retrieved successfully",
        data=energy,
    )