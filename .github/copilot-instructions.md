# Copilot / AI Agent Instructions — VERTIV v6.0

Short actionable guide to get an AI coding agent productive in this repository.

Overview
- Modular monolith: Next.js frontend (`apps/frontend`), FastAPI backend (`apps/backend/src`), and a Python worker (`apps/worker`).
- Runtimes: Python 3.10+ (backend/worker), Node 18+ (frontend).

Architecture & data flow (concise)
- Frontend: UI and shared TypeScript types in `packages/shared/src`.
- Backend: FastAPI app at [apps/backend/src/api/main.py](apps/backend/src/api/main.py). Domain schemas: [apps/backend/src/domain/schemas.py](apps/backend/src/domain/schemas.py).
- Worker: long-running financial engine at [apps/worker/core/main.py](apps/worker/core/main.py). The worker consumes tasks enqueued by the API and writes results to Supabase.
- Task dispatch: see [apps/backend/src/services/task_queue.py](apps/backend/src/services/task_queue.py) — worker listens for `/tasks/process-simulation` style targets.

Key files to check immediately
- API entry: [apps/backend/src/api/main.py](apps/backend/src/api/main.py)
- Task queue: [apps/backend/src/services/task_queue.py](apps/backend/src/services/task_queue.py)
- Worker entry + sanitizer: [apps/worker/core/main.py](apps/worker/core/main.py)
- Schemas: [apps/backend/src/domain/schemas.py](apps/backend/src/domain/schemas.py)
- LLM template: [apps/backend/src/services/llm_service.py](apps/backend/src/services/llm_service.py)
- Supabase DB client: [apps/backend/src/infrastructure/database.py](apps/backend/src/infrastructure/database.py)

Developer workflows (concrete commands)
- Backend (Windows PowerShell):
  ```powershell
  cd apps/backend
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  $env:SUPABASE_URL = "<your_url>"
  $env:SUPABASE_KEY = "<your_key>"
  $env:PYTHONPATH = (Get-Location).Path
  uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
  ```
- Worker (dev): set `PYTHONPATH` to `apps/backend` so worker can import backend `src.*` modules. Example (Unix):
  ```bash
  export PYTHONPATH=$PWD/apps/backend
  cd apps/worker
  pip install -r requirements.txt
  uvicorn apps.worker.core.main:app --reload --port 8100
  ```
- Frontend: `cd apps/frontend && npm install && npm run dev`
- Tests: run `pytest` under `apps/backend/tests` using same environment where `PYTHONPATH` allows `src.*` imports.

Project-specific conventions (must-follow)
- Import namespace: backend code uses `src.*` imports. Always set `PYTHONPATH` or run from package root.
- Pydantic-first: change schemas in [apps/backend/src/domain/schemas.py](apps/backend/src/domain/schemas.py) carefully — consumers (worker/frontend) rely on stable shapes.
- Serialization: when modifying engine outputs update `sanitize_payload()` in [apps/worker/core/main.py](apps/worker/core/main.py) and usages of `P10FinancialOutput` to ensure JSON-serializable results.
- LLM: `LLMService.generate_investment_thesis()` is stubbed/deterministic; preserve its output structure if you add LLM integrations.

Integrations & secrets
- Supabase: `SUPABASE_URL` and `SUPABASE_KEY` required for DB writes.
- Search agent: `SERPER_API_KEY` used by agents in `apps/agents` — tests should mock when absent.

Editing guidance (safe changes)
- Preserve Pydantic schemas or increment a version and update all consumers (worker, frontend).
- Update `sanitize_payload()` when engine outputs add non-JSON types (Polars, Decimal, numpy).
- When changing task payload shape, update `TaskDispatcher` and worker handlers in lockstep.

If you need more context
- Ask for missing env values (Supabase/SERPER) or permission to run the worker locally.
- I can open and annotate `apps/backend/src/services/task_queue.py` and the Supabase table schema with example payloads.

---
_Concise, focused, and actionable — tell me which sections you want expanded or examples added._
# Copilot / AI Agent Instructions for VERTIV v6.0

This file gives concise, actionable guidance so an AI coding agent can be immediately productive in this repository.

Overview
- Project style: a "Modular Monolith" — Next.js frontend, FastAPI backend, and Python worker (financial engine).
- Key runtimes: Python 3.10+ (backend/worker), Node 18+ (frontend).

Architecture (big-picture)
- Frontend: Next.js app in `apps/frontend` (Executive UI).
- Backend: FastAPI service in `apps/backend/src` — routers under `apps/backend/src/api/routes`, domain schemas in `apps/backend/src/domain/schemas.py`, persistence in `apps/backend/src/infrastructure`.
- Worker: long-running calculation/service in `apps/worker/core/main.py`. Worker imports backend modules at runtime and writes results to Supabase.
- Agents: small agent swarm in `apps/agents/src/` using `mcp` tools (web search, PDF/html scraping).
- Shared types/helpers: `packages/shared/src` (TypeScript shared package used by the frontend).

