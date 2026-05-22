# VERTIV V7 API Surface

Este documento fixa a superficie V7 oficial para ingestao de Data Room e acoes humanas. Rotas historicas de simulacao e wizard ficam fora deste contrato, exceto como legado/calibracao em documentos separados.

**Base local:** `http://localhost:8000`
**Prefixo V7:** `/api/v7`
**Autenticacao:** `Authorization: Bearer <jwt>` do Supabase
**Storage/Dados:** Supabase Auth, Storage bucket `data-rooms` e Postgres com RLS existente

## Estados Permitidos

| Estado | Significado | Terminal |
| --- | --- | --- |
| `UPLOADING` | ZIP aceito e linha criada para processamento | Nao |
| `INGESTING` | Worker esta extraindo e calculando | Nao |
| `AUTONOMOUS_SENTENCED` | Sentenca gerada automaticamente com calculos | Nao |
| `PENDING_HUMAN_AUDIT` | Usuario solicitou auditoria manual | Nao |
| `MANUAL_ASSISTED` | Pipeline exige assistencia humana antes de fechar | Nao |
| `KILLED` | Ingestao encerrada por criterio de corte | Sim |
| `FAILED` | Falha tecnica ou operacional | Sim |

## Modelo de Erro

O backend usa respostas FastAPI padrao:

```json
{
  "detail": "Mensagem do erro"
}
```

Erros de validacao Pydantic usam `detail` como lista de itens com `loc`, `msg` e `type`.

## POST /api/v7/ingest

Recebe um ZIP de Data Room, valida tamanho/formato, grava no bucket privado `data-rooms` e cria a ingestao com status `UPLOADING`.

### Request

`Content-Type: multipart/form-data`

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `file` | `.zip` | Sim | Data Room do ativo. Apenas arquivos `.zip` sao aceitos. |
| `legacy_simulation_id` | string | Nao | UUID historico usado somente para calibracao GoldenEvaluator. |

### Resposta 202 `IngestResponse`

```json
{
  "ingestion_id": "8b179d3f-7f69-4b73-91f6-580c0f9fd92b",
  "status": "UPLOADING",
  "message": "Data room aceito. Aguardando processamento agentico."
}
```

### Erros

| Codigo | Quando ocorre |
| ---: | --- |
| `400` | Arquivo sem extensao `.zip`, ZIP invalido, `Content-Length` invalido ou ZIP suspeito |
| `401` | JWT ausente ou invalido |
| `413` | Upload, quantidade de entradas ou tamanho descompactado acima do limite |
| `422` | Payload multipart invalido |
| `500` | Falha interna ao armazenar arquivo ou criar registro |

## GET /api/v7/ingestion/{ingestion_id}

Retorna o estado completo da ingestao do usuario autenticado. O acesso e limitado por usuario e pela RLS existente.

### Resposta 200 `IngestionDetail`

```json
{
  "id": "8b179d3f-7f69-4b73-91f6-580c0f9fd92b",
  "status": "AUTONOMOUS_SENTENCED",
  "raw_storage_url": "data-rooms/user-id/ingestion-id/data-room.zip",
  "llm_extracted_payload": {},
  "polars_calculations": {},
  "kill_reasons": [],
  "legacy_simulation_id": null,
  "accuracy_score": 0.91,
  "validation_metrics": {},
  "manual_audit_requested_at": null,
  "manual_audit_requested_by": null,
  "sentence_confirmed_at": null,
  "sentence_confirmed_by": null,
  "sentence_confirmation_notes": null,
  "created_at": "2026-05-22T00:00:00Z",
  "updated_at": "2026-05-22T00:00:00Z"
}
```

### Erros

| Codigo | Quando ocorre |
| ---: | --- |
| `401` | JWT ausente ou invalido |
| `404` | Ingestao inexistente ou de outro usuario |
| `422` | `ingestion_id` invalido para o roteamento |
| `500` | Falha interna ao consultar ingestao |

## POST /api/v7/ingestion/{ingestion_id}/manual-audit

Solicita auditoria humana para uma sentenca automatica. A acao e auditavel e aceita chave de idempotencia via header ou body.

### Request `ManualAuditRequest`

Headers opcionais:

```http
Idempotency-Key: client-generated-key
```

Body:

```json
{
  "reason": "Revisar premissas de area e custo.",
  "expected_status": "AUTONOMOUS_SENTENCED",
  "idempotency_key": "client-generated-key"
}
```

### Regras de estado

| Status atual | Resultado |
| --- | --- |
| `AUTONOMOUS_SENTENCED` | Aplica a acao e move para `PENDING_HUMAN_AUDIT` |
| `PENDING_HUMAN_AUDIT` | Retorna `idempotent_noop` |
| `MANUAL_ASSISTED` | Retorna `idempotent_noop` |
| `UPLOADING` ou `INGESTING` | Bloqueia com `409` |
| `KILLED` ou `FAILED` | Bloqueia com `409` |

