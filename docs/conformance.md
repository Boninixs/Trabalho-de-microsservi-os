# Conformidade com o `agent.md`

## Checklist arquitetural
- Stack oficial mantida: Python, FastAPI, PostgreSQL por serviço, RabbitMQ, Alembic, Docker e Docker Compose.
- Microsserviços finais: `auth-service`, `item-service`, `matching-service`, `recovery-case-service`.
- `gateway` como ponto único de entrada HTTP.
- Comunicação síncrona via REST e assíncrona via eventos.
- `gateway` HTTP-only e sem consumo de eventos.
- Saga implementada no `recovery-case-service`.
- `Notification Service` permanece fora do escopo.
- Não existem foreign keys entre bancos de serviços diferentes.
- Entre serviços trafegam apenas IDs externos.

## Integridade obrigatória
- Duplicidade do mesmo par `LOST + FOUND` bloqueada por constraint.
- Mais de um caso ativo para o mesmo `FOUND` bloqueado em aplicação e banco.
- Reprocessamento duplicado de evento bloqueado por `processed_events`.
- O `item-service` permanece como única autoridade de status do item.

## Limitações finais
- Replay automático de DLQ não foi implementado.
- Eventos `EXHAUSTED` no outbox exigem ação operacional.
- Não há interface em tempo real nem notificações.
