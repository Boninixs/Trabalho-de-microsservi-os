from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.outbox import OutboxEvent


def add_outbox_event(session: Session, outbox_event: OutboxEvent) -> OutboxEvent:
    session.add(outbox_event)
    return outbox_event


def list_pending_outbox_events(
    session: Session,
    limit: int = 100,
) -> list[OutboxEvent]:
    statement = (
        select(OutboxEvent)
        .where(OutboxEvent.status == "PENDING")
        .order_by(OutboxEvent.occurred_at)
        .limit(limit)
    )
    return list(session.scalars(statement))


def mark_outbox_event_published(session: Session, event_id: UUID) -> OutboxEvent | None:
    outbox_event = session.get(OutboxEvent, event_id)
    if outbox_event is None:
        return None

    outbox_event.status = "PUBLISHED"
    outbox_event.publish_attempts += 1
    return outbox_event

