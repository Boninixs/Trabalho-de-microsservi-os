# Testes Manuais Pelo Terminal

Fluxo manual via `curl` para validar autenticação, itens, match e recovery case pelo `gateway`.

## Pré-requisitos

- Stack em execução com `docker compose up --build -d`
- `jq` instalado para extrair IDs e token
- Gateway acessível em `http://localhost:8000`

## Script único

```bash
#!/usr/bin/env bash

set -euo pipefail

BASE_URL="http://localhost:8000"
EMAIL="teste.$(date +%s)@example.com"
PASSWORD="Password123"
NAME="Usuario Teste"

echo "1) Health: verifica se o gateway está no ar"
curl -s "$BASE_URL/health" | jq

echo
echo "2) Register: cria um usuário para o fluxo"
REGISTER_RESPONSE=$(
  curl -s -X POST "$BASE_URL/api/auth/register" \
    -H "Content-Type: application/json" \
    -d "{
      \"full_name\": \"$NAME\",
      \"email\": \"$EMAIL\",
      \"password\": \"$PASSWORD\"
    }"
)
echo "$REGISTER_RESPONSE" | jq
USER_ID=$(echo "$REGISTER_RESPONSE" | jq -r '.id')

echo
echo "3) Login: obtém o token JWT"
LOGIN_RESPONSE=$(
  curl -s -X POST "$BASE_URL/api/auth/login" \
    -H "Content-Type: application/json" \
    -d "{
      \"email\": \"$EMAIL\",
      \"password\": \"$PASSWORD\"
    }"
)
echo "$LOGIN_RESPONSE" | jq
TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token')

echo
echo "4) Auth me: confirma o usuário autenticado"
curl -s "$BASE_URL/api/auth/me" \
  -H "Authorization: Bearer $TOKEN" | jq

echo
echo "5) Create LOST: cria o item perdido"
LOST_RESPONSE=$(
  curl -s -X POST "$BASE_URL/api/items" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"classification\": \"LOST\",
      \"title\": \"Mochila preta perdida\",
      \"description\": \"Mochila preta com notebook e caderno\",
      \"category\": \"Mochila\",
      \"color\": \"Preta\",
      \"location_description\": \"Biblioteca central\",
      \"approximate_date\": \"2026-04-20\",
      \"reporter_user_id\": \"$USER_ID\"
    }"
)
echo "$LOST_RESPONSE" | jq
LOST_ID=$(echo "$LOST_RESPONSE" | jq -r '.id')

echo
echo "6) Create FOUND: cria o item encontrado compatível"
FOUND_RESPONSE=$(
  curl -s -X POST "$BASE_URL/api/items" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"classification\": \"FOUND\",
      \"title\": \"Mochila preta encontrada\",
      \"description\": \"Mochila preta com notebook e caderno encontrada na biblioteca\",
      \"category\": \"Mochila\",
      \"color\": \"Preta\",
      \"location_description\": \"Biblioteca central\",
      \"approximate_date\": \"2026-04-20\",
      \"reporter_user_id\": \"$USER_ID\"
    }"
)
echo "$FOUND_RESPONSE" | jq
FOUND_ID=$(echo "$FOUND_RESPONSE" | jq -r '.id')

echo
echo "7) List items: consulta os itens criados"
curl -s "$BASE_URL/api/items" \
  -H "Authorization: Bearer $TOKEN" | jq

echo
echo "8) Get item: busca o item FOUND por ID"
curl -s "$BASE_URL/api/items/$FOUND_ID" \
  -H "Authorization: Bearer $TOKEN" | jq

echo
echo "9) Patch item: atualiza a descrição do item FOUND"
curl -s -X PATCH "$BASE_URL/api/items/$FOUND_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Mochila preta com notebook, caderno e garrafa encontrada na biblioteca"
  }' | jq

echo
echo "10) Wait match: aguarda o match SUGGESTED aparecer"
MATCH_ID=""
for i in $(seq 1 20); do
  MATCH_ID=$(
    curl -s "$BASE_URL/api/matches" \
      -H "Authorization: Bearer $TOKEN" \
    | jq -r --arg LOST_ID "$LOST_ID" --arg FOUND_ID "$FOUND_ID" '
        map(select(.lost_item_id == $LOST_ID and .found_item_id == $FOUND_ID and .status == "SUGGESTED")) | .[0].id // empty
      '
  )
  [ -n "$MATCH_ID" ] && break
  sleep 2
done
echo "MATCH_ID=$MATCH_ID"

echo
echo "11) List matches: confirma o match sugerido"
curl -s "$BASE_URL/api/matches" \
  -H "Authorization: Bearer $TOKEN" | jq

echo
echo "12) Accept match: aceita o match para abrir recovery"
curl -s -X POST "$BASE_URL/api/matches/$MATCH_ID/accept" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"decided_by_user_id\": \"$USER_ID\"
  }" | jq

echo
echo "13) Wait recovery case: aguarda o caso ser criado"
CASE_ID=""
for i in $(seq 1 20); do
  CASE_ID=$(
    curl -s "$BASE_URL/api/recovery-cases" \
      -H "Authorization: Bearer $TOKEN" \
    | jq -r --arg MATCH_ID "$MATCH_ID" '
        map(select(.match_id == $MATCH_ID)) | .[0].id // empty
      '
  )
  [ -n "$CASE_ID" ] && break
  sleep 2
done
echo "CASE_ID=$CASE_ID"

echo
echo "14) List recovery-cases: lista os casos de recuperação"
curl -s "$BASE_URL/api/recovery-cases" \
  -H "Authorization: Bearer $TOKEN" | jq

echo
echo "15) Complete recovery: conclui o caso com sucesso"
curl -s -X POST "$BASE_URL/api/recovery-cases/$CASE_ID/complete" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"actor_user_id\": \"$USER_ID\",
    \"reason\": \"Entrega concluida com sucesso\"
  }" | jq
```

## Variação útil

Se quiser testar cancelamento em vez de conclusão, troque a etapa final por:

```bash
curl -s -X POST "$BASE_URL/api/recovery-cases/$CASE_ID/cancel" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"actor_user_id\": \"$USER_ID\",
    \"reason\": \"Cancelado para teste manual\",
    \"target_status\": \"AVAILABLE\"
  }" | jq
```

Se quiser testar rejeição de match em vez de aceitar, use:

```bash
curl -s -X POST "$BASE_URL/api/matches/$MATCH_ID/reject" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"decided_by_user_id\": \"$USER_ID\"
  }" | jq
```
