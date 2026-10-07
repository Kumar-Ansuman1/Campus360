from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TrafficCreate(BaseModel):
    facility_id: UUID
    building_id: UUID
    device_id: UUID
    vehicle_count: int
    parking_occupancy: float
    average_speed: float | None = None
    recorded_at: datetime


class TrafficResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    facility_id: UUID
    building_id: UUID
    device_id: UUID
    vehicle_count: int
    parking_occupancy: float
    average_speed: float | None
    recorded_at: datetime
    created_at: datetime