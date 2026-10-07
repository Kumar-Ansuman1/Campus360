from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FacilityCreate(BaseModel):
    facility_code: str
    name: str
    location: str | None = None
    city: str
    state: str
    country: str


class FacilityUpdate(BaseModel):
    facility_code: str | None = None
    name: str | None = None
    location: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None


class FacilityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    facility_code: str
    name: str
    location: str | None
    city: str
    state: str
    country: str
    created_at: datetime
    updated_at: datetime