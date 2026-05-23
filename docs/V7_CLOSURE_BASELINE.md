# VERTIV V7 Closure Baseline

> Baseline gerado para a Task 1 do fechamento VERTIV V7. Escopo: documentar o estado atual sem implementar codigo, sem alterar RLS e sem remover mudancas locais.

## 1. Estado atual do repositorio e branch

- Branch atual: `codex/finish-vertiv-v7`.
- Worktree: altamente modificado, com muitas alteracoes locais preexistentes e arquivos nao rastreados. Este baseline deve preservar esse estado.
- Arquivo criado nesta task: `docs/V7_CLOSURE_BASELINE.md`.
- Diagnostico `git status --short --branch` confirmou alteracoes em documentacao, frontend, backend, worker, testes, golden dataset, Supabase e configs.
- Arquivos nao rastreados relevantes ao fechamento:
  - `apps/backend/src/domain/ingestion_actions.py`
  - `apps/backend/tests/test_ingestion_action_endpoints.py`
  - `apps/backend/tests/test_ingestion_actions.py`
  - `apps/worker/tracer.py`
  - `docs/superpowers/`
  - `supabase/migrations/20260503_ingestion_action_audit.sql`
- Estado declarado em `.context/current_state.md`: V7 em Fase I dry run com `USE_MOCK=1`, RLS blindado, backend `/api/v7/openapi/schemas`, frontend com guard de UUID e servidores esperados em frontend `3002`, backend `8000`, worker `8001`.
- Estado publico ainda desalinhado: `README.md`, `package.json`, `apps/backend/src/api/main.py` e docs principais ainda vendem ou expõem identidade V6/v6.1.

## 2. Fluxos V7 que ja funcionam

### Identidade V7 interna

- `.context/current_state.md`, rota de ingestao e orquestrador ja descrevem o VERTIV V7 como fluxo Data Room ZIP -> IA extrai -> Diamond Core/Polars calcula -> GoldenEvaluator compara -> Sentenca.
- `apps/frontend/src/app/dashboard/upload/page.tsx` ja apresenta a jornada de upload do Data Room e valida ZIP/limite de tamanho/UUID de calibracao.

### Upload e ingestao

- `POST /api/v7/ingest` aceita apenas `.zip`, valida tamanho, valida ZIP malformado/suspeito, faz upload no bucket privado `data-rooms`, cria linha em `data_room_ingestions` com status `UPLOADING` e retorna `ingestion_id`.
- O upload usa cliente Supabase autenticado por JWT quando disponivel, preservando compatibilidade com RLS.
- `GET /api/v7/ingestion/{id}` retorna status, payload extraido, calculos Polars, kill reasons, score, metricas e metadados de acao humana.

### Worker e pipeline

- `apps/worker/worker_daemon.py` faz polling de linhas `UPLOADING`, tenta marcar como `INGESTING` e chama `IngestionOrchestrator`.
- `USE_MOCK=1` aciona `MockLLMProvider` e evita gasto de tokens para dry run.
- `IngestionOrchestrator` baixa o ZIP do Storage, extrai texto de arquivos texto/CSV/JSON/MD/XML e PDF quando `PyMuPDF` esta disponivel, chama mock ou router LLM real, executa Diamond Core via Polars/Python e atualiza status final.
- Diamond Core permanece separado da IA: a IA entrega dados; `_run_polars_engines` usa `CashFlowEngine`, `RealOptionsEngine`, `vertiv.biz.tropicalize` e funcoes de `core.main`.
- GoldenEvaluator e acionado quando `legacy_simulation_id` existe, mantendo calibracao contra historico.

### Fluxo humano parcial

- Backend possui acoes `REQUEST_MANUAL_AUDIT` e `CONFIRM_SENTENCE`.
- Migration `20260503_ingestion_action_audit.sql` adiciona metadados de solicitacao de auditoria e confirmacao de sentenca, alem de `data_room_ingestion_events` com idempotencia.
- Frontend de auditoria permite solicitar auditoria manual e confirmar sentenca para estados confirmaveis.
- Testes backend novos cobrem parte da maquina de estados e endpoints de acoes humanas.

### WebMCP experimental

- Backend registra rotas WebMCP somente quando `WEBMCP_ENABLED` esta habilitado.
- Frontend possui hook `useWebMCP` com `NEXT_PUBLIC_WEBMCP_ENABLED === "true"` como gate.
- Catalogo WebMCP exige usuario autenticado nas rotas atuais.