### Resposta 200 `IngestionActionResponse`

```json
{
  "ingestion_id": "8b179d3f-7f69-4b73-91f6-580c0f9fd92b",
  "action": "REQUEST_MANUAL_AUDIT",
  "action_status": "applied",
  "previous_status": "AUTONOMOUS_SENTENCED",
  "current_status": "PENDING_HUMAN_AUDIT",
  "audit_event_id": "3f8a2f75-9501-4e83-97b4-66d1d8e3b4bd",
  "manual_audit_requested_at": "2026-05-22T00:00:00Z",
  "sentence_confirmed_at": null,
  "sentence_confirmed_by": null,
  "updated_at": "2026-05-22T00:00:00Z"
}
```

### Erros

| Codigo | Quando ocorre |
| ---: | --- |
| `401` | JWT ausente ou invalido |
| `404` | Ingestao inexistente ou de outro usuario |
| `409` | `expected_status` diverge, status mudou antes do update ou acao nao permitida |
| `422` | Body invalido |
| `500` | Falha interna ao registrar acao |

## POST /api/v7/ingestion/{ingestion_id}/confirm-sentence

Confirma a Sentenca de Capital. A acao nao muda o status de negocio; ela grava metadados de confirmacao e evento auditavel.

### Request `ConfirmSentenceRequest`

Headers opcionais:

```http
Idempotency-Key: client-generated-key
```

Body:

```json
{
  "accepted": true,
  "notes": "Sentenca revisada e aceita.",
  "expected_status": "AUTONOMOUS_SENTENCED",
  "decision_snapshot_hash": "sha256-opcional",
  "idempotency_key": "client-generated-key"
}
```

### Regras de estado

| Status atual | Resultado |
| --- | --- |
| `AUTONOMOUS_SENTENCED` | Confirma se `polars_calculations` existir |
| `PENDING_HUMAN_AUDIT` | Confirma se `polars_calculations` existir |
| Ja confirmado | Retorna `idempotent_noop` |
| `MANUAL_ASSISTED` | Bloqueia com `409` nesta etapa do fechamento |
| `UPLOADING` ou `INGESTING` | Bloqueia com `409` |
| `KILLED` ou `FAILED` | Bloqueia com `409` |

`accepted` deve ser `true`; `false` retorna erro de validacao.

### Resposta 200 `IngestionActionResponse`

```json
{
  "ingestion_id": "8b179d3f-7f69-4b73-91f6-580c0f9fd92b",
  "action": "CONFIRM_SENTENCE",
  "action_status": "applied",
  "previous_status": "AUTONOMOUS_SENTENCED",
  "current_status": "AUTONOMOUS_SENTENCED",
  "audit_event_id": "3f8a2f75-9501-4e83-97b4-66d1d8e3b4bd",
  "manual_audit_requested_at": null,
  "sentence_confirmed_at": "2026-05-22T00:00:00Z",
  "sentence_confirmed_by": "user-id",
  "updated_at": "2026-05-22T00:00:00Z"
}
```

### Erros

| Codigo | Quando ocorre |
| ---: | --- |
| `401` | JWT ausente ou invalido |
| `404` | Ingestao inexistente ou de outro usuario |
| `409` | `expected_status` diverge, status nao permite confirmacao, sentenca sem calculos Polars ou status mudou durante a acao |
| `422` | Body invalido ou `accepted` diferente de `true` |
| `500` | Falha interna ao confirmar sentenca |

## Secao Condicional Experimental: WEBMCP_ENABLED=true

`GET /api/v7/openapi/schemas` nao e rota oficial sempre ativa da superficie principal. Ela fica no router experimental WebMCP e so e registrada quando `WEBMCP_ENABLED=true` no backend.

Com `WEBMCP_ENABLED=false`, que e o padrao V7.0, a rota nao deve existir.

Quando habilitada, exige JWT e retorna catalogo de ferramentas/schema para integracoes B2B/WebMCP controladas:

```http
GET /api/v7/openapi/schemas
Authorization: Bearer <jwt>
```

Resposta resumida:

```json
{
  "version": "7.0.0-SINGULARITY",
  "protocol": "openapi-b2b-v7",
  "tools": [],
  "context_policy": {
    "max_fields": 5,
    "allowed_fields": [
      "project_id",
      "current_vpl",
      "current_irr",
      "role",
      "active_step"
    ]
  },
  "description": "VERTIV Real Estate Analysis Platform - deterministic NPV/IRR engine with legal due diligence.",
  "documentation": "https://vertiv.tech/docs/api"
}
```

Esta rota nao substitui `POST /api/v7/ingest`, `GET /api/v7/ingestion/{id}` nem as acoes humanas.