Important files to consult (examples)
- Backend API entry: [apps/backend/src/api/main.py](apps/backend/src/api/main.py)
- Worker entry: [apps/worker/core/main.py](apps/worker/core/main.py)
- LLM template service: [apps/backend/src/services/llm_service.py](apps/backend/src/services/llm_service.py)
- Supabase client: [apps/backend/src/infrastructure/database.py](apps/backend/src/infrastructure/database.py)
- Frontend package: [apps/frontend/package.json](apps/frontend/package.json)
- Root README (project intent): [README.md](README.md)

Dev workflows & commands
- Backend (local, development):

  PowerShell (Windows):
  ```powershell
  cd apps/backend
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  $env:SUPABASE_URL = "<your_url>"
  $env:SUPABASE_KEY = "<your_key>"
  # Run with PYTHONPATH pointing to the backend src root so imports like `src.*` work
  $env:PYTHONPATH = (Get-Location).Path
  uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
  ```

  Bash (Linux/macOS):
  ```bash
  cd apps/backend
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  export SUPABASE_URL="<your_url>"
  export SUPABASE_KEY="<your_key>"
  export PYTHONPATH=$(pwd)
  uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
  ```

- Worker (local): ensure the worker can import backend modules. Two options:
  - Run from repo root and set `PYTHONPATH=apps/backend` (Unix) or set `sys.path`/environment in Windows to include `apps/backend`.
  - In Docker/devcontainers the worker expects `/apps/backend` to be mounted.

  Example (Unix):
  ```bash
  export PYTHONPATH=$PWD/apps/backend
  cd apps/worker
  pip install -r requirements.txt
  uvicorn apps.worker.core.main:app --reload --port 8100
  ```

- Frontend: `cd apps/frontend && npm install && npm run dev` (Next.js dev server runs on default port).
- Docker/Cloud: the repo includes Dockerfiles and `scripts/orbit_deploy.sh` for cloud deployment — inspect `docker/` and `scripts/` before changing runtime assumptions.

Testing & linting
- Backend unit tests: `pytest` in `apps/backend/tests` (use the same Python environment as the backend). Tests import engine modules via `src.*` so `PYTHONPATH` or running from `apps/backend` with correct path matters.

Project-specific conventions & patterns
- Namespace style: backend packages are imported as `src.*` (not top-level package). Local dev must set `PYTHONPATH` or run from the package root so `src` is resolvable.
- Pydantic-first: domain schemas live in `apps/backend/src/domain/schemas.py` and are used for request/response models and worker serialization.
- Serialization guardrails: Worker sanitizes Polars/NumPy/Decimal types via `sanitize_payload()` in `apps/worker/core/main.py` — keep outputs JSON-serializable.
- LLM is stubbed: `LLMService.generate_investment_thesis()` provides a deterministic template (no external API). If adding an LLM integration, follow the existing template shape to preserve memo formatting.
- External keys: `SERPER_API_KEY` (agents), `SUPABASE_URL`, `SUPABASE_KEY` (backend/worker) are required for live integrations—use mock/fallback code paths when missing.

Integration & cross-component notes
- Persistence: Supabase used as the canonical `simulations` table. See [apps/backend/src/infrastructure/database.py](apps/backend/src/infrastructure/database.py).
- Task dispatch: API enqueues a simulation via `TaskDispatcher` (see `apps/backend/src/services/task_queue.py`) and the worker listens for `/tasks/process-simulation` target. When changing dispatch mechanism, update both sides.
- CORS: `apps/backend/src/api/main.py` currently allows origins `*` for dev; do not merge `*` into production without narrowing.

What to do when editing code
- Preserve Pydantic schemas — change schema versions incrementally and update consumer code in `worker` and `frontend`.
- When altering engine outputs, update `sanitize_payload()` and `P10FinancialOutput` usages to avoid serialization regressions.

Examples the agent can use directly
- To locate the API routes, open: [apps/backend/src/api/main.py](apps/backend/src/api/main.py)
- To see how worker sanitizes and writes results: [apps/worker/core/main.py](apps/worker/core/main.py)
- To modify the investment report template: [apps/backend/src/services/llm_service.py](apps/backend/src/services/llm_service.py)

If anything is missing
- Ask the reviewer for missing environment values (Supabase, SERPER key) or to point to any private infra docs. When unsure, prefer non-destructive changes and add tests.

Next step
- If you want, I can open `apps/backend/src/services/task_queue.py` and the Supabase table schema to add explicit examples of the dispatched payload and expected DB rows.

---
_Generated on behalf of a code review — request edits or ask me to expand any section._
