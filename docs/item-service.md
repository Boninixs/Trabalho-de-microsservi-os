# Item Service

## Objetivo
O `item-service` é a autoridade exclusiva sobre o ciclo de vida dos itens e a origem confiável dos eventos `ItemCreated` e `ItemUpdated`.

## Endpoints públicos
- `POST /items`
- `GET /items`
- `GET /items/{id}`
- `PATCH /items/{id}`
- `PATCH /items/{id}/status`
- `GET /items/{id}/history`
- `GET /health`

## Endpoints internos
- `POST /internal/recovery/open`
- `POST /internal/recovery/cancel`
- `POST /internal/recovery/complete`

## Enums oficiais
- `classification`: `LOST`, `FOUND`
- `item_status`: `AVAILABLE`, `MATCHED`, `IN_RECOVERY`, `RECOVERED`, `CANCELLED`, `CLOSED`

## Regras implementadas
- Todo item nasce com `status = AVAILABLE`.
- `classification` é obrigatório e validado por enum.
- Somente o `item-service` altera o status dos itens.
- Itens `CANCELLED` e `CLOSED` não retornam ao fluxo de matching.
- Toda mudança de status gera histórico.
- Eventos `ItemCreated` e `ItemUpdated` são gravados em `outbox_events` na mesma transação do agregado.
- O publisher de outbox publica com confirmação do broker e retry finito.

## Variáveis de ambiente
- `DATABASE_URL`
- `DATABASE_ECHO`
- `RABBITMQ_URL`
- `RABBITMQ_EVENTS_EXCHANGE`
- `RABBITMQ_DEAD_LETTER_EXCHANGE`
- `OUTBOX_PUBLISHER_ENABLED`
- `OUTBOX_PUBLISH_POLL_INTERVAL_SECONDS`
- `OUTBOX_PUBLISH_BATCH_SIZE`
- `OUTBOX_PUBLISH_RETRY_DELAY_SECONDS`
- `OUTBOX_PUBLISH_MAX_ATTEMPTS`
- `SERVICE_NAME`
- `SERVICE_VERSION`
- `SERVICE_PORT`
- `ENVIRONMENT`
- `LOG_LEVEL`
