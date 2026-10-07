from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RecommendationCreate(BaseModel):
    facility_id: UUID
    building_id: UUID | None = None
    device_id: UUID | None = None
    alert_id: UUID | None = None
    recommendation_type: str
    priority: str
    title: str
    description: str
    status: str = "PENDING"


class RecommendationUpdate(BaseModel):
    recommendation_type: str | None = None
    priority: str | None = None
    title: str | None = None
    description: str | None = None
    status: str | None = None


class RecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    facility_id: UUID
    building_id: UUID | None
    device_id: UUID | None
    alert_id: UUID | None
    recommendation_type: str
    priority: str
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime