# VERTIV v6.0 - Estrutura do Projeto

**Gerado em:** 2025-12-24
**Metodo:** Filesystem MCP Exploration
**Status:** Production Ready

---

## Arquitetura ASCII

```
VERTIV_V6_GLOBAL/
|
+-- apps/                          # APLICACOES PRINCIPAIS
|   +-- backend/                   # API FastAPI (Python)
|   |   +-- src/
|   |   |   +-- api/               # Endpoints REST
|   |   |   |   +-- main.py        # Entry point FastAPI
|   |   |   |   +-- routes/        # Rotas por dominio
|   |   |   |       +-- analysis.py
|   |   |   |       +-- p1.py
|   |   |   |       +-- wizard.py
|   |   |   +-- domain/            # Schemas Pydantic
|   |   |   |   +-- schemas.py
|   |   |   +-- engine/            # CORE - Motor de Calculo TIV
|   |   |   |   +-- cashflow.py         # Fluxo de caixa
|   |   |   |   +-- p1_screener.py      # Garimpo de terrenos
|   |   |   |   +-- p2_economic.py      # Analise economica
|   |   |   |   +-- p4_vocation.py      # Vocacao urbana
|   |   |   |   +-- p5_legal.py         # Compliance legal
|   |   |   |   +-- p6_p9_market.py     # Estudo de mercado
|   |   |   |   +-- real_options.py     # Opcoes reais (MIT)
|   |   |   |   +-- real_options_binomial.py
|   |   |   |   +-- regulatory.py
|   |   |   +-- infrastructure/    # Camada de infra
|   |   |   |   +-- auth.py             # Autenticacao
|   |   |   |   +-- database.py         # Conexao DB
|   |   |   |   +-- rate_limiter.py     # Rate limiting
|   |   |   |   +-- repositories.py     # Repositorios
|   |   |   |   +-- tasks/              # Cloud Tasks
|   |   |   +-- services/          # Servicos externos
|   |   |       +-- llm_service.py      # Integracao LLM
|   |   |       +-- market_data.py      # Dados de mercado
|   |   |       +-- search_engine.py    # Serper API
|   |   |       +-- task_queue.py       # Fila de tarefas
|   |   +-- tests/
|   |   +-- Dockerfile
|   |   +-- requirements.txt
|   |
|   +-- frontend/                  # Next.js + React (TypeScript)
|   |   +-- src/
|   |   |   +-- app/               # App Router (Next.js 13+)
|   |   |   |   +-- auth/          # Paginas de autenticacao
|   |   |   |   +-- dashboard/     # Dashboard principal
|   |   |   |   +-- reports/       # Relatorios
|   |   |   |   +-- wizard/        # Wizard TIV
|   |   |   +-- components/        # Componentes React
|   |   |   |   +-- charts/        # Graficos (CashFlow, RealOptions)
|   |   |   |   +-- dashboard/     # Cards de insights
|   |   |   |   +-- map/           # GodViewMap (Mapbox)
|   |   |   |   +-- tribunal/      # Tribunal de Validacao
|   |   |   |   +-- ui/            # ShadCN UI components
|   |   |   |   +-- wizard/        # Steps do wizard
|   |   |   +-- contexts/          # React Context
|   |   |   +-- hooks/             # Custom hooks
|   |   |   +-- lib/               # Utilitarios
|   |   |   +-- store/             # Zustand store
|   |   +-- public/
|   |   +-- package.json
|   |   +-- tailwind.config.ts
|   |
|   +-- agents/                    # Agentes de Deep Research
|   |   +-- src/
|   |   |   +-- server.py          # FastMCP Server
|   |   +-- Dockerfile
|   |
|   +-- worker/                    # Worker de processamento
|       +-- core/
|       |   +-- main.py            # Cloud Tasks handler
|       +-- Dockerfile
|
+-- packages/                      # PACOTES COMPARTILHADOS
|   +-- shared/                    # Codigo compartilhado
|
+-- scripts/                       # SCRIPTS DE OPERACAO
|   +-- orbit_deploy.sh            # Deploy Cloud Run
|   +-- orbit_deploy.ps1           # Deploy (Windows)
|   +-- backup_database.py         # Backup Supabase
|   +-- load_test.py               # Testes de carga
|   +-- verify_*.py                # Scripts de verificacao
|   +-- spatial/                   # Processamento espacial
|
+-- docs/                          # DOCUMENTACAO
|   +-- API_CONTRACT.md            # Contrato de API
|   +-- ARCHITECTURE.md            # Arquitetura
|   +-- GUIA_USUARIO.md            # Manual do usuario
|   +-- MCP_SERVERS_DOCUMENTATION.md
|   +-- WHITE_PAPER.md
|
+-- docker/                        # Configuracoes Docker
+-- tests/                         # Testes E2E
|   +-- load/
|       +-- locustfile.py          # Testes Locust
|
+-- .agent/                        # CONHECIMENTO DO AGENTE
|   +-- KB_CORE v6.0               # Knowledge Base (112k tokens)
|   +-- rules/                     # Regras de conduta
|   +-- workflows/                 # Fluxos de trabalho
|
+-- .github/                       # GitHub configs
|   +-- copilot-instructions.md
|
+-- docker-compose.yml             # Orquestracao local
+-- orbital.config.js              # Config Orbital
+-- README.md
```

