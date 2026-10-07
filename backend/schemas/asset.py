from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AssetCreate(BaseModel):
    facility_id: UUID
    building_id: UUID
    asset_code: str
    name: str
    asset_type: str
    status: str = "ACTIVE"
    manufacturer: str | None = None
    model_number: str | None = None
    installed_at: date | None = None


class AssetUpdate(BaseModel):
    facility_id: UUID | None = None
    building_id: UUID | None = None
    asset_code: str | None = None
    name: str | None = None
    asset_type: str | None = None
    status: str | None = None
    manufacturer: str | None = None
    model_number: str | None = None
    installed_at: date | None = None


class AssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    facility_id: UUID
    building_id: UUID
    asset_code: str
    name: str
    asset_type: str
    status: str
    manufacturer: str | None
    model_number: str | None
    installed_at: date | None
    created_at: datetime
    updated_at: datetime