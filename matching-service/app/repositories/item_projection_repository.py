from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.item_projection import ExternalItemStatus, ItemClassification, ItemProjection


def get_item_projection_by_id(session: Session, item_id: UUID) -> ItemProjection | None:
    return session.get(ItemProjection, item_id)


def add_item_projection(session: Session, item_projection: ItemProjection) -> ItemProjection:
    session.add(item_projection)
    return item_projection


def list_candidate_item_projections(
    session: Session,
    *,
    classification: ItemClassification,
    exclude_item_id: UUID,
) -> list[ItemProjection]:
    statement: Select[tuple[ItemProjection]] = (
        select(ItemProjection)
        .where(ItemProjection.classification == classification)
        .where(ItemProjection.id != exclude_item_id)
        .order_by(ItemProjection.created_at.asc())
    )
    return list(session.scalars(statement))


def get_item_projections_by_ids(session: Session, item_ids: list[UUID]) -> list[ItemProjection]:
    statement = select(ItemProjection).where(ItemProjection.id.in_(item_ids))
    return list(session.scalars(statement))

