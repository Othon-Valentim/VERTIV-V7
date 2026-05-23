# VERTIV V7 Fechamento Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformar o `VERTIV_V7` de prototipo operacional avancado em produto V7 concluido, harmonizado, verificavel e pronto para demonstracao/operacao controlada.

**Architecture:** Manter o monolito modular definido na constituicao V7: Next.js 14, FastAPI, worker Python, Supabase e Diamond Core em Python/Polars. A IA extrai dados; o Diamond Core calcula; o backend governa estado, auditoria e seguranca; o frontend exibe upload, triagem, sentenca e revisao humana.

**Tech Stack:** Next.js 14, TypeScript, FastAPI, Python, Pydantic, Polars, Supabase Auth/Storage/Postgres/RLS, Playwright, pytest.

---

## Diagnostico Executivo

O documento `C:\Users\Jussara Thomaz\Desktop\VERTIV\Vertiv\01. O QUE É O VERTIV V7 DEFINIÇÃO DO CODEX.md` define o V7 como um tribunal agentico de risco imobiliario. A base operacional ja existe: upload de ZIP, storage privado, linha `data_room_ingestions`, worker por polling, extracao mock/LLM, calculo Diamond Core, avaliacao Golden e tela de auditoria.

O fechamento nao deve reconstruir o produto. Deve eliminar o desalinhamento entre codigo, documentacao, testes e experiencia de produto. O V7 fica concluido quando:

- O produto inteiro fala V7, e a camada V6 aparece apenas como legado/calibracao.
- O caminho `USE_MOCK=1` continua confiavel para dry run.
- O caminho `USE_MOCK=0` fica explicitamente produtivo, com schema, fallback realista e observabilidade.
- O worker deixa de parecer experimento e passa a ter semantica de fila: claim, retry, falha rastreavel e recuperacao.
- `MANUAL_ASSISTED` deixa de ser beco sem saida e ganha fluxo humano ate fechamento.
- A suite de verificacao separa V7 de legado, roda em verde e vira gate de release.
- WebMCP fica com escopo fechado para V7.0: desligado por padrao, autenticado e documentado como experimental.

## Regras de Execucao

- Nao alterar RLS ja blindado sem uma razao objetiva e teste correspondente.
- Nao mover matematica financeira para IA.
- Nao criar microservicos.
- Nao tentar fechar WebMCP como feature principal da V7.0.
- Trabalhar em commits pequenos por frente.
- Antes de alterar arquivos com mudancas locais, ler o conteudo atual e preservar trabalho existente.

## Ordem Recomendada

1. Baseline e congelamento de estado.
2. Harmonizacao de identidade V7.
3. Contrato API/tipos V7.
4. Extracao LLM real.
5. Worker produtivo.
6. Fluxo humano completo.
7. UI final de auditoria/sentenca.
8. Testes e gates.
9. WebMCP V7.0 em modo experimental controlado.
10. Release runbook e validacao final.

---

### Task 1: Baseline de Fechamento

**Files:**
- Read: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\.context\current_state.md`
- Read: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\README.md`
- Read: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\package.json`
- Read: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\backend\src\api\routes\ingest.py`
- Read: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\worker\worker_daemon.py`
- Create: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\docs\V7_CLOSURE_BASELINE.md`

- [ ] **Step 1: Gerar inventario de estado**

Run:

```powershell
git status --short --branch
rg -n "v6|v6\.1|wizard|USE_MOCK|MANUAL_ASSISTED|WEBMCP|WebMCP" README.md docs apps package.json tests supabase -S
```

Expected:

- Lista de arquivos modificados preservada.
- Lista de referencias v6/wizard/WebMCP usada como backlog de harmonizacao.

- [ ] **Step 2: Criar documento de baseline**

Prompt especifico:

```text
Aja como auditor tecnico de fechamento do VERTIV V7. Leia o estado atual do repositorio, o documento de definicao V7 e os arquivos centrais de ingestao, worker, frontend upload/audit, migrations e testes. Crie docs/V7_CLOSURE_BASELINE.md com: estado atual, fluxos que ja funcionam, lacunas bloqueantes, lacunas nao bloqueantes, riscos, e lista objetiva de arquivos que devem entrar no fechamento. Nao implemente codigo. Nao altere RLS. Nao remova mudancas locais.
```

