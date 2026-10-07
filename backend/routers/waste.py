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
from backend.schemas.waste import WasteCreate, WasteResponse
from backend.services.waste_service import WasteService


router = APIRouter(
    prefix="/waste",
    tags=["Waste"],
)


@router.post(
    "",
    response_model=ApiResponse[WasteResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_waste(
    data: WasteCreate,
    db: Session = Depends(get_db),
):
    waste = WasteService.create(
        db,
        data,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Waste record created successfully",
        data=waste,
    )


@router.get(
    "/facility/{facility_id}",
    response_model=ApiResponse[list[WasteResponse]],
)
def get_waste_by_facility(
    facility_id: UUID,
    db: Session = Depends(get_db),
):
    waste = WasteService.get_by_facility(
        db,
        facility_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Waste records retrieved successfully",
        data=waste,
    )


@router.get(
    "/building/{building_id}",
    response_model=ApiResponse[list[WasteResponse]],
)
def get_waste_by_building(
    building_id: UUID,
    db: Session = Depends(get_db),
):
    waste = WasteService.get_by_building(
        db,
        building_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Waste records retrieved successfully",
        data=waste,
    )


@router.get(
    "/device/{device_id}",
    response_model=ApiResponse[list[WasteResponse]],
)
def get_waste_by_device(
    device_id: UUID,
    db: Session = Depends(get_db),
):
    waste = WasteService.get_by_device(
        db,
        device_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Waste records retrieved successfully",
        data=waste,
    )


@router.get(
    "/type/{waste_type}",
    response_model=ApiResponse[list[WasteResponse]],
)
def get_waste_by_type(
    waste_type: str,
    db: Session = Depends(get_db),
):
    waste = WasteService.get_by_type(
        db,
        waste_type,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Waste records retrieved successfully",
        data=waste,
    )


@router.get(
    "/range/{start_time}/{end_time}",
    response_model=ApiResponse[list[WasteResponse]],
)
def get_waste_by_time_range(
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db),
):
    if start_time > end_time:
        raise ResourceValidationException(
            "start_time must be before end_time"
        )

    waste = WasteService.get_by_time_range(
        db,
        start_time,
        end_time,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Waste records retrieved successfully",
        data=waste,
    )


@router.get(
    "/{waste_id}",
    response_model=ApiResponse[WasteResponse],
)
def get_waste(
    waste_id: UUID,
    db: Session = Depends(get_db),
):
    waste = WasteService.get_by_id(
        db,
        waste_id,
    )

    if waste is None:
        raise ResourceNotFoundException(
            f"Waste record not found: {waste_id}"
        )

    return ApiResponse(
        status="SUCCESS",
        message="Waste record retrieved successfully",
        data=waste,
    )