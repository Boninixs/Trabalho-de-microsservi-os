# Arquitetura Final

## Serviços operacionais
- `gateway`
- `auth-service`
- `item-service`
- `matching-service`
- `recovery-case-service`
- `auth-postgres`
- `item-postgres`
- `matching-postgres`
- `recovery-postgres`
- `rabbitmq`

## Responsabilidades por serviço
- `gateway`: ponto único de entrada HTTP sob `/api/*`, valida JWT, aplica regras simples de acesso, propaga `Authorization` e `X-Correlation-ID`.
- `auth-service`: cadastro, login, emissão e validação de JWT.
- `item-service`: autoridade exclusiva sobre o estado do item e origem confiável de `ItemCreated` e `ItemUpdated`.
- `matching-service`: consome eventos de item, mantém projeção local e gera/decide sugestões de match.
- `recovery-case-service`: consome `MatchAccepted`, abre casos automaticamente e orquestra a saga com o `item-service`.

## Fluxo síncrono
1. O cliente chama apenas o `gateway`.
2. O `gateway` valida o token quando a rota é protegida.
3. O `gateway` roteia para `auth-service`, `item-service`, `matching-service` ou `recovery-case-service`.
4. O `recovery-case-service` chama somente os endpoints internos do `item-service` para abertura, cancelamento e conclusão da saga.

## Fluxo assíncrono real
1. O `item-service` grava `ItemCreated` ou `ItemUpdated` em `outbox_events` na mesma transação do item.
2. O publisher de outbox do `item-service` publica no exchange `domain.events` com confirmação real do broker.
3. O `matching-service` consome `item.created` e `item.updated`, aplica idempotência e gera ou expira sugestões.
4. O `matching-service` grava `MatchSuggested`, `MatchAccepted` ou `MatchRejected` em seu próprio outbox.
5. O publisher de outbox do `matching-service` publica esses eventos no broker.
6. O `recovery-case-service` consome `match.accepted`, aplica idempotência e abre automaticamente o caso.
7. O `recovery-case-service` chama o `item-service` por HTTP interno para mover os itens para `IN_RECOVERY`, compensar cancelamentos e concluir com `RECOVERED`.
8. O `recovery-case-service` grava `RecoveryCaseOpened`, `RecoveryCaseCancelled` e `RecoveryCaseCompleted` em seu outbox.
9. O publisher de outbox do `recovery-case-service` publica esses eventos no broker.

## Broker e filas
- Exchange principal: `domain.events`
- DLX: `domain.events.dlx`
- Filas de consumo real:
  - `matching-service.item-events`
  - `recovery-case-service.match-events`
- Fila de auditoria durável:
  - `domain.events.audit`
- Filas de dead-letter:
  - `matching-service.item-events.dlq`
  - `recovery-case-service.match-events.dlq`

## Integridade e hardening
- Outbox com estados `PENDING`, `FAILED`, `PUBLISHED` e `EXHAUSTED`.
- Retry do publisher com polling configurável, backoff exponencial e limite de tentativas.
- Reprocessamento idempotente por `processed_events`.
- Constraint de unicidade para impedir match duplicado entre o mesmo par `LOST + FOUND`.
- Índice único parcial para impedir mais de um caso ativo para o mesmo `FOUND`.
- O `gateway` não consome eventos e não acessa banco de nenhum serviço.
- Não há foreign keys entre bancos de serviços diferentes.

## Limitações conhecidas
- Não existe replay automático das filas `.dlq`; o tratamento é operacional e manual.
- Eventos com status `EXHAUSTED` no outbox exigem intervenção operacional.
- O `Notification Service` continua fora do escopo.