- [ ] **Step 3: Confirmar criterio de entrada**

Acceptance:

- `docs/V7_CLOSURE_BASELINE.md` existe.
- O documento lista explicitamente: identidade V7, LLM real, worker, fluxo humano, testes, WebMCP e documentacao.

Commit:

```powershell
git add docs/V7_CLOSURE_BASELINE.md
git commit -m "docs: establish V7 closure baseline"
```

---

### Task 2: Harmonizacao de Identidade V7

**Files:**
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\README.md`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\package.json`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\backend\src\api\main.py`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\docs\ARCHITECTURE.md`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\docs\API_CONTRACT.md`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\docs\BACKEND_API_MAP.md`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\docs\GUIA_USUARIO.md`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\docs\USER_MANUAL.md`

- [ ] **Step 1: Reescrever README como V7**

Prompt especifico:

```text
Reescreva o README do VERTIV_V7 para refletir o produto atual: VERTIV V7 como Tribunal Agentico de Risco Imobiliario. O README deve explicar o fluxo ZIP Data Room -> IA extrai -> Diamond Core/Polars calcula -> GoldenEvaluator compara -> Sentenca de Capital. Substitua linguagem v6.1/Singularity global por V7.0, mantendo V6 apenas como "legado de calibracao". Inclua Quick Start local com frontend 3002, backend 8000, worker 8001, USE_MOCK=1, Supabase e bucket data-rooms. Nao prometer recursos nao fechados. WebMCP deve aparecer como experimental por feature flag.
```

- [ ] **Step 2: Corrigir metadados de pacote e API**

Prompt especifico:

```text
Atualize package.json e apps/backend/src/api/main.py para que nome, descricao, titulo OpenAPI e health payload declarem VERTIV V7.0. Preserve scripts existentes, mas adicione scripts claros para dev:worker e test:v7 se ainda nao existirem. Nao quebrar scripts legados que ainda sejam usados.
```

- [ ] **Step 3: Alinhar documentacao principal**

Prompt especifico:

```text
Atualize docs/ARCHITECTURE.md, docs/API_CONTRACT.md, docs/BACKEND_API_MAP.md, docs/GUIA_USUARIO.md e docs/USER_MANUAL.md para refletir V7. Priorize o fluxo de ingestao Data Room, auditoria, sentenca e acao humana. Mova referencias ao wizard v6 para uma secao "Legado/compatibilidade" quando forem historicamente uteis. Remova claims de producao que o codigo nao sustenta.
```

- [ ] **Step 4: Verificar residuos publicos**

Run:

```powershell
rg -n "v6\.1|v6.1.0|VERTIV v6|wizard" README.md docs package.json apps/backend/src/api/main.py apps/frontend/src/app -S
```

Expected:

- As ocorrencias restantes devem estar em secoes de legado, calibracao ou compatibilidade.

Commit:

```powershell
git add README.md package.json apps/backend/src/api/main.py docs/ARCHITECTURE.md docs/API_CONTRACT.md docs/BACKEND_API_MAP.md docs/GUIA_USUARIO.md docs/USER_MANUAL.md
git commit -m "docs: harmonize product identity for V7"
```

---

### Task 3: Contrato API e Tipos V7

**Files:**
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\backend\src\api\routes\ingest.py`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\frontend\src\types\api.generated.ts`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\frontend\src\lib\api-client.ts`
- Create: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\docs\V7_API_SURFACE.md`

- [ ] **Step 1: Formalizar superficie V7**

Prompt especifico:

```text
Mapeie a superficie oficial da API V7. O contrato publico deve cobrir: POST /api/v7/ingest, GET /api/v7/ingestion/{id}, POST /api/v7/ingestion/{id}/manual-audit, POST /api/v7/ingestion/{id}/confirm-sentence e GET /api/v7/openapi/schemas. Gere docs/V7_API_SURFACE.md com payloads, respostas, codigos de erro e estados permitidos. Nao incluir endpoints wizard como fluxo principal.
```

