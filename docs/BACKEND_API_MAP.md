# Backend API Map - VERTIV V7.0

**Base local:** `http://localhost:8000`
**Arquivo principal:** `apps/backend/src/api/main.py`
**Fluxo oficial:** Data Room ZIP -> IA -> Diamond Core/Polars -> GoldenEvaluator -> Sentenca de Capital

## Resumo

| Modulo | Rotas | Autenticacao | Papel |
| --- | ---: | --- | --- |
| Core | 2 | Misto | health e usuario atual |
| V7 Ingestion | 4+ | JWT | upload, status e acoes humanas |
| WebMCP | condicional | JWT | experimental por feature flag |
| Compatibilidade | varias | JWT | simulacoes historicas e apoio legado |

## Core

| Metodo | Rota | Funcao | Auth |
| --- | --- | --- | --- |
| `GET` | `/health` | `health_check()` | Publica |
| `GET` | `/me` | `get_current_user_info()` | JWT |

Health esperado:

```json
{
  "status": "ok",
  "version": "7.0.0",
  "product": "VERTIV V7.0",
  "mode": "TRIBUNAL_AGENTICO_RISCO_IMOBILIARIO",
  "security": "enabled",
  "webmcp_enabled": false
}
```

## V7 Ingestion

**Arquivo:** `apps/backend/src/api/routes/ingest.py`
**Prefixo:** `/api/v7`
**Tag:** `V7 Ingestion`

| Metodo | Rota | Funcao | Descricao |
| --- | --- | --- | --- |
| `POST` | `/api/v7/ingest` | `ingest_data_room()` | Recebe ZIP, valida, grava no bucket `data-rooms` e cria ingestao |
| `GET` | `/api/v7/ingestion/{ingestion_id}` | `get_ingestion()` | Retorna status, evidencias, calculos e metadados de decisao |
| `POST` | `/api/v7/ingestion/{ingestion_id}/manual-audit` | `request_manual_audit()` | Move sentenca automatica para auditoria humana |
| `POST` | `/api/v7/ingestion/{ingestion_id}/confirm-sentence` | `confirm_sentence()` | Confirma a Sentenca de Capital com idempotencia |

### POST /api/v7/ingest

Entrada `multipart/form-data`:

- `file`: ZIP obrigatorio.
- `legacy_simulation_id`: opcional, usado apenas para calibracao GoldenEvaluator.

Resposta `202`: `IngestResponse`.

### GET /api/v7/ingestion/{ingestion_id}

Resposta: `IngestionDetail`, incluindo:

- `status`
- `llm_extracted_payload`
- `polars_calculations`
- `kill_reasons`
- `accuracy_score`
- `validation_metrics`
- metadados de auditoria e confirmacao

### POST /api/v7/ingestion/{ingestion_id}/manual-audit

Entrada: `ManualAuditRequest`.

Estados aceitos:

- `AUTONOMOUS_SENTENCED` aplica a auditoria e move para `PENDING_HUMAN_AUDIT`.
- `PENDING_HUMAN_AUDIT` e `MANUAL_ASSISTED` retornam idempotencia operacional.

### POST /api/v7/ingestion/{ingestion_id}/confirm-sentence

Entrada: `ConfirmSentenceRequest`.

Estados confirmaveis hoje:

- `AUTONOMOUS_SENTENCED`
- `PENDING_HUMAN_AUDIT`

Estados bloqueados:

- `UPLOADING`
- `INGESTING`
- `MANUAL_ASSISTED`
- `KILLED`
- `FAILED`

## WebMCP Experimental

**Arquivo:** `apps/backend/src/api/routes/webmcp.py`
**Registro:** somente quando `WEBMCP_ENABLED=true`.

WebMCP nao faz parte do caminho principal V7.0. Com a flag desligada, as rotas nao devem ser registradas.

| Metodo | Rota | Funcao | Descricao |
| --- | --- | --- | --- |
| `GET` | `/api/v7/openapi/schemas` | `get_openapi_schemas_b2b()` | Catalogo B2B/WebMCP experimental, disponivel apenas com `WEBMCP_ENABLED=true` |

## Compatibilidade

O backend ainda pode expor rotas historicas:

| Rota | Uso |
| --- | --- |
| `/calculate/quick` | Simulacao assincrona legada |
| `/simulation/{simulation_id}` | Consulta de simulacao legada |
| `/simulation/{simulation_id}/stream` | SSE legado para status de simulacao |
| `/simulations` e `/simulations/recent` | Portfolio baseado em simulacoes antigas |
| `/p1/analyze` | Screener historico |
| `/analyze/thesis` | Geracao de tese auxiliar |

Essas rotas sao mantidas para compatibilidade e calibracao, nao como narrativa principal V7.0.

## Arquitetura de Rotas

```text
main.py
|-- /health
|-- /me
|-- /api/v7/ingest
|-- /api/v7/ingestion/{id}
|-- /api/v7/ingestion/{id}/manual-audit
|-- /api/v7/ingestion/{id}/confirm-sentence
|-- /api/v7/webmcp/*           [experimental, flag]
|-- /calculate/quick           [compatibilidade]
|-- /simulation/*              [compatibilidade]
|-- /simulations*              [compatibilidade]
```
