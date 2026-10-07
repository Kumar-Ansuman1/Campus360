from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EnergyCreate(BaseModel):
    facility_id: UUID
    building_id: UUID
    device_id: UUID
    consumption: float
    unit: str = "kWh"
    recorded_at: datetime


class EnergyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    facility_id: UUID
    building_id: UUID
    device_id: UUID
    consumption: float
    unit: str
    recorded_at: datetime
    created_at: datetime