### Testes

- Existe spec V7 em `tests/e2e/v7_upload_audit_mock.spec.ts` cobrindo upload mockado, rejeicao de arquivo nao-ZIP, erros de acesso, polling terminal, solicitacao de auditoria manual e confirmacao de sentenca.
- Existem testes backend para `ingestion_actions` e endpoints de acao humana.

## 3. Lacunas bloqueantes para concluir produto

### Identidade V7

- `README.md` ainda declara `VERTIV v6.1.0-SINGULARITY`.
- `package.json` ainda usa `vertiv-v6-global`, versao `6.1.0` e descricao V6.
- `apps/backend/src/api/main.py` ainda declara titulo OpenAPI `VERTIV v6.0 API`, health `6.1.0-SINGULARITY` e modo `GLOBAL_EDITION`.
- Docs principais e varias telas ainda contem claims V6/v6.1/wizard. Isso bloqueia fechamento porque o produto publico nao fala V7 de forma consistente.

### LLM real

- `USE_MOCK=0` usa Gemini como provider real, mas o schema passado ao router e apenas um marcador generico `{type, version}`, sem schema Pydantic V7 completo antes do Diamond Core.
- `ClaudeProvider` esta como stub e levanta `NotImplementedError`; se Gemini falhar e `ANTHROPIC_API_KEY` estiver setada, o fallback produtivo pode falhar em runtime.
- Nao ha validacao Pydantic formal do retorno LLM antes de `_run_polars_engines`; coercoes ficam implicitamente em `sf()` e defaults do motor.

### Worker

- Claim do worker nao registra `attempt_count`, `worker_id`, `processing_started_at`, `processing_finished_at` ou `last_error`.
- Falhas marcam `FAILED` e `kill_reasons`, mas nao ha politica controlada de retry, requeue de linhas presas ou rastreabilidade operacional suficiente.
- `worker_daemon.py` e `IngestionOrchestrator.process()` ambos podem atualizar `INGESTING`, o que funciona, mas a semantica de fila ainda nao esta fechada.

### Fluxo humano

- `MANUAL_ASSISTED` ainda nao possui caminho completo de conclusao humana.
- `CONFIRM_SENTENCE` aceita `AUTONOMOUS_SENTENCED` e `PENDING_HUMAN_AUDIT`, mas bloqueia `MANUAL_ASSISTED` sem alternativa de `COMPLETE_MANUAL_REVIEW`.
- A tela de auditoria ainda nao tem painel para concluir revisao com verdict, notas e payload corrigido.

### Testes e gates

- `package.json` nao possui scripts `test:v7`, `test:v7:backend`, `test:v7:worker`, `test:v7:e2e` ou `verify:v7`.
- Testes antigos do wizard V6 continuam misturados com o gate geral E2E.
- `apps/worker/tests` nao existe no estado lido; faltam testes de schema LLM, roteamento de providers e semantica de fila.

### WebMCP

- Embora as flags estejam desligadas por padrao no codigo, nao ha documento de escopo V7.0 dedicado.
- Faltam testes que provem graceful degradation com WebMCP desligado, ausencia de `navigator.modelContext` e rotas nao registradas quando `WEBMCP_ENABLED=false`.

### Documentacao

- Documentacao principal ainda mistura V6, v6.1, wizard e claims de producao.
- Falta runbook V7 com operacao local/pre-producao, `USE_MOCK=1`, smoke `USE_MOCK=0`, bucket `data-rooms`, worker e troubleshooting.

## 4. Lacunas nao bloqueantes

- Wizard V6 pode permanecer como legado/calibracao se sair do fluxo principal e for isolado em documentacao/testes legacy.
- WebMCP pode permanecer experimental e fora do caminho principal da V7.0.
- SSE/rotas antigas de simulacao podem permanecer para compatibilidade, desde que a superficie V7 oficial fique clara.
- Claims de Agentic SEO e WebMCP declarativo no frontend podem continuar como experimento se estiverem atras de flags e sem quebrar UX principal.
- Load tests e documentos historicos V6 podem ficar no repositorio, desde que nao bloqueiem o gate V7.

## 5. Riscos tecnicos e de produto