- [ ] **Step 2: Regenerar tipos do frontend**

Prompt especifico:

```text
Regere ou ajuste apps/frontend/src/types/api.generated.ts para incluir os endpoints V7 de ingestao e acoes humanas. Se a geracao automatica nao estiver configurada, crie tipos TypeScript manuais em api-client.ts ou arquivo adjacente, mas mantenha nomes alinhados aos modelos FastAPI: IngestResponse, IngestionDetail, ManualAuditRequest, ConfirmSentenceRequest e IngestionActionResponse.
```

- [ ] **Step 3: Testar contrato local**

Run:

```powershell
cd apps/backend
pytest tests/test_ingestion_actions.py tests/test_ingestion_action_endpoints.py -q
```

Expected:

- Todos os testes de acoes humanas passam.

Commit:

```powershell
git add apps/backend/src/api/routes/ingest.py apps/frontend/src/types/api.generated.ts apps/frontend/src/lib/api-client.ts docs/V7_API_SURFACE.md
git commit -m "feat: formalize V7 ingestion API surface"
```

---

### Task 4: Extracao LLM Real de Producao

**Files:**
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\worker\src\providers\gemini.py`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\worker\src\providers\claude.py`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\worker\src\providers\router.py`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\worker\src\services\ingest_orchestrator.py`
- Create: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\worker\src\schemas\v7_extraction.py`
- Create: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\worker\tests\test_v7_extraction_schema.py`
- Create: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\worker\tests\test_provider_router.py`

- [ ] **Step 1: Criar schema Pydantic de extracao**

Prompt especifico:

```text
Crie um schema Pydantic V7 para a extracao agentica em apps/worker/src/schemas/v7_extraction.py. Ele deve cobrir os campos que ingest_orchestrator._run_polars_engines consome hoje: asking_price/land_cost, area_sqm/land_area_sqm, total_units, sales_price_avg/unit_price_avg, construction_cost_total, development_months, incc_annual_rate, ipca_annual_rate, use_ret_taxation, permuta_physical_pct, funding_model, green_premium, brown_discount, volatility, risk_free_rate, time_to_permit_years, is_in_app, has_contamination, has_adverse_possession_claims. Inclua defaults seguros somente quando a regra de negocio atual ja usa default; caso contrario permita null. Inclua metodo to_engine_payload() que retorna dict plano compativel com _run_polars_engines.
```

- [ ] **Step 2: Forcar validacao antes do Diamond Core**

Prompt especifico:

```text
Atualize ingest_orchestrator.py para validar o retorno da IA com V7ExtractionSchema antes de chamar _run_polars_engines. Se a validacao aplicar coercoes, salve normalization_logs em validation_metrics. Se a validacao falhar sem recuperacao, marque ingestion como FAILED com kill_reasons claras. Nao mover calculos financeiros para o provider LLM.
```

- [ ] **Step 3: Implementar Claude real ou retirar como fallback produtivo**

Prompt especifico:

```text
ClaudeProvider hoje e stub com NotImplementedError. Feche esta lacuna de uma das duas formas: implemente chamada real via anthropic SDK com tool_use/json estruturado e retries, ou remova Claude do fallback produtivo e documente que Gemini e o unico provider real da V7.0. A decisao deve impedir que USE_MOCK=0 falhe por cair em stub. Atualize tests para provar o comportamento.
```

- [ ] **Step 4: Testar roteamento sem gastar tokens**

Prompt especifico:

```text
Crie testes unitarios com providers falsos para provar: Gemini saudavel e usado primeiro; fallback so e chamado quando permitido; payload grande nao tenta provider menor; provider stub nao entra em producao; erros finais sao legiveis. Nao chamar APIs externas nos testes.
```

Run:

```powershell
cd apps/worker
pytest tests/test_v7_extraction_schema.py tests/test_provider_router.py -q
```

Expected:

- Testes passam sem rede e sem chaves LLM.

Commit:

```powershell
git add apps/worker/src/providers apps/worker/src/services/ingest_orchestrator.py apps/worker/src/schemas apps/worker/tests
git commit -m "feat: harden V7 real LLM extraction path"
```

---

### Task 5: Worker Produtivo e Semantica de Fila

**Files:**
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\worker\worker_daemon.py`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\worker\src\services\ingest_orchestrator.py`
- Create: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\supabase\migrations\20260522_ingestion_queue_hardening.sql`
- Create: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\worker\tests\test_worker_daemon_queue.py`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\.env.example`

