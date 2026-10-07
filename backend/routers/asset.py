from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.exceptions import ResourceNotFoundException
from backend.schemas.asset import (
    AssetCreate,
    AssetResponse,
    AssetUpdate,
)
from backend.schemas.common import ApiResponse
from backend.services.asset_service import AssetService


router = APIRouter(
    prefix="/assets",
    tags=["Assets"],
)


@router.post(
    "",
    response_model=ApiResponse[AssetResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_asset(
    data: AssetCreate,
    db: Session = Depends(get_db),
):
    asset = AssetService.create(db, data)

    return ApiResponse(
        status="SUCCESS",
        message="Asset created successfully",
        data=asset,
    )


@router.get(
    "",
    response_model=ApiResponse[list[AssetResponse]],
)
def get_assets(
    db: Session = Depends(get_db),
):
    assets = AssetService.get_all(db)

    return ApiResponse(
        status="SUCCESS",
        message="Assets retrieved successfully",
        data=assets,
    )


@router.get(
    "/facility/{facility_id}",
    response_model=ApiResponse[list[AssetResponse]],
)
def get_assets_by_facility(
    facility_id: UUID,
    db: Session = Depends(get_db),
):
    assets = AssetService.get_by_facility(db, facility_id)

    return ApiResponse(
        status="SUCCESS",
        message="Assets retrieved successfully",
        data=assets,
    )


@router.get(
    "/building/{building_id}",
    response_model=ApiResponse[list[AssetResponse]],
)
def get_assets_by_building(
    building_id: UUID,
    db: Session = Depends(get_db),
):
    assets = AssetService.get_by_building(db, building_id)

    return ApiResponse(
        status="SUCCESS",
        message="Assets retrieved successfully",
        data=assets,
    )


@router.get(
    "/type/{asset_type}",
    response_model=ApiResponse[list[AssetResponse]],
)
def get_assets_by_type(
    asset_type: str,
    db: Session = Depends(get_db),
):
    assets = AssetService.get_by_type(db, asset_type)

    return ApiResponse(
        status="SUCCESS",
        message="Assets retrieved successfully",
        data=assets,
    )


@router.get(
    "/{asset_id}",
    response_model=ApiResponse[AssetResponse],
)
def get_asset(
    asset_id: UUID,
    db: Session = Depends(get_db),
):
    asset = AssetService.get_by_id(db, asset_id)

    if asset is None:
        raise ResourceNotFoundException(
            f"Asset not found: {asset_id}"
        )

    return ApiResponse(
        status="SUCCESS",
        message="Asset retrieved successfully",
        data=asset,
    )


@router.put(
    "/{asset_id}",
    response_model=ApiResponse[AssetResponse],
)
def update_asset(
    asset_id: UUID,
    data: AssetUpdate,
    db: Session = Depends(get_db),
):
    asset = AssetService.get_by_id(db, asset_id)

    if asset is None:
        raise ResourceNotFoundException(
            f"Asset not found: {asset_id}"
        )

    updated_asset = AssetService.update(db, asset, data)

    return ApiResponse(
        status="SUCCESS",
        message="Asset updated successfully",
        data=updated_asset,
    )


@router.delete(
    "/{asset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_asset(
    asset_id: UUID,
    db: Session = Depends(get_db),
):
    asset = AssetService.get_by_id(db, asset_id)

    if asset is None:
        raise ResourceNotFoundException(
            f"Asset not found: {asset_id}"
        )

    AssetService.delete(db, asset)