---

## Contagem de Arquivos por Tipo

| Tipo | Extensao | Quantidade |
|------|----------|------------|
| Python | .py | 50 |
| TypeScript/TSX | .ts/.tsx | 41 |
| JavaScript | .js | 6 |
| JSON | .json | 609 |
| Markdown | .md | 27 |
| YAML | .yml/.yaml | 5 |
| Dockerfile | Dockerfile* | 8 |

**Total de arquivos de codigo:** ~97 arquivos (excluindo configs)

---

## Arquivos Criticos

### Backend (Python)
| Arquivo | Funcao | Criticidade |
|---------|--------|-------------|
| `apps/backend/src/api/main.py` | Entry point FastAPI | ALTA |
| `apps/backend/src/engine/cashflow.py` | Motor de fluxo de caixa | CRITICA |
| `apps/backend/src/engine/real_options.py` | Opcoes reais MIT/Geltner | CRITICA |
| `apps/backend/src/engine/p1_screener.py` | Garimpo de terrenos | ALTA |
| `apps/backend/src/services/market_data.py` | Dados de mercado live | ALTA |
| `apps/backend/src/services/llm_service.py` | Integracao com LLM | MEDIA |
| `apps/backend/src/infrastructure/auth.py` | Autenticacao Supabase | ALTA |

### Frontend (TypeScript)
| Arquivo | Funcao | Criticidade |
|---------|--------|-------------|
| `apps/frontend/src/app/wizard/page.tsx` | Wizard principal TIV | CRITICA |
| `apps/frontend/src/components/charts/CashFlowChart.tsx` | Visualizacao DCF | ALTA |
| `apps/frontend/src/components/charts/RealOptionsCone.tsx` | Cone de opcoes reais | ALTA |
| `apps/frontend/src/components/map/GodViewMap.tsx` | Mapa interativo | ALTA |
| `apps/frontend/src/store/wizard-store.ts` | Estado do wizard | ALTA |
| `apps/frontend/src/contexts/AuthContext.tsx` | Contexto de auth | ALTA |

### Configuracao
| Arquivo | Funcao | Criticidade |
|---------|--------|-------------|
| `docker-compose.yml` | Orquestracao local | ALTA |
| `.env.production.example` | Template de producao | ALTA |
| `apps/backend/requirements.txt` | Deps Python | ALTA |
| `apps/frontend/package.json` | Deps Node | ALTA |

---

## Arquitetura de Microservicos

```
                    +------------------+
                    |   CLOUDFLARE     |
                    |   (CDN + WAF)    |
                    +--------+---------+
                             |
              +--------------+--------------+
              |                             |
    +---------v---------+         +---------v---------+
    |    FRONTEND       |         |     BACKEND       |
    |    (Next.js)      |         |    (FastAPI)      |
    |   Cloud Run       |         |   Cloud Run       |
    +--------+----------+         +---------+---------+
             |                              |
             |         +--------------------+
             |         |                    |
             |    +----v----+         +-----v-----+
             |    | SUPABASE|         |  WORKER   |
             +--->|   DB    |         | Cloud Run |
                  +---------+         +-----------+
                                            |
                                      +-----v-----+
                                      |  SERPER   |
                                      | Live Data |
                                      +-----------+
```

---

## Stack Tecnologico

### Backend
- **Framework:** FastAPI 0.115+
- **Linguagem:** Python 3.11+
- **ORM:** Supabase Client
- **Auth:** Supabase Auth + JWT
- **Queue:** Google Cloud Tasks

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Linguagem:** TypeScript 5+
- **UI:** Tailwind CSS + ShadCN
- **State:** Zustand
- **Charts:** Recharts
- **Maps:** Mapbox GL

### Infraestrutura
- **Cloud:** Google Cloud Platform
- **Runtime:** Cloud Run
- **Database:** Supabase (PostgreSQL)
- **CDN:** Cloudflare
- **CI/CD:** GitHub Actions

---

## Metodologia TIV - 10 Passos

```
P1  Garimpo          -> Screener de terrenos
P2  Economico        -> Analise macroeconomica
P3  Projecao         -> Projecao de vendas
P4  Vocacao          -> Vocacao urbana
P5  Legal            -> Compliance regulatorio
P6  Mercado          -> Estudo de mercado
P7  Competidores     -> Analise competitiva
P8  Precificacao     -> Pricing strategy
P9  Demanda          -> Validacao de demanda
P10 Financeiro       -> DCF + Opcoes Reais
```

---

## Proximos Passos

1. [ ] Integrar Deep Research Agents com FastMCP
2. [ ] Implementar GodViewMap com dados reais
3. [ ] Adicionar testes E2E com Playwright
4. [ ] Deploy producao com dominio vertiv.tech

---

**Gerado por:** Filesystem MCP + Claude Code
**Projeto:** VERTIV v6.0 - GLOBAL EDITION