- [ ] **Step 1: Adicionar metadados de fila**

Prompt especifico:

```text
Crie migration aditiva para data_room_ingestions com colunas: processing_started_at timestamptz, processing_finished_at timestamptz, worker_id text, attempt_count integer default 0, last_error text. Nao alterar politicas RLS. Nao alterar constraint de status, salvo se for estritamente necessario e coberto por teste.
```

- [ ] **Step 2: Tornar claim atomico e rastreavel**

Prompt especifico:

```text
Atualize worker_daemon.py para que o claim de uma ingestao UPLOADING incremente attempt_count, preencha processing_started_at e worker_id, e so processe linhas que conseguiu atualizar com status ainda UPLOADING. Em sucesso, preencha processing_finished_at. Em falha, status FAILED, last_error e kill_reasons devem ficar claros.
```

- [ ] **Step 3: Criar politica de retry controlada**

Prompt especifico:

```text
Adicione retry controlado no worker: MAX_WORKER_ATTEMPTS via env, default 2. Linhas UPLOADING sao processadas normalmente. Linhas FAILED nao devem ser reprocessadas automaticamente. Se uma linha ficar INGESTING alem de WORKER_STALE_MINUTES, permitir requeue apenas por funcao interna/testada, sem endpoint publico. Documente a operacao no runbook.
```

- [ ] **Step 4: Testar fila com cliente fake**

Run:

```powershell
cd apps/worker
pytest tests/test_worker_daemon_queue.py -q
```

Expected:

- Dois workers falsos nao processam a mesma linha.
- Falha registra `FAILED`, `last_error` e `kill_reasons`.
- Sucesso registra `processing_finished_at`.

Commit:

```powershell
git add apps/worker/worker_daemon.py apps/worker/src/services/ingest_orchestrator.py apps/worker/tests/test_worker_daemon_queue.py supabase/migrations/20260522_ingestion_queue_hardening.sql .env.example
git commit -m "feat: harden V7 ingestion worker queue"
```

---

### Task 6: Fluxo Humano Completo para MANUAL_ASSISTED

**Files:**
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\backend\src\domain\ingestion_actions.py`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\backend\src\api\routes\ingest.py`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\supabase\migrations\20260503_ingestion_action_audit.sql`
- Create: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\supabase\migrations\20260522_manual_review_completion.sql`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\backend\tests\test_ingestion_actions.py`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\backend\tests\test_ingestion_action_endpoints.py`

- [ ] **Step 1: Definir modelo de revisao humana**

Prompt especifico:

```text
Implemente o fechamento humano de MANUAL_ASSISTED sem criar microservico. Adicione action COMPLETE_MANUAL_REVIEW com payload: reviewer_verdict ("APPROVE_WITH_NOTES" | "REJECT" | "REQUEST_REUPLOAD"), notes, corrected_payload opcional, expected_status, idempotency_key. A action deve gravar evento auditavel e metadados na ingestao: manual_review_completed_at, manual_review_completed_by, manual_review_verdict, manual_review_notes. CONFIRM_SENTENCE deve continuar bloqueada para MANUAL_ASSISTED ate manual_review_completed_at existir e reviewer_verdict ser APPROVE_WITH_NOTES.
```

- [ ] **Step 2: Atualizar migration**

Prompt especifico:

```text
Crie migration aditiva para colunas de conclusao de revisao manual e atualize a tabela data_room_ingestion_events para aceitar COMPLETE_MANUAL_REVIEW. Nao remover colunas existentes. Nao mexer em RLS exceto se o novo evento ficar inacessivel; nesse caso, manter a mesma regra "usuario ve eventos da propria ingestao".
```

- [ ] **Step 3: Testar maquina de estados**

Run:

```powershell
cd apps/backend
pytest tests/test_ingestion_actions.py tests/test_ingestion_action_endpoints.py -q
```

