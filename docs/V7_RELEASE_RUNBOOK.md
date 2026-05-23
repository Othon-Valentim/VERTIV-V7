# VERTIV V7 Release Runbook

## Objetivo

Operar e validar o VERTIV V7 como produto fechado em ambiente local ou
pre-producao controlada. O fluxo principal e:

`ZIP Data Room -> Supabase Storage -> worker -> IA/mock -> Diamond Core -> auditoria -> revisao humana -> confirmacao de sentenca`.

## Variaveis Obrigatorias

Base:

```env
ENV=development
API_URL=http://localhost:8000
BASE_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
ALLOWED_ORIGINS=https://vertiv.tech,http://localhost:3000
```

Supabase:

```env
SUPABASE_URL=...
SUPABASE_KEY=...
SUPABASE_JWT_SECRET=...
SUPABASE_SERVICE_ROLE_KEY=...
```

Worker:

```env
USE_MOCK=1
WORKER_ID=local-worker-1
WORKER_POLL_INTERVAL_SECONDS=3
MAX_WORKER_ATTEMPTS=2
WORKER_STALE_MINUTES=30
```

LLM real:

```env
GOOGLE_API_KEY=...
```

WebMCP experimental:

```env
WEBMCP_ENABLED=false
NEXT_PUBLIC_WEBMCP_ENABLED=false
```

## Supabase

1. Aplicar migrations em ordem.
2. Confirmar que o bucket privado `data-rooms` existe.
3. Confirmar RLS em `data_room_ingestions`, `data_room_ingestion_events` e objetos do bucket.
4. Nao enfraquecer RLS para smoke tests. Use usuario autenticado e service role apenas no worker.

Migrations relevantes do fechamento:

- `20260219_data_room_ingestions.sql`
- `20260503_ingestion_action_audit.sql`
- `20260522_ingestion_queue_hardening.sql`
- `20260522_manual_review_completion.sql`

## Operacao Local

Instalar dependencias:

```bash
npm install
npm run playwright:install
```

Subir servicos em terminais separados:

```bash
npm run dev:frontend
npm run dev:backend
npm run dev:worker
```

URLs esperadas:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Worker: `http://localhost:8001` quando rodado como servidor auxiliar

## Dry Run USE_MOCK=1

1. Definir `USE_MOCK=1`.
2. Subir frontend, backend e worker.
3. Fazer login.
4. Abrir `/dashboard/upload`.
5. Enviar ZIP pequeno de teste, sem dados sensiveis.
6. Aguardar a pagina `/dashboard/audit/<ingestion_id>`.
7. Confirmar que a tela mostra numeros Diamond Core, evidencias IA, calibracao Golden e sentenca.
8. Validar acoes:
   - `Auditoria Manual` para `AUTONOMOUS_SENTENCED`;
   - `Concluir Revisao` para `MANUAL_ASSISTED`;
   - `Confirmar Sentenca` quando permitido;
   - botoes bloqueados em `KILLED` e `FAILED`.

## Smoke USE_MOCK=0

Use apenas Data Room pequeno, controlado e sem dados sensiveis.

1. Definir `USE_MOCK=0`.
2. Definir `GOOGLE_API_KEY`.
3. Reiniciar o worker.
4. Fazer upload de ZIP de teste.
5. Confirmar que o provider Gemini retorna JSON validado por schema Pydantic.
6. Confirmar que o Diamond Core calcula e grava `polars_calculations`.
7. Abrir `/dashboard/audit/<ingestion_id>`.
8. Se a chave estiver ausente ou invalida, a ingestao deve terminar como `FAILED`, com `last_error` e `kill_reasons` legiveis. Nao deve cair em stub Claude.

## UUID de Calibracao

Use o `ingestion_id` retornado por `POST /api/v7/ingest` como identificador de rastreio. Ele conecta:

- objeto no bucket `data-rooms`;
- linha em `data_room_ingestions`;
- eventos em `data_room_ingestion_events`;
- URL `/dashboard/audit/<ingestion_id>`.

## Diagnostico do Worker

Campos principais em `data_room_ingestions`:

- `status`
- `worker_id`
- `attempt_count`
- `processing_started_at`
- `processing_finished_at`
- `last_error`
- `kill_reasons`

Leitura operacional:

- `UPLOADING`: aguardando claim do worker.
- `INGESTING`: worker processando.
- `AUTONOMOUS_SENTENCED`: sentenca automatica pronta.
- `PENDING_HUMAN_AUDIT`: auditoria manual solicitada.
- `MANUAL_ASSISTED`: revisao humana obrigatoria.
- `FAILED`: falha controlada, verificar `last_error`.
- `KILLED`: regra fatal, sem confirmacao de sentenca.

## WebMCP

V7.0 deve operar com WebMCP desligado:

```env
WEBMCP_ENABLED=false
NEXT_PUBLIC_WEBMCP_ENABLED=false
```

Para experimento controlado:

1. Ativar as duas flags.
2. Reiniciar backend e frontend.
3. Usar usuario autenticado.
4. Confirmar que o catalogo publica somente `simulate_what_if` e `highlight_pdf_evidence`.

Rollback: voltar ambas as flags para `false` e reiniciar servicos.

## Gates

Com frontend ativo em `http://localhost:3000`:

```bash
npm run build
npm run test:v7
```

`npm run test:v7` executa:

- backend: ingestao, acoes humanas e escopo WebMCP;
- worker: schema de extracao, router, orquestrador e fila;
- E2E: upload mockado ate auditoria, revisao humana e confirmacao idempotente.

## Promocao

Antes de promover:

1. Gate V7 verde.
2. `.env` revisado sem secrets commitados.
3. Supabase com migrations aplicadas.
4. Bucket `data-rooms` privado.
5. `USE_MOCK=1` validado.
6. Smoke `USE_MOCK=0` executado ou registrado como pendente por falta de chave/Data Room seguro.
7. WebMCP desligado por padrao.
