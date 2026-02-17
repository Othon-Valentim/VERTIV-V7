# TF-MVT SYSTEM REQUIREMENTS (SPEC SHEET)

**Version:** 1.0.0  
**Authority:** Arquiteto Valentim Hou  
**Status:** MANDATORY

## 1. Core Principles
- **Hard-Kill Protocol:** Se uma Hard Constraint (Legal, Física, Ética) falhar (Score < 0.65), o sistema deve interromper a análise financeira imediatamente.
- **Audit Traceability:** Todo cálculo de score deve gerar um log em `audit_results.txt` com timestamp, entrada (input) e justificativa.

## 2. Technical Stack (Non-Negotiable)
- **Frontend:** Next.js 14+ (App Router), Tailwind CSS.
- **Backend:** Python 3.11+, Polars (Calculations), Pydantic (Schemas).
- **Communication:** Supabase for persistence, standard REST/FastAPI.

## 3. Security Constraints
- **Zero Exfiltration:** Credenciais e tokens (Airtable, Supabase, OpenAI) devem ser lidos apenas via `.env`. Nunca hardcoded.
- **Sandbox Execution:** O Browser Subagent só pode acessar URLs em conformidade com a Allowlist institucional.

## 4. Maintenance & Resiliency
- **Three Strike Protocol:** Em caso de erro em automações (ex: Airtable), o agente deve diagnosticar a raíz do problema via logs antes de tentar a correção.
- **Planning First:** Nenhuma modificação em motores de cálculo (`CashFlowEngine`, `MVT`) sem antes validar o `task_plan.md`.
