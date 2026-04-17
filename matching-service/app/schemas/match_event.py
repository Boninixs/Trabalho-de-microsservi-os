from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.match_suggestion import MatchStatus
from app.schemas.events import EventEnvelope


class MatchEventPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lost_item_id: UUID
    found_item_id: UUID
    score: int
    criteria_snapshot_json: dict[str, Any]
    status: MatchStatus
    decided_by_user_id: UUID | None
    created_at: datetime
    updated_at: datetime


class MatchSuggestedEnvelope(EventEnvelope):
    event_type: Literal["MatchSuggested"]
    payload: MatchEventPayload


class MatchAcceptedEnvelope(EventEnvelope):
    event_type: Literal["MatchAccepted"]
    payload: MatchEventPayload


class MatchRejectedEnvelope(EventEnvelope):
    event_type: Literal["MatchRejected"]
    payload: MatchEventPayload
