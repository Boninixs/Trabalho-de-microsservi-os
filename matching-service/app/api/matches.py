from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.exceptions import InvalidMatchDecisionError, MatchNotFoundError
from app.db.session import get_db
from app.mappers.match_mapper import to_match_response
from app.models.match_suggestion import MatchStatus
from app.schemas.match import MatchDecisionRequest, MatchFilters, MatchResponse
from app.services.matching_service import (
    accept_match,
    list_match_suggestions,
    reject_match,
    retrieve_match_suggestion,
)

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("", response_model=list[MatchResponse])
def list_matches_endpoint(
    status_filter: MatchStatus | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
) -> list[MatchResponse]:
    filters = MatchFilters(status=status_filter)
    return [to_match_response(match) for match in list_match_suggestions(db, filters)]


@router.get("/{match_id}", response_model=MatchResponse)
def get_match_endpoint(match_id: UUID, db: Session = Depends(get_db)) -> MatchResponse:
    try:
        match = retrieve_match_suggestion(db, match_id)
    except MatchNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return to_match_response(match)


@router.post("/{match_id}/accept", response_model=MatchResponse)
def accept_match_endpoint(
    match_id: UUID,
    payload: MatchDecisionRequest,
    db: Session = Depends(get_db),
) -> MatchResponse:
    try:
        match = accept_match(db, match_id, payload)
    except MatchNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidMatchDecisionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return to_match_response(match)


@router.post("/{match_id}/reject", response_model=MatchResponse)
def reject_match_endpoint(
    match_id: UUID,
    payload: MatchDecisionRequest,
    db: Session = Depends(get_db),
) -> MatchResponse:
    try:
        match = reject_match(db, match_id, payload)
    except MatchNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidMatchDecisionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return to_match_response(match)