Expected:

- `CONFIRM_SENTENCE` bloqueia `MANUAL_ASSISTED` sem revisao concluida.
- `COMPLETE_MANUAL_REVIEW` aceita `MANUAL_ASSISTED`.
- `CONFIRM_SENTENCE` aceita `MANUAL_ASSISTED` revisado com `APPROVE_WITH_NOTES`.
- `REJECT` e `REQUEST_REUPLOAD` nao confirmam sentenca.

Commit:

```powershell
git add apps/backend/src/domain/ingestion_actions.py apps/backend/src/api/routes/ingest.py apps/backend/tests/test_ingestion_actions.py apps/backend/tests/test_ingestion_action_endpoints.py supabase/migrations
git commit -m "feat: complete manual review flow for V7 ingestions"
```

---

### Task 7: UI Final de Auditoria, Sentenca e Review

**Files:**
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\frontend\src\app\dashboard\audit\[id]\page.tsx`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\frontend\src\lib\api-client.ts`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\tests\e2e\v7_upload_audit_mock.spec.ts`

- [ ] **Step 1: Transformar audit page em cockpit de fechamento**

Prompt especifico:

```text
Refatore a tela /dashboard/audit/[id] para funcionar como cockpit final da V7. Manter o visual institucional atual, mas organizar em secoes claras: Sentenca, Numeros Diamond Core, Evidencias IA, Calibracao Golden, Revisao Humana, Trilha de Auditoria. Para MANUAL_ASSISTED, exibir painel de revisao com textarea de notas, seletor de verdict e botao "Concluir Revisao". Para AUTONOMOUS_SENTENCED e PENDING_HUMAN_AUDIT, manter "Confirmar Sentenca". Estados KILLED/FAILED devem deixar claro que nao podem ser confirmados.
```

- [ ] **Step 2: Integrar COMPLETE_MANUAL_REVIEW**

Prompt especifico:

```text
Adicione completeManualReview() em api-client.ts e use na audit page com Idempotency-Key. Reutilize expected_status para concorrencia otimista. Mensagens de erro 409 devem ser amigaveis: status mudou, acao nao permitida ou revisao ausente.
```

- [ ] **Step 3: Cobrir E2E mockado**

Prompt especifico:

```text
Atualize tests/e2e/v7_upload_audit_mock.spec.ts para cobrir: MANUAL_ASSISTED mostra painel de revisao; COMPLETE_MANUAL_REVIEW com APPROVE_WITH_NOTES habilita confirmacao; KILLED/FAILED deixam botoes desabilitados; confirmacao fica idempotente apos sentence_confirmed_at.
```

Run:

```powershell
npm run test:e2e -- tests/e2e/v7_upload_audit_mock.spec.ts --project=chromium
```

Expected:

- O fluxo mockado upload -> audit continua passando.
- O fluxo manual assistido fica coberto.

Commit:

```powershell
git add apps/frontend/src/app/dashboard/audit/[id]/page.tsx apps/frontend/src/lib/api-client.ts tests/e2e/v7_upload_audit_mock.spec.ts
git commit -m "feat: finish V7 audit and manual review UI"
```

---

### Task 8: Suite Verde e Separacao Legado/V7

**Files:**
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\playwright.config.ts`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\package.json`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\tests\e2e\README.md`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\tests\e2e\v7_upload_audit_mock.spec.ts`
- Modify: legacy specs under `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\tests\e2e\`

- [ ] **Step 1: Definir gate V7**

Prompt especifico:

```text
Separe testes E2E em gate V7 e legado. O gate V7 deve rodar apenas specs que validam login essencial, upload Data Room, audit page, acoes humanas e contrato visual basico. Tests antigos do wizard v6 devem ficar marcados como legacy, com script separado, e nao podem quebrar o fechamento V7. Nao apagar testes legados sem justificativa no README.
```

- [ ] **Step 2: Scripts de verificacao**

Prompt especifico:

```text
Atualize package.json com scripts: test:v7, test:v7:e2e, test:v7:backend, test:v7:worker e verify:v7. verify:v7 deve executar backend tests, worker tests e Playwright V7 quando servidores estiverem ativos ou documentar claramente o requisito.
```

- [ ] **Step 3: Rodar gate**

Run:

```powershell
npm run test:v7:backend
npm run test:v7:worker
npm run test:v7:e2e
```

Expected:

- Gate V7 passa.
- Falhas legadas nao aparecem no gate de fechamento.

Commit:

```powershell
git add package.json playwright.config.ts tests/e2e/README.md tests/e2e
git commit -m "test: define green V7 release gate"
```

---

### Task 9: WebMCP com Escopo Fechado para V7.0

**Files:**
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\backend\src\api\routes\webmcp.py`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\backend\src\api\export_webmcp_schemas.py`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\apps\frontend\src\hooks\useWebMCP.ts`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\docs\MCP_SERVERS_DOCUMENTATION.md`
- Create: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\docs\WEBMCP_V7_SCOPE.md`

