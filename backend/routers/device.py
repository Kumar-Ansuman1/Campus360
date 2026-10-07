from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.exceptions import ResourceNotFoundException
from backend.schemas.common import ApiResponse
from backend.schemas.device import (
    DeviceCreate,
    DeviceResponse,
    DeviceUpdate,
)
from backend.services.device_service import DeviceService


router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


@router.post(
    "",
    response_model=ApiResponse[DeviceResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_device(
    data: DeviceCreate,
    db: Session = Depends(get_db),
):
    device = DeviceService.create(
        db,
        data,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Device created successfully",
        data=device,
    )


@router.get(
    "",
    response_model=ApiResponse[list[DeviceResponse]],
)
def get_devices(
    db: Session = Depends(get_db),
):
    devices = DeviceService.get_all(db)

    return ApiResponse(
        status="SUCCESS",
        message="Devices retrieved successfully",
        data=devices,
    )


@router.get(
    "/building/{building_id}",
    response_model=ApiResponse[list[DeviceResponse]],
)
def get_devices_by_building(
    building_id: UUID,
    db: Session = Depends(get_db),
):
    devices = DeviceService.get_by_building(
        db,
        building_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Devices retrieved successfully",
        data=devices,
    )


@router.get(
    "/category/{category}",
    response_model=ApiResponse[list[DeviceResponse]],
)
def get_devices_by_category(
    category: str,
    db: Session = Depends(get_db),
):
    devices = DeviceService.get_by_category(
        db,
        category,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Devices retrieved successfully",
        data=devices,
    )


@router.get(
    "/{device_id}",
    response_model=ApiResponse[DeviceResponse],
)
def get_device(
    device_id: UUID,
    db: Session = Depends(get_db),
):
    device = DeviceService.get_by_id(
        db,
        device_id,
    )

    if device is None:
        raise ResourceNotFoundException(
            f"Device not found: {device_id}"
        )

    return ApiResponse(
        status="SUCCESS",
        message="Device retrieved successfully",
        data=device,
    )


@router.put(
    "/{device_id}",
    response_model=ApiResponse[DeviceResponse],
)
def update_device(
    device_id: UUID,
    data: DeviceUpdate,
    db: Session = Depends(get_db),
):
    device = DeviceService.get_by_id(
        db,
        device_id,
    )

    if device is None:
        raise ResourceNotFoundException(
            f"Device not found: {device_id}"
        )

    updated_device = DeviceService.update(
        db,
        device,
        data,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Device updated successfully",
        data=updated_device,
    )


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_device(
    device_id: UUID,
    db: Session = Depends(get_db),
):
    device = DeviceService.get_by_id(
        db,
        device_id,
    )

    if device is None:
        raise ResourceNotFoundException(
            f"Device not found: {device_id}"
        )

    DeviceService.delete(
        db,
        device,
    )