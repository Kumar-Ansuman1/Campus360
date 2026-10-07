from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.exceptions import ResourceNotFoundException
from backend.schemas.building import (
    BuildingCreate,
    BuildingResponse,
    BuildingUpdate,
)
from backend.schemas.common import ApiResponse
from backend.services.building_service import BuildingService


router = APIRouter(
    prefix="/buildings",
    tags=["Buildings"],
)


@router.post(
    "",
    response_model=ApiResponse[BuildingResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_building(
    data: BuildingCreate,
    db: Session = Depends(get_db),
):
    building = BuildingService.create(
        db,
        data,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Building created successfully",
        data=building,
    )


@router.get(
    "",
    response_model=ApiResponse[list[BuildingResponse]],
)
def get_buildings(
    db: Session = Depends(get_db),
):
    buildings = BuildingService.get_all(db)

    return ApiResponse(
        status="SUCCESS",
        message="Buildings retrieved successfully",
        data=buildings,
    )


@router.get(
    "/facility/{facility_id}",
    response_model=ApiResponse[list[BuildingResponse]],
)
def get_buildings_by_facility(
    facility_id: UUID,
    db: Session = Depends(get_db),
):
    buildings = BuildingService.get_by_facility(
        db,
        facility_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Buildings retrieved successfully",
        data=buildings,
    )


@router.get(
    "/{building_id}",
    response_model=ApiResponse[BuildingResponse],
)
def get_building(
    building_id: UUID,
    db: Session = Depends(get_db),
):
    building = BuildingService.get_by_id(
        db,
        building_id,
    )

    if building is None:
        raise ResourceNotFoundException(
            f"Building not found: {building_id}"
        )

    return ApiResponse(
        status="SUCCESS",
        message="Building retrieved successfully",
        data=building,
    )


@router.put(
    "/{building_id}",
    response_model=ApiResponse[BuildingResponse],
)
def update_building(
    building_id: UUID,
    data: BuildingUpdate,
    db: Session = Depends(get_db),
):
    building = BuildingService.get_by_id(
        db,
        building_id,
    )

    if building is None:
        raise ResourceNotFoundException(
            f"Building not found: {building_id}"
        )

    updated_building = BuildingService.update(
        db,
        building,
        data,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Building updated successfully",
        data=updated_building,
    )


@router.delete(
    "/{building_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_building(
    building_id: UUID,
    db: Session = Depends(get_db),
):
    building = BuildingService.get_by_id(
        db,
        building_id,
    )

    if building is None:
        raise ResourceNotFoundException(
            f"Building not found: {building_id}"
        )

    BuildingService.delete(
        db,
        building,
    )