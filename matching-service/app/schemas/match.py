from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.match_suggestion import MatchStatus


class MatchFilters(BaseModel):
    status: MatchStatus | None = None


class MatchDecisionRequest(BaseModel):
    decided_by_user_id: UUID


class MatchResponse(BaseModel):
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
