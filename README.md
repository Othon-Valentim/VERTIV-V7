# VERTIV V7.0

VERTIV V7.0 e um Tribunal Agentico de Risco Imobiliario para o mercado brasileiro. O produto recebe um Data Room em ZIP, usa IA para extrair evidencias, executa o Diamond Core em Python/Polars, compara o resultado com calibracoes GoldenEvaluator e entrega uma Sentenca de Capital auditavel.

## Fluxo Principal V7

```text
ZIP Data Room -> IA extrai -> Diamond Core/Polars calcula -> GoldenEvaluator compara -> Sentenca de Capital
```

1. O operador envia um ZIP com documentos do ativo pelo fluxo de Data Room.
2. A API grava o arquivo no bucket privado `data-rooms` do Supabase e cria uma ingestao.
3. O worker processa a fila. Com `USE_MOCK=1`, usa extracao simulada para dry run local. Com `USE_MOCK=0`, usa o provider LLM configurado.
4. A IA extrai campos estruturados; ela nao decide a viabilidade financeira.
5. O Diamond Core calcula fluxo de caixa, opcoes reais, riscos e metricas em Polars/Python.
6. O GoldenEvaluator compara a ingestao contra um historico/calibracao quando ha `legacy_simulation_id`.
7. A interface de auditoria apresenta a sentenca, evidencias, calculos, motivos de kill e acoes humanas.

V6 permanece no repositorio somente como legado de calibracao e compatibilidade. O fluxo oficial V7.0 e Data Room primeiro, nao wizard manual.

## Componentes

| Camada | Papel |
| --- | --- |
| Frontend | Next.js 14 para upload, acompanhamento, auditoria e confirmacao de sentenca |
| Backend | FastAPI para autenticacao, ingestao, status, acoes humanas e OpenAPI |
| Worker | Python para extracao, Diamond Core/Polars e atualizacao de status |
| Supabase | Auth, Postgres com RLS e Storage privado `data-rooms` |
| Golden dataset | Calibracao historica e comparacao de resultados |

## Quick Start Local

### Requisitos

- Node.js 18+
- Python 3.11+
- Supabase configurado com Auth, Postgres e bucket privado `data-rooms`
- Variaveis de ambiente locais para frontend, backend e worker

### Variaveis principais

```bash
USE_MOCK=1
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
WEBMCP_ENABLED=false
NEXT_PUBLIC_WEBMCP_ENABLED=false
```

Use `USE_MOCK=1` para demonstracao e dry run sem gasto de tokens. Reserve `USE_MOCK=0` para smoke controlado com chaves LLM validas.

### Subir os servicos

Em terminais separados:

```bash
npm run dev:frontend
npm run dev:backend
npm run dev:worker
```

Portas esperadas:

| Servico | Porta | Comando |
| --- | ---: | --- |
| Frontend | 3002 | `npm run dev:frontend` |
| Backend | 8000 | `npm run dev:backend` |
| Worker | 8001 | `npm run dev:worker` |

Tambem e possivel iniciar frontend e backend juntos com:

```bash
npm run dev
```

## API V7 Oficial

Base local: `http://localhost:8000`

| Metodo | Rota | Uso |
| --- | --- | --- |
| `GET` | `/health` | Saude da API V7 |
| `POST` | `/api/v7/ingest` | Upload do Data Room ZIP |
| `GET` | `/api/v7/ingestion/{id}` | Status, evidencias, calculos e sentenca |
| `POST` | `/api/v7/ingestion/{id}/manual-audit` | Solicitar auditoria humana |
| `POST` | `/api/v7/ingestion/{id}/confirm-sentence` | Confirmar sentenca |

Rotas antigas de simulacao podem existir para compatibilidade, mas nao definem o fluxo principal V7.0.

## Verificacao

Scripts V7 adicionados no pacote raiz:

```bash
npm run test:v7
npm run test:v7:backend
npm run test:v7:worker
npm run test:v7:e2e
npm run verify:v7
```

Os testes E2E V7 esperam os servicos locais ativos nas portas acima.

## WebMCP

WebMCP e experimental em V7.0 e fica fora do fluxo principal. Ative somente de forma controlada:

```bash
WEBMCP_ENABLED=true
NEXT_PUBLIC_WEBMCP_ENABLED=true
```

Com as flags desligadas, a aplicacao deve funcionar normalmente sem registrar rotas WebMCP nem depender de `window.modelContext`.

Quando `WEBMCP_ENABLED=true`, o backend tambem registra o catalogo B2B/WebMCP experimental:

| Metodo | Rota | Uso |
| --- | --- | --- |
| `GET` | `/api/v7/openapi/schemas` | Schemas expostos para integracoes B2B/WebMCP flagged |

## Documentacao

- [Arquitetura](docs/ARCHITECTURE.md)
- [Contrato de API](docs/API_CONTRACT.md)
- [Mapa da API Backend](docs/BACKEND_API_MAP.md)
- [Guia do Usuario](docs/GUIA_USUARIO.md)
- [Manual Operacional](docs/USER_MANUAL.md)

Copyright 2026 VERTIV CAPITAL.
