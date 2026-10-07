from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BuildingCreate(BaseModel):
    building_code: str
    facility_id: UUID
    name: str
    building_type: str
    floor_count: int | None = None
    area_sq_m: float | None = None


class BuildingUpdate(BaseModel):
    building_code: str | None = None
    facility_id: UUID | None = None
    name: str | None = None
    building_type: str | None = None
    floor_count: int | None = None
    area_sq_m: float | None = None


class BuildingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    building_code: str
    facility_id: UUID
    name: str
    building_type: str
    floor_count: int | None
    area_sq_m: float | None
    created_at: datetime
    updated_at: datetime