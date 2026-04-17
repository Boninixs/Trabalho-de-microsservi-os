# Desenvolvimento Local

## Pré-requisitos
- Docker Engine
- Docker Compose
- Python 3.11 com dependências instaladas localmente, se quiser rodar testes fora dos containers

## Portas padrão
- Gateway: `http://localhost:8000`
- Auth Service: `http://localhost:8001`
- Item Service: `http://localhost:8002`
- Matching Service: `http://localhost:8003`
- Recovery Case Service: `http://localhost:8004`
- RabbitMQ Management: `http://localhost:15672`

## Subir todo o ambiente final
1. Copie `.env.example` para `.env`.
2. Ajuste credenciais e portas se necessário.
3. Execute `docker compose up --build -d`.
4. Verifique a saúde com `docker compose ps`.

Os containers de `auth-service`, `item-service`, `matching-service` e `recovery-case-service` executam `alembic upgrade head` na inicialização.

## Rodar migrations manualmente
Use `./scripts/migrate_all.sh` com o ambiente Python configurado localmente ou execute o Alembic em cada serviço:

- `cd auth-service && alembic upgrade head`
- `cd item-service && alembic upgrade head`
- `cd matching-service && alembic upgrade head`
- `cd recovery-case-service && alembic upgrade head`

## Rodar a suíte E2E
1. Suba o ambiente completo com `docker compose up --build -d`.
2. Garanta que o gateway responde em `GET /health`.
3. Execute `./scripts/run_e2e.sh`.

Variáveis úteis para a suíte:
- `E2E_GATEWAY_URL`
- `E2E_RABBITMQ_URL`
- `E2E_ITEM_DB_URL`
- `E2E_MATCHING_DB_URL`
- `E2E_RECOVERY_DB_URL`
- `E2E_WAIT_TIMEOUT_SECONDS`
- `E2E_POLL_INTERVAL_SECONDS`

## Rodar testes por serviço
- `cd auth-service && pytest -q`
- `cd item-service && pytest -q`
- `cd matching-service && pytest -q`
- `cd recovery-case-service && pytest -q`
- `cd gateway && pytest -q`

## Fluxo assíncrono validado pela suíte E2E
- Cadastro e login pelo `gateway`
- Criação de item `LOST`
- Criação de item `FOUND`
- Geração de match por eventos reais `ItemCreated` e `ItemUpdated`
- Aceitação de match
- Abertura automática do recovery case por consumo de `MatchAccepted`
- Cancelamento com compensação
- Novo fluxo com reabertura e conclusão final
- Bloqueio de duplicidade de evento
- Bloqueio de duplicidade de match
- Bloqueio de mais de um caso ativo para o mesmo `FOUND`
- Bloqueio de `/api/internal/*` no `gateway`

## Observabilidade operacional
- Logs estruturados com correlação por `X-Correlation-ID`
- Healthcheck HTTP em todos os serviços
- DLQ para consumidores reais do broker
- Retry finito no publisher de outbox
