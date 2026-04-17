from uuid import UUID

from sqlalchemy import Select, or_, select
from sqlalchemy.orm import Session

from app.models.match_suggestion import MatchStatus, MatchSuggestion


def add_match_suggestion(session: Session, suggestion: MatchSuggestion) -> MatchSuggestion:
    session.add(suggestion)
    return suggestion


def get_match_suggestion_by_id(session: Session, match_id: UUID) -> MatchSuggestion | None:
    return session.get(MatchSuggestion, match_id)


def get_match_suggestion_by_pair(
    session: Session,
    *,
    lost_item_id: UUID,
    found_item_id: UUID,
) -> MatchSuggestion | None:
    statement = (
        select(MatchSuggestion)
        .where(MatchSuggestion.lost_item_id == lost_item_id)
        .where(MatchSuggestion.found_item_id == found_item_id)
    )
    return session.scalar(statement)


def list_match_suggestions(
    session: Session,
    *,
    status: MatchStatus | None = None,
) -> list[MatchSuggestion]:
    statement: Select[tuple[MatchSuggestion]] = select(MatchSuggestion)
    if status is not None:
        statement = statement.where(MatchSuggestion.status == status)

    statement = statement.order_by(MatchSuggestion.created_at.desc())
    return list(session.scalars(statement))


def list_suggested_matches_for_item(
    session: Session,
    item_id: UUID,
) -> list[MatchSuggestion]:
    statement = (
        select(MatchSuggestion)
        .where(MatchSuggestion.status == MatchStatus.SUGGESTED)
        .where(
            or_(
                MatchSuggestion.lost_item_id == item_id,
                MatchSuggestion.found_item_id == item_id,
            ),
        )
        .order_by(MatchSuggestion.created_at.asc())
    )
    return list(session.scalars(statement))
