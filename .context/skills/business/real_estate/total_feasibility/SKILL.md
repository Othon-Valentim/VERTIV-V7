---
name: total_feasibility_matrix
description: Implementa a Matriz de Viabilidade Total (MVT) para Land Banking e Valuation.
---

# Matriz de Viabilidade Total (MVT)

Esta skill orquestra a avaliação multidimensional de projetos imobiliários, integrando as doutrinas Vertiv.

## Trigger
"viabilidade", "land banking", "estudo de massa", "valuation"

## A Fórmula Mestre
`VT = f(L, P, M, F, I, E, T)`

Onde:
- **L:** Legal (Hard)
- **P:** Physical (Hard)
- **M:** Market (Hard)
- **E:** Ethical (Hard)
- **F:** Financial (Soft)
- **I:** Institutional (Soft)
- **T:** Time (Soft)

## Lógica de Execução (The Engine)

### 1. Identificação de Hard Constraints
Avalie as dimensões Críticas (L, P, M, E) usando os Gatekeepers correspondentes:
- **Legal & Ethical:** Consultar `@AUDITOR`.
- **Physical:** Consultar `@LUCAS`.
- **Market:** Consultar `@OTHON`.

### Model Override (Thinking Model)
- **Model:** `gemini-2.0-flash-thinking` (ou o modelo Thinking mais atual disponível).
- **Scope:** Específico para a etapa de **Hard Constraints**.
- **Justificativa:** "Cadeia de Pensamento" necessária para julgar se o terreno de 220k m² pode realmente ser desmembrado segundo o Plano Diretor em cache.

### 2. O Kill-Switch (O Veto Supremo)
- Calcule `MIN(L, P, M, E)`.
- Se `MIN(Hard) < 0.65`:
    - **Ação:** Retornar **NO-GO IMEDIATO**.
    - **Justificativa:** "Dinheiro não compensa risco estrutural."

### 3. Cálculo do IVT (Índice de Viabilidade Total)
Se passed Hard Constraints, calcule o IVT integrando as Soft Constraints (F, I, T).
O lucro é condição de existência, mas a solvência do caixa precede a maximização da TIR.

### 4. Relatório "Decisão de Comitê"
Gere um output estruturado com:
- Status dos Gatekeepers.
- Ponto de falha (se houver).
- Recomendação estratégica baseada na Doutrina de Solvência.
