from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.item_projection import ExternalItemStatus, ItemClassification
from app.schemas.events import EventEnvelope


class ItemEventPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    classification: ItemClassification
    title: str
    description: str
    category: str
    color: str
    location_description: str
    approximate_date: date
    reporter_user_id: UUID
    status: ExternalItemStatus
    version: int
    created_at: datetime
    updated_at: datetime


class ItemCreatedEnvelope(EventEnvelope):
    event_type: Literal["ItemCreated"]
    payload: ItemEventPayload


class ItemUpdatedEnvelope(EventEnvelope):
    event_type: Literal["ItemUpdated"]
    payload: ItemEventPayload
