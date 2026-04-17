# Matching Service

## Objetivo
O `matching-service` consome eventos do `item-service`, mantém projeções locais e gera sugestões válidas entre um item `LOST` e um item `FOUND`.

## Endpoints
- `GET /matches`
- `GET /matches/{id}`
- `POST /matches/{id}/accept`
- `POST /matches/{id}/reject`
- `GET /health`

## Regras implementadas
- Sugestões só existem entre `LOST` e `FOUND`.
- `category` precisa ser igual.
- Além de `category`, pelo menos mais um critério relevante precisa coincidir:
  - `color`
  - `location_description`
  - `approximate_date`
  - palavras-chave de `title` e `description`
- Itens com status fora de `AVAILABLE` não participam do matching.
- Itens `CANCELLED` e `CLOSED` expiram sugestões abertas e não entram em novos matches.
- O par `lost_item_id + found_item_id` é protegido por constraint única.
- O consumo de eventos usa `processed_events` para idempotência.
- Eventos `MatchSuggested`, `MatchAccepted` e `MatchRejected` são gravados em `outbox_events`.
- O publisher de outbox publica com confirmação do broker e retry finito.

## Filas
- `matching-service.item-events`
- `matching-service.item-events.dlq`

## Variáveis de ambiente
- `DATABASE_URL`
- `DATABASE_ECHO`
- `RABBITMQ_URL`
- `RABBITMQ_EVENTS_EXCHANGE`
- `RABBITMQ_DEAD_LETTER_EXCHANGE`
- `EVENT_CONSUMER_ENABLED`
- `RABBITMQ_ITEM_EVENTS_QUEUE`
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
