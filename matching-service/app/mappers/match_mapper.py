from app.models.match_suggestion import MatchSuggestion
from app.schemas.match import MatchResponse
from app.schemas.match_event import MatchEventPayload


def to_match_response(match: MatchSuggestion) -> MatchResponse:
    return MatchResponse.model_validate(match)


def to_match_event_payload(match: MatchSuggestion) -> MatchEventPayload:
    return MatchEventPayload.model_validate(match)

