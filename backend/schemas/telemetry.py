from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TelemetryCreate(BaseModel):
    device_id: UUID
    metric: str
    value: float
    unit: str
    timestamp: datetime


class TelemetryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    device_id: UUID
    metric: str
    value: float
    unit: str
    timestamp: datetime
    created_at: datetime