# API Gateway

## Objetivo
O `gateway` é o ponto único de entrada HTTP do sistema. Ele roteia requisições para os microsserviços, valida JWT, aplica regras simples de acesso e propaga headers úteis.

## Responsabilidades
- Expor rotas públicas sob `/api/*`
- Validar `Authorization: Bearer <token>`
- Validar e propagar claims mínimas `sub`, `role`, `exp`
- Propagar `Authorization` e `X-Correlation-ID`
- Tratar timeout e indisponibilidade downstream de forma consistente

## Restrições
- Não consome eventos do RabbitMQ
- Não executa regra de negócio de domínio
- Não acessa banco de nenhum serviço
- Não expõe endpoints internos de saga

## Mapa de rotas públicas
- `POST /api/auth/register` -> `auth-service /auth/register`
- `POST /api/auth/login` -> `auth-service /auth/login`
- `GET /api/auth/me` -> `auth-service /auth/me`
- `GET /api/items` -> `item-service /items`
- `POST /api/items` -> `item-service /items`
- `GET /api/items/{id}` -> `item-service /items/{id}`
- `PATCH /api/items/{id}` -> `item-service /items/{id}`
- `PATCH /api/items/{id}/status` -> `item-service /items/{id}/status`
- `GET /api/items/{id}/history` -> `item-service /items/{id}/history`
- `GET /api/matches` -> `matching-service /matches`
- `GET /api/matches/{id}` -> `matching-service /matches/{id}`
- `POST /api/matches/{id}/accept` -> `matching-service /matches/{id}/accept`
- `POST /api/matches/{id}/reject` -> `matching-service /matches/{id}/reject`
- `GET /api/recovery-cases` -> `recovery-case-service /recovery-cases`
- `GET /api/recovery-cases/{id}` -> `recovery-case-service /recovery-cases/{id}`
- `POST /api/recovery-cases/{id}/cancel` -> `recovery-case-service /recovery-cases/{id}/cancel`
- `POST /api/recovery-cases/{id}/complete` -> `recovery-case-service /recovery-cases/{id}/complete`
- `GET /health` -> `gateway`

## Regras simples de acesso
- `POST /api/auth/register` e `POST /api/auth/login` são públicas
- As demais rotas públicas exigem JWT válido com perfil `USER` ou `ADMIN`

## Rotas internas bloqueadas
- `/api/internal/recovery/open`
- `/api/internal/recovery/cancel`
- `/api/internal/recovery/complete`

## Tratamento de erro downstream
- Timeout downstream -> `504`
- Indisponibilidade downstream -> `502`
- Respostas HTTP normais do serviço downstream são repassadas com o mesmo status
