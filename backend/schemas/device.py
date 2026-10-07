from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DeviceCreate(BaseModel):
    device_code: str
    building_id: UUID
    name: str
    device_type: str
    category: str
    unit: str | None = None
    status: str = "ACTIVE"


class DeviceUpdate(BaseModel):
    device_code: str | None = None
    building_id: UUID | None = None
    name: str | None = None
    device_type: str | None = None
    category: str | None = None
    unit: str | None = None
    status: str | None = None


class DeviceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    device_code: str
    building_id: UUID
    name: str
    device_type: str
    category: str
    unit: str | None
    status: str
    created_at: datetime
    updated_at: datetime