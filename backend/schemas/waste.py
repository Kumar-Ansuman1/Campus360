from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WasteCreate(BaseModel):
    facility_id: UUID
    building_id: UUID
    device_id: UUID
    waste_type: str
    quantity: float
    unit: str
    recorded_at: datetime


class WasteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    facility_id: UUID
    building_id: UUID
    device_id: UUID
    waste_type: str
    quantity: float
    unit: str
    recorded_at: datetime
    created_at: datetime