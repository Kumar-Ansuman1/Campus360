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
from backend.schemas.traffic import TrafficCreate, TrafficResponse
from backend.services.traffic_service import TrafficService


router = APIRouter(
    prefix="/traffic",
    tags=["Traffic"],
)


@router.post(
    "",
    response_model=ApiResponse[TrafficResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_traffic(
    data: TrafficCreate,
    db: Session = Depends(get_db),
):
    traffic = TrafficService.create(
        db,
        data,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Traffic record created successfully",
        data=traffic,
    )


@router.get(
    "/facility/{facility_id}",
    response_model=ApiResponse[list[TrafficResponse]],
)
def get_traffic_by_facility(
    facility_id: UUID,
    db: Session = Depends(get_db),
):
    traffic = TrafficService.get_by_facility(
        db,
        facility_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Traffic records retrieved successfully",
        data=traffic,
    )


@router.get(
    "/building/{building_id}",
    response_model=ApiResponse[list[TrafficResponse]],
)
def get_traffic_by_building(
    building_id: UUID,
    db: Session = Depends(get_db),
):
    traffic = TrafficService.get_by_building(
        db,
        building_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Traffic records retrieved successfully",
        data=traffic,
    )


@router.get(
    "/device/{device_id}",
    response_model=ApiResponse[list[TrafficResponse]],
)
def get_traffic_by_device(
    device_id: UUID,
    db: Session = Depends(get_db),
):
    traffic = TrafficService.get_by_device(
        db,
        device_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Traffic records retrieved successfully",
        data=traffic,
    )


@router.get(
    "/range/{start_time}/{end_time}",
    response_model=ApiResponse[list[TrafficResponse]],
)
def get_traffic_by_time_range(
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db),
):
    if start_time > end_time:
        raise ResourceValidationException(
            "start_time must be before end_time"
        )

    traffic = TrafficService.get_by_time_range(
        db,
        start_time,
        end_time,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Traffic records retrieved successfully",
        data=traffic,
    )


@router.get(
    "/{traffic_id}",
    response_model=ApiResponse[TrafficResponse],
)
def get_traffic(
    traffic_id: UUID,
    db: Session = Depends(get_db),
):
    traffic = TrafficService.get_by_id(
        db,
        traffic_id,
    )

    if traffic is None:
        raise ResourceNotFoundException(
            f"Traffic record not found: {traffic_id}"
        )

    return ApiResponse(
        status="SUCCESS",
        message="Traffic record retrieved successfully",
        data=traffic,
    )