# Eventos e Mensageria

## Envelope padrão
Todos os eventos de domínio usam o envelope abaixo:

- `event_id`
- `event_type`
- `aggregate_id`
- `aggregate_version`
- `occurred_at`
- `correlation_id`
- `causation_id`
- `payload`

O schema JSON de referência está em `contracts/events/domain-event-envelope.schema.json`.

## Exchange e routing keys
- Exchange principal: `domain.events`
- Exchange de dead-letter: `domain.events.dlx`
- Routing keys:
  - `item.created`
  - `item.updated`
  - `match.suggested`
  - `match.accepted`
  - `match.rejected`
  - `recovery_case.opened`
  - `recovery_case.cancelled`
  - `recovery_case.completed`

## Topologia mínima coerente com os consumidores reais
- `matching-service.item-events`
  - bindings: `item.created`, `item.updated`
- `matching-service.item-events.dlq`
  - bindings no DLX: `item.created`, `item.updated`
- `recovery-case-service.match-events`
  - binding: `match.accepted`
- `recovery-case-service.match-events.dlq`
  - binding no DLX: `match.accepted`
- `domain.events.audit`
  - bindings: todos os routing keys publicados
  - objetivo: garantir rota durável para eventos sem consumidor de domínio imediato, preservando confirmação real do broker com `mandatory=True`

## Garantias do publisher de outbox
- O evento só é marcado como `PUBLISHED` depois do retorno bem-sucedido do broker.
- A publicação usa mensagem persistente e `publisher_confirms`.
- A publicação usa `mandatory=True`, evitando marcar como entregue um evento sem rota válida.
- Falhas transitórias movem o registro para `FAILED` com `available_at` futuro.
- Falhas repetidas acima de `OUTBOX_PUBLISH_MAX_ATTEMPTS` movem o registro para `EXHAUSTED`.
- Eventos `PENDING` e `FAILED` permanecem em banco e são retomados após restart do container.

## Regras de publicação e consumo
- Eventos nunca são publicados diretamente do controller.
- O registro inicial da publicação sempre nasce em `outbox_events`.
- Consumidores aplicam idempotência em `processed_events`.
- O `gateway` não consome eventos do broker.
- Serviços não atualizam diretamente o banco de outro serviço.
