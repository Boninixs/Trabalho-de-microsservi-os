# Recovery Case Service

## Objetivo
O `recovery-case-service` consome `MatchAccepted`, abre automaticamente casos de recuperação e orquestra a saga com o `item-service` pelos endpoints internos de recovery.

## Endpoints
- `GET /recovery-cases`
- `GET /recovery-cases/{id}`
- `POST /recovery-cases/{id}/cancel`
- `POST /recovery-cases/{id}/complete`
- `GET /health`

## Regras implementadas
- `MatchAccepted` abre automaticamente um caso via consumer idempotente.
- O `item-service` é chamado apenas pelos endpoints internos:
  - `/internal/recovery/open`
  - `/internal/recovery/cancel`
  - `/internal/recovery/complete`
- Um item `FOUND` não pode estar em mais de um caso ativo ao mesmo tempo.
- Cancelamento executa compensação coordenada no `item-service`.
- Conclusão executa atualização final coordenada no `item-service`.
- `RecoveryCaseOpened`, `RecoveryCaseCancelled` e `RecoveryCaseCompleted` são gravados em `outbox_events`.
- O publisher de outbox publica com confirmação do broker e retry finito.

## Estratégia para bloquear mais de um caso ativo por FOUND
- Validação em aplicação antes da abertura, consultando se já existe caso ativo para o `found_item_id`.
- Proteção em banco com índice único parcial `ux_recovery_cases_found_item_active` sobre `found_item_id` quando `status IN ('OPEN', 'IN_PROGRESS')`.
- A combinação das duas camadas cobre regra de negócio e corrida concorrente.

## Filas
- `recovery-case-service.match-events`
- `recovery-case-service.match-events.dlq`

## Variáveis de ambiente
- `DATABASE_URL`
- `DATABASE_ECHO`
- `RABBITMQ_URL`
- `RABBITMQ_EVENTS_EXCHANGE`
- `RABBITMQ_DEAD_LETTER_EXCHANGE`
- `EVENT_CONSUMER_ENABLED`
- `RABBITMQ_MATCH_EVENTS_QUEUE`
- `ITEM_SERVICE_BASE_URL`
- `ITEM_SERVICE_TIMEOUT_SECONDS`
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
