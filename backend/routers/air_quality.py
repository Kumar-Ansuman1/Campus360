from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.exceptions import (
    ResourceNotFoundException,
    ResourceValidationException,
)
from backend.schemas.air_quality import (
    AirQualityCreate,
    AirQualityResponse,
)
from backend.schemas.common import ApiResponse
from backend.services.air_quality_service import AirQualityService


router = APIRouter(
    prefix="/air-quality",
    tags=["Air Quality"],
)


@router.post(
    "",
    response_model=ApiResponse[AirQualityResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_air_quality(
    data: AirQualityCreate,
    db: Session = Depends(get_db),
):
    air_quality = AirQualityService.create(db, data)

    return ApiResponse(
        status="SUCCESS",
        message="Air quality record created successfully",
        data=air_quality,
    )


@router.get(
    "/facility/{facility_id}",
    response_model=ApiResponse[list[AirQualityResponse]],
)
def get_air_quality_by_facility(
    facility_id: UUID,
    db: Session = Depends(get_db),
):
    air_quality = AirQualityService.get_by_facility(
        db,
        facility_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Air quality records retrieved successfully",
        data=air_quality,
    )


@router.get(
    "/building/{building_id}",
    response_model=ApiResponse[list[AirQualityResponse]],
)
def get_air_quality_by_building(
    building_id: UUID,
    db: Session = Depends(get_db),
):
    air_quality = AirQualityService.get_by_building(
        db,
        building_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Air quality records retrieved successfully",
        data=air_quality,
    )


@router.get(
    "/device/{device_id}",
    response_model=ApiResponse[list[AirQualityResponse]],
)
def get_air_quality_by_device(
    device_id: UUID,
    db: Session = Depends(get_db),
):
    air_quality = AirQualityService.get_by_device(
        db,
        device_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Air quality records retrieved successfully",
        data=air_quality,
    )


@router.get(
    "/range/{start_time}/{end_time}",
    response_model=ApiResponse[list[AirQualityResponse]],
)
def get_air_quality_by_time_range(
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db),
):
    if start_time > end_time:
        raise ResourceValidationException(
            "start_time must be before end_time"
        )

    air_quality = AirQualityService.get_by_time_range(
        db,
        start_time,
        end_time,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Air quality records retrieved successfully",
        data=air_quality,
    )


@router.get(
    "/{air_quality_id}",
    response_model=ApiResponse[AirQualityResponse],
)
def get_air_quality(
    air_quality_id: UUID,
    db: Session = Depends(get_db),
):
    air_quality = AirQualityService.get_by_id(
        db,
        air_quality_id,
    )

    if air_quality is None:
        raise ResourceNotFoundException(
            f"Air quality record not found: {air_quality_id}"
        )

    return ApiResponse(
        status="SUCCESS",
        message="Air quality record retrieved successfully",
        data=air_quality,
    )