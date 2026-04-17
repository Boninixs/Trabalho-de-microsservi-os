# Auth Service

## Objetivo
O `auth-service` é responsável por cadastro, login, emissão de JWT e autorização básica por perfil.

## Endpoints
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `GET /health`
- `GET /docs`

## Fluxo de autenticação
1. O cliente registra um usuário em `POST /auth/register`.
2. O cliente autentica via `POST /auth/login`.
3. O serviço retorna um JWT com `sub`, `role` e `exp`.
4. O cliente envia `Authorization: Bearer <token>` para acessar `GET /auth/me`.

## Variáveis de ambiente
- `DATABASE_URL`
- `DATABASE_ECHO`
- `JWT_SECRET`
- `JWT_ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `SERVICE_NAME`
- `SERVICE_VERSION`
- `SERVICE_PORT`
- `ENVIRONMENT`
- `LOG_LEVEL`

## Restrições
- O serviço usa PostgreSQL como base ativa.
- O serviço não consome eventos do broker.
- O fluxo operacional não depende de SQLite.