- [ ] **Step 1: Fixar decisao V7.0**

Prompt especifico:

```text
Feche WebMCP como experimental para V7.0. Garanta que WEBMCP_ENABLED e NEXT_PUBLIC_WEBMCP_ENABLED sejam false por padrao. O catalogo deve ser autenticado e nao deve prometer mais ferramentas do que as realmente implementadas. Crie docs/WEBMCP_V7_SCOPE.md explicando: escopo, flags, riscos, ferramentas suportadas, e criterio para V7.1.
```

- [ ] **Step 2: Testar graceful degradation**

Prompt especifico:

```text
Adicione ou ajuste testes para provar que a aplicacao funciona com WebMCP desligado, que rotas WebMCP nao sao registradas quando WEBMCP_ENABLED=false, e que o frontend nao quebra quando window.modelContext nao existe.
```

Commit:

```powershell
git add apps/backend/src/api/routes/webmcp.py apps/backend/src/api/export_webmcp_schemas.py apps/frontend/src/hooks/useWebMCP.ts docs/MCP_SERVERS_DOCUMENTATION.md docs/WEBMCP_V7_SCOPE.md
git commit -m "docs: lock WebMCP scope for V7"
```

---

### Task 10: Release Runbook e Validacao Final

**Files:**
- Create: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\docs\V7_RELEASE_RUNBOOK.md`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\.env.example`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\docker-compose.yml`
- Modify: `C:\Users\Jussara Thomaz\Documents\VERTIV_V7\DEPLOY_VERCEL.md`

- [ ] **Step 1: Criar runbook operacional**

Prompt especifico:

```text
Crie docs/V7_RELEASE_RUNBOOK.md com procedimento de operacao local e pre-producao: variaveis de ambiente, Supabase migrations, bucket data-rooms, comandos para frontend/backend/worker, dry run USE_MOCK=1, smoke test USE_MOCK=0, como usar UUID de calibracao, como confirmar sentenca, como concluir revisao manual, como diagnosticar falha no worker e como desligar WebMCP.
```

- [ ] **Step 2: Validacao final dry run**

Run:

```powershell
npm run build
npm run test:v7:backend
npm run test:v7:worker
npm run test:v7:e2e
```

Expected:

- Build passa.
- Gate V7 passa.
- O produto roda localmente com `USE_MOCK=1`.

- [ ] **Step 3: Smoke real controlado**

Prompt especifico:

```text
Execute smoke test controlado com USE_MOCK=0 usando um Data Room pequeno e seguro. Nao usar dados sensiveis reais. Validar que Gemini ou provider produtivo retorna JSON validado por Pydantic, que Diamond Core calcula, que a tela de auditoria abre, e que erro de provider aparece como FAILED legivel caso a chave esteja ausente ou invalida.
```

- [ ] **Step 4: Criar relatorio de fechamento**

Create:

`C:\Users\Jussara Thomaz\Documents\VERTIV_V7\docs\V7_CLOSURE_REPORT.md`

Prompt especifico:

```text
Crie docs/V7_CLOSURE_REPORT.md com: resumo do que foi fechado, criterios de aceite atendidos, comandos rodados e resultado, riscos residuais, decisoes de escopo, e proximos passos pos-V7.0. O documento deve ser executivo e tecnico, sem prometer features fora do que passou no gate.
```

Commit:

```powershell
git add docs/V7_RELEASE_RUNBOOK.md docs/V7_CLOSURE_REPORT.md .env.example docker-compose.yml DEPLOY_VERCEL.md
git commit -m "docs: add V7 release runbook and closure report"
```

---

## Prompts Mestres por Modo de Trabalho

### Prompt Mestre: Executor de Frente

```text
Voce esta fechando o VERTIV V7, nao redesenhando o produto. Siga a frente indicada do plano docs/superpowers/plans/2026-05-22-fechamento-vertiv-v7.md. Antes de editar, leia os arquivos citados. Preserve mudancas locais nao relacionadas. Nao altere RLS salvo instrucao explicita da tarefa. Nao mova calculo financeiro para IA. Entregue codigo pequeno, teste correspondente e verificacao. Ao final, resuma arquivos alterados, testes rodados e riscos residuais.
```

### Prompt Mestre: Revisor Tecnico

```text
Aja como revisor senior do fechamento VERTIV V7. Compare a alteracao com a definicao do produto: tribunal agentico de risco imobiliario, Diamond Core intocavel, monolito modular, Supabase com RLS, WebMCP experimental. Procure bugs, regressao de seguranca, claims falsos, falta de teste, status de ingestao inconsistente e risco de quebrar dry run USE_MOCK=1. Responda com findings por severidade e referencias de arquivo/linha.
```

### Prompt Mestre: QA de Produto

```text
Valide o VERTIV V7 como usuario operador. Execute o fluxo: login, upload ZIP, aguardar audit, ler sentenca, solicitar auditoria manual, concluir revisao quando aplicavel, confirmar sentenca e exportar/printar relatorio. Registre falhas de texto, botoes desabilitados indevidamente, estados sem saida, mensagens tecnicas demais e inconsistencias V6/V7. Nao sugerir features novas; foque em fechamento.
```

### Prompt Mestre: Harmonizacao de Copy e Documentacao

```text
Revise textos publicos do VERTIV_V7 para consistencia. A linguagem deve dizer VERTIV V7, Tribunal Agentico de Risco Imobiliario, Data Room, Diamond Core, Sentenca de Capital e trilha de auditoria. V6 so pode aparecer como legado/calibracao. Remova promessas de recursos nao implementados. O resultado deve ser claro para investidor, operador e engenheiro.
```

---

## Definition of Done V7.0

- `README.md`, `package.json`, OpenAPI e docs principais declaram V7.
- Fluxo `USE_MOCK=1` funciona de ponta a ponta com ZIP golden.
- Fluxo `USE_MOCK=0` nao depende de provider stub.
- Worker tem claim rastreavel, tentativa, erro legivel e finalizacao.
- `AUTONOMOUS_SENTENCED`, `PENDING_HUMAN_AUDIT`, `MANUAL_ASSISTED`, `KILLED` e `FAILED` possuem comportamento de UI e backend definido.
- `MANUAL_ASSISTED` tem caminho humano ate conclusao ou rejeicao.
- Confirmacao de sentenca e revisao humana possuem evento auditavel e idempotencia.
- Gate `test:v7` passa.
- Testes legados do wizard nao bloqueiam release V7.
- WebMCP fica desligado por padrao e documentado como experimental.
- `docs/V7_RELEASE_RUNBOOK.md` e `docs/V7_CLOSURE_REPORT.md` existem.

## Riscos Residuals Aceitaveis para V7.0

- WebMCP nao ser feature principal.
- Wizard v6 permanecer no codigo como legado, desde que nao seja fluxo principal/documentado como V7.
- Smoke `USE_MOCK=0` depender de chave externa; se a chave estiver ausente, o erro deve ser controlado e auditavel.

## Riscos Nao Aceitaveis

- README ou UI principal ainda venderem v6.1 como produto atual.
- `USE_MOCK=0` cair em `NotImplementedError`.
- `MANUAL_ASSISTED` nao ter saida operacional.
- Teste de release depender de specs antigas do wizard quebradas.
- RLS ser enfraquecido para "fazer funcionar".
