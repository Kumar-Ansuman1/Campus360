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
from backend.schemas.telemetry import (
    TelemetryCreate,
    TelemetryResponse,
)
from backend.services.telemetry_service import TelemetryService


router = APIRouter(
    prefix="/telemetry",
    tags=["Telemetry"],
)


@router.post(
    "",
    response_model=ApiResponse[TelemetryResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_telemetry(
    data: TelemetryCreate,
    db: Session = Depends(get_db),
):
    telemetry = TelemetryService.create(
        db,
        data,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Telemetry created successfully",
        data=telemetry,
    )


@router.get(
    "/device/{device_id}",
    response_model=ApiResponse[list[TelemetryResponse]],
)
def get_telemetry_by_device(
    device_id: UUID,
    db: Session = Depends(get_db),
):
    telemetry = TelemetryService.get_by_device(
        db,
        device_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Telemetry records retrieved successfully",
        data=telemetry,
    )


@router.get(
    "/metric/{metric}",
    response_model=ApiResponse[list[TelemetryResponse]],
)
def get_telemetry_by_metric(
    metric: str,
    db: Session = Depends(get_db),
):
    telemetry = TelemetryService.get_by_metric(
        db,
        metric,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Telemetry records retrieved successfully",
        data=telemetry,
    )


@router.get(
    "/context/building/{building_id}",
    response_model=ApiResponse[list[TelemetryResponse]],
)
def get_context_telemetry_by_building(
    building_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Return context telemetry for a building.

    This endpoint is consumed by the AI optimization layer.
    """

    telemetry = TelemetryService.get_context_by_building(
        db,
        building_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Context telemetry retrieved successfully",
        data=telemetry,
    )


@router.get(
    "/range/{start_time}/{end_time}",
    response_model=ApiResponse[list[TelemetryResponse]],
)
def get_telemetry_by_time_range(
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db),
):
    if start_time > end_time:
        raise ResourceValidationException(
            "start_time must be before end_time"
        )

    telemetry = TelemetryService.get_by_time_range(
        db,
        start_time,
        end_time,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Telemetry records retrieved successfully",
        data=telemetry,
    )


@router.get(
    "/{telemetry_id}",
    response_model=ApiResponse[TelemetryResponse],
)
def get_telemetry(
    telemetry_id: UUID,
    db: Session = Depends(get_db),
):
    telemetry = TelemetryService.get_by_id(
        db,
        telemetry_id,
    )

    if telemetry is None:
        raise ResourceNotFoundException(
            f"Telemetry record not found: {telemetry_id}"
        )

    return ApiResponse(
        status="SUCCESS",
        message="Telemetry record retrieved successfully",
        data=telemetry,
    )