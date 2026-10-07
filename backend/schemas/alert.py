from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AlertCreate(BaseModel):
    facility_id: UUID
    building_id: UUID | None = None
    device_id: UUID | None = None
    alert_type: str
    severity: str
    title: str
    message: str
    status: str = "OPEN"
    detected_at: datetime


class AlertUpdate(BaseModel):
    severity: str | None = None
    title: str | None = None
    message: str | None = None
    status: str | None = None
    resolved_at: datetime | None = None


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    facility_id: UUID
    building_id: UUID | None
    device_id: UUID | None
    alert_type: str
    severity: str
    title: str
    message: str
    status: str
    detected_at: datetime
    resolved_at: datetime | None
    created_at: datetime