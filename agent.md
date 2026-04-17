# AGENTS.md

## Objetivo do projeto
Construir um sistema acadêmico de Achados e Perdidos Inteligente em arquitetura de microsserviços.

## Regras arquiteturais obrigatórias
- A arquitetura deve ter exatamente 4 microsserviços principais:
  1. Auth Service
  2. Item Service
  3. Matching Service
  4. Recovery Case Service
- Deve existir API Gateway como ponto único de entrada.
- Deve existir comunicação síncrona via REST e assíncrona via mensageria.
- O padrão Event-Driven é obrigatório.
- O padrão Saga Pattern é obrigatório no fluxo de recuperação.
- JWT é obrigatório para autenticação.
- Cada microsserviço deve ter banco de dados próprio.
- O ambiente deve rodar por Docker Compose.
- Notification Service NÃO faz parte do escopo atual. Deve ser tratado apenas como trabalho futuro.

## Regras de domínio obrigatórias
- O Item Service é o núcleo principal do domínio.
- Um item deve possuir classificação obrigatória: LOST ou FOUND.
- O sistema deve registrar itens com informações como:
  - título ou nome resumido
  - descrição
  - categoria
  - cor
  - local
  - data aproximada
  - usuário responsável pelo cadastro
  - status
- O Matching Service só pode sugerir correspondência entre um item LOST e um item FOUND.
- Para haver match, deve existir compatibilidade de categoria e pelo menos mais um critério relevante.
- Itens encerrados não podem voltar ao processo de matching.
- Um item encontrado não pode participar de mais de um caso ativo ao mesmo tempo.
- Um item só pode ser marcado como recuperado após caso concluído.

## Serviços e responsabilidades
### Auth Service
- cadastro de usuário
- login
- emissão e validação de JWT
- controle de acesso básico por perfil

### Item Service
- CRUD de itens
- classificação LOST/FOUND
- filtros de consulta
- atualização de status
- publicação de eventos quando item for criado ou atualizado

### Matching Service
- consumo de eventos de item
- cálculo de score de similaridade
- persistência de sugestões de correspondência
- confirmação e rejeição de sugestões

### Recovery Case Service
- abertura de caso a partir de match confirmado
- acompanhamento do caso
- conclusão do caso
- cancelamento com compensação via saga
- atualização coordenada dos estados necessários

## Eventos mínimos obrigatórios
- ItemCreated
- ItemUpdated
- MatchSuggested
- MatchAccepted
- MatchRejected
- RecoveryCaseOpened
- RecoveryCaseCancelled
- RecoveryCaseCompleted

## Requisitos de implementação
- Usar arquitetura em camadas em cada serviço
- Separar controller, service, repository, entity/model, DTO, mapper e tests
- Expor documentação OpenAPI/Swagger
- Criar testes unitários e de integração para os fluxos principais
- Criar Dockerfile para cada serviço
- Criar docker-compose para subir tudo

## Definition of Done
Uma etapa só está pronta quando:
- o código compila
- os testes da etapa passam
- os endpoints principais funcionam
- a documentação da etapa foi atualizada
- os comandos para rodar foram informados no final