- Risco de produto: README, docs e partes da UI ainda vendem V6/v6.1, criando narrativa inconsistente para demo e operacao.
- Risco de IA: `USE_MOCK=0` pode produzir payload fora do esperado ou cair em fallback Claude stub.
- Risco de calculo: sem schema formal, campos ausentes podem virar default silencioso no Diamond Core, mascarando extracao incompleta.
- Risco operacional: worker sem metadados de tentativa e sem requeue controlado dificulta diagnosticar linha presa ou falha intermitente.
- Risco de estado: `MANUAL_ASSISTED` e terminal para o usuario sem fluxo de revisao concluida.
- Risco de qualidade: gate V7 ainda nao esta separado do legado wizard, entao a release pode ser bloqueada por specs antigas ou passar sem cobrir worker/LLM.
- Risco de seguranca: qualquer ajuste futuro em Supabase deve ser aditivo e testado; RLS atual nao deve ser enfraquecido para acelerar fechamento.
- Risco de escopo: WebMCP pode parecer feature principal se a documentacao nao fechar explicitamente seu status experimental.

## 6. Lista objetiva de arquivos que devem entrar no fechamento

### Identidade V7 e documentacao publica

- `README.md`
- `package.json`
- `apps/backend/src/api/main.py`
- `docs/ARCHITECTURE.md`
- `docs/API_CONTRACT.md`
- `docs/BACKEND_API_MAP.md`
- `docs/GUIA_USUARIO.md`
- `docs/USER_MANUAL.md`
- `docs/MCP_SERVERS_DOCUMENTATION.md`
- `docs/V7_API_SURFACE.md`
- `docs/WEBMCP_V7_SCOPE.md`
- `docs/V7_RELEASE_RUNBOOK.md`
- `docs/V7_CLOSURE_REPORT.md`

### LLM real

- `apps/worker/src/providers/gemini.py`
- `apps/worker/src/providers/claude.py`
- `apps/worker/src/providers/router.py`
- `apps/worker/src/services/ingest_orchestrator.py`
- `apps/worker/src/schemas/v7_extraction.py`
- `apps/worker/tests/test_v7_extraction_schema.py`
- `apps/worker/tests/test_provider_router.py`

### Worker

- `apps/worker/worker_daemon.py`
- `apps/worker/src/services/ingest_orchestrator.py`
- `apps/worker/tests/test_worker_daemon_queue.py`
- `supabase/migrations/20260522_ingestion_queue_hardening.sql`
- `.env.example`

### Fluxo humano

- `apps/backend/src/domain/ingestion_actions.py`
- `apps/backend/src/api/routes/ingest.py`
- `apps/frontend/src/app/dashboard/audit/[id]/page.tsx`
- `apps/frontend/src/lib/api-client.ts`
- `apps/backend/tests/test_ingestion_actions.py`
- `apps/backend/tests/test_ingestion_action_endpoints.py`
- `supabase/migrations/20260503_ingestion_action_audit.sql`
- `supabase/migrations/20260522_manual_review_completion.sql`

### Testes e gate V7

- `package.json`
- `playwright.config.ts`
- `tests/e2e/README.md`
- `tests/e2e/v7_upload_audit_mock.spec.ts`
- Specs legacy em `tests/e2e/` que devem ser marcadas/isoladas como legado.

### WebMCP

- `apps/backend/src/api/routes/webmcp.py`
- `apps/backend/src/api/export_webmcp_schemas.py`
- `apps/frontend/src/hooks/useWebMCP.ts`
- `apps/frontend/src/lib/webmcp-tools.ts`
- `apps/frontend/src/lib/webmcp-types.ts`
- `docs/WEBMCP_V7_SCOPE.md`

## 7. Backlog direto vindo do diagnostico `rg`

- Harmonizar referencias V6/v6.1 em `README.md`, `package.json`, `docs/WHITE_PAPER.md`, `docs/USER_MANUAL.md`, `docs/GUIA_USUARIO.md`, `docs/MCP_SERVERS_DOCUMENTATION.md`, engines Python e telas de dashboard/relatorio.
- Isolar referencias `wizard` em testes E2E legados e docs de compatibilidade.
- Manter `USE_MOCK=1` como caminho confiavel de dry run.
- Fechar `USE_MOCK=0` para nao depender de stub.
- Completar `MANUAL_ASSISTED`.
- Fechar WebMCP como experimental, desligado por padrao, autenticado e documentado.

## 8. Criterio de entrada para as proximas tasks

- Este arquivo existe e registra o estado atual.
- A branch correta foi confirmada.
- Os fluxos V7 existentes foram separados das lacunas.
- As frentes obrigatorias foram explicitamente listadas: identidade V7, LLM real, worker, fluxo humano, testes, WebMCP e documentacao.
