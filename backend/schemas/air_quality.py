from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AirQualityCreate(BaseModel):
    facility_id: UUID
    building_id: UUID
    device_id: UUID
    pm25: float | None = None
    pm10: float | None = None
    co2: float | None = None
    temperature: float | None = None
    humidity: float | None = None
    aqi: float | None = None
    recorded_at: datetime


class AirQualityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    facility_id: UUID
    building_id: UUID
    device_id: UUID
    pm25: float | None
    pm10: float | None
    co2: float | None
    temperature: float | None
    humidity: float | None
    aqi: float | None
    recorded_at: datetime
    created_at: datetime