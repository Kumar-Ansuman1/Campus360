from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WaterCreate(BaseModel):
    facility_id: UUID
    building_id: UUID
    device_id: UUID
    consumption: float
    unit: str = "L"
    recorded_at: datetime


class WaterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    facility_id: UUID
    building_id: UUID
    device_id: UUID
    consumption: float
    unit: str
    recorded_at: datetime
    created_at: datetime
