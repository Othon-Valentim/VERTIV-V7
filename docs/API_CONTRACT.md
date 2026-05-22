# VERTIV V7.0 API Contract

Este contrato descreve a superficie publica do VERTIV V7.0: ingestao de Data Room, consulta de sentenca e acoes humanas auditaveis.

**Base local:** `http://localhost:8000`
**Autenticacao:** JWT Bearer Token do Supabase para rotas protegidas
**Fluxo oficial:** ZIP Data Room -> IA extrai -> Diamond Core/Polars calcula -> GoldenEvaluator compara -> Sentenca de Capital

## Autenticacao

```http
Authorization: Bearer <jwt>
```

## Health

```http
GET /health
```

Resposta:

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

## Upload de Data Room

```http
POST /api/v7/ingest
Content-Type: multipart/form-data
```

Campos:

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `file` | `.zip` | Sim | Data Room do ativo |
| `legacy_simulation_id` | string | Nao | UUID historico para calibracao GoldenEvaluator |

Resposta `202`:

```json
{
  "ingestion_id": "uuid",
  "status": "UPLOADING",
  "message": "Data room aceito. Aguardando processamento agentico."
}
```

Erros comuns:

| Codigo | Motivo |
| ---: | --- |
| `400` | Arquivo nao e ZIP ou ZIP invalido |
| `401` | JWT ausente/invalido |
| `413` | Arquivo ou conteudo descompactado excede limites |
| `500` | Falha interna ao gravar ou registrar ingestao |

## Consultar Ingestao

```http
GET /api/v7/ingestion/{ingestion_id}
```

Resposta:

```json
{
  "id": "uuid",
  "status": "AUTONOMOUS_SENTENCED",
  "raw_storage_url": "data-rooms/user/id/data-room.zip",
  "llm_extracted_payload": {},
  "polars_calculations": {},
  "kill_reasons": [],
  "legacy_simulation_id": "uuid",
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

Estados permitidos:

- `UPLOADING`
- `INGESTING`
- `AUTONOMOUS_SENTENCED`
- `PENDING_HUMAN_AUDIT`
- `MANUAL_ASSISTED`
- `KILLED`
- `FAILED`

## Solicitar Auditoria Humana

```http
POST /api/v7/ingestion/{ingestion_id}/manual-audit
Content-Type: application/json
Idempotency-Key: <opcional>
```

Request:

```json
{
  "reason": "Revisar premissas de area e custo.",
  "expected_status": "AUTONOMOUS_SENTENCED",
  "idempotency_key": "client-key"
}
```

Resposta:

```json
{
  "ingestion_id": "uuid",
  "action": "REQUEST_MANUAL_AUDIT",
  "action_status": "applied",
  "previous_status": "AUTONOMOUS_SENTENCED",
  "current_status": "PENDING_HUMAN_AUDIT",
  "audit_event_id": "uuid",
  "manual_audit_requested_at": "2026-05-22T00:00:00Z",
  "sentence_confirmed_at": null,
  "sentence_confirmed_by": null,
  "updated_at": "2026-05-22T00:00:00Z"
}
```

## Confirmar Sentenca

```http
POST /api/v7/ingestion/{ingestion_id}/confirm-sentence
Content-Type: application/json
Idempotency-Key: <opcional>
```

Request:

```json
{
  "accepted": true,
  "notes": "Sentenca revisada e aceita.",
  "expected_status": "AUTONOMOUS_SENTENCED",
  "decision_snapshot_hash": "sha256-opcional",
  "idempotency_key": "client-key"
}
```

Resposta:

```json
{
  "ingestion_id": "uuid",
  "action": "CONFIRM_SENTENCE",
  "action_status": "applied",
  "previous_status": "AUTONOMOUS_SENTENCED",
  "current_status": "AUTONOMOUS_SENTENCED",
  "audit_event_id": "uuid",
  "manual_audit_requested_at": null,
  "sentence_confirmed_at": "2026-05-22T00:00:00Z",
  "sentence_confirmed_by": "user-id",
  "updated_at": "2026-05-22T00:00:00Z"
}
```

Regras:

- `accepted` deve ser `true`.
- A sentenca precisa ter calculos Polars.
- `KILLED` e `FAILED` nao permitem confirmacao.
- `MANUAL_ASSISTED` ainda exige fluxo humano completo em task posterior.
- Repeticoes com a mesma chave de idempotencia retornam `idempotent_noop`.

## Catalogo B2B/WebMCP Experimental

```http
GET /api/v7/openapi/schemas
```

Este endpoint e condicional. Ele so e registrado quando `WEBMCP_ENABLED=true`, porque fica no roteador experimental WebMCP. Com a flag desligada, que e o padrao V7.0, a rota nao deve estar disponivel.

Quando habilitado, retorna schemas para integracoes B2B/WebMCP controladas. Ele nao faz parte do fluxo principal de ingestao, sentenca ou acao humana.

## Legado/Compatibilidade

Rotas como `/calculate/quick`, `/simulation/{id}` e `/simulations` podem existir para compatibilidade com simulacoes anteriores. Elas nao sao o fluxo principal V7.0 e nao substituem ingestao de Data Room.
