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
from backend.schemas.water import WaterCreate, WaterResponse
from backend.services.water_service import WaterService


router = APIRouter(
    prefix="/water",
    tags=["Water"],
)


@router.post(
    "",
    response_model=ApiResponse[WaterResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_water(
    data: WaterCreate,
    db: Session = Depends(get_db),
):
    water = WaterService.create(
        db,
        data,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Water record created successfully",
        data=water,
    )


@router.get(
    "/facility/{facility_id}",
    response_model=ApiResponse[list[WaterResponse]],
)
def get_water_by_facility(
    facility_id: UUID,
    db: Session = Depends(get_db),
):
    water = WaterService.get_by_facility(
        db,
        facility_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Water records retrieved successfully",
        data=water,
    )


@router.get(
    "/building/{building_id}",
    response_model=ApiResponse[list[WaterResponse]],
)
def get_water_by_building(
    building_id: UUID,
    db: Session = Depends(get_db),
):
    water = WaterService.get_by_building(
        db,
        building_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Water records retrieved successfully",
        data=water,
    )


@router.get(
    "/device/{device_id}",
    response_model=ApiResponse[list[WaterResponse]],
)
def get_water_by_device(
    device_id: UUID,
    db: Session = Depends(get_db),
):
    water = WaterService.get_by_device(
        db,
        device_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Water records retrieved successfully",
        data=water,
    )


@router.get(
    "/range/{start_time}/{end_time}",
    response_model=ApiResponse[list[WaterResponse]],
)
def get_water_by_time_range(
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db),
):
    if start_time > end_time:
        raise ResourceValidationException(
            "start_time must be before end_time"
        )

    water = WaterService.get_by_time_range(
        db,
        start_time,
        end_time,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Water records retrieved successfully",
        data=water,
    )


@router.get(
    "/{water_id}",
    response_model=ApiResponse[WaterResponse],
)
def get_water(
    water_id: UUID,
    db: Session = Depends(get_db),
):
    water = WaterService.get_by_id(
        db,
        water_id,
    )

    if water is None:
        raise ResourceNotFoundException(
            f"Water record not found: {water_id}"
        )

    return ApiResponse(
        status="SUCCESS",
        message="Water record retrieved successfully",
        data=water,
    )