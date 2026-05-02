""""
Esse arquivo é responsável por fornecer funções para interagir com a tabela de ProcessedEvent no banco de dados. 
Ele inclui funções para verificar se um evento já foi processado e para adicionar um novo evento processado à tabela.
"""
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.processed_event import ProcessedEvent


def is_event_processed(session: Session, event_id: UUID) -> bool:
    """"
    Verifica se um evento já foi processado, consultando a tabela de ProcessedEvent pelo ID do evento.
    Retorna True se o evento já foi processado, ou False caso não tenha.
    """
    return session.get(ProcessedEvent, event_id) is not None


def add_processed_event(
    session: Session,
    processed_event: ProcessedEvent,
) -> ProcessedEvent:
    """"
    Adiciona um novo evento processado à tabela de ProcessedEvent.
    """
    session.add(processed_event)
    return processed_event

