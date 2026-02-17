# VERTIV v6.0 — Mapa do Sistema (1 Tela)

## Fluxo de Dados: Entrada → Processamento → Saída

```mermaid
graph TD
    User((Usuário / Browser)) -->|HTTPS / Next.js| Frontend[Frontend: Next.js 13+]
    Frontend -->|REST API (JSON)| Backend[Backend: Python FastAPI]
    
    subgraph "Nuvem & Infra (Google Cloud Run)"
        Frontend
        Backend
        Worker[Worker Service: Python]
    end

    subgraph "Camada de Dados (Supabase)"
        Auth[Auth: Supabase Auth]
        DB[(PostgreSQL: Dados Persistentes)]
        Storage[Storage: Buckets]
    end

    subgraph "Motores de Inteligência (The Diamond Core)"
        Backend -->|Dados Brutos| Polars[Engine: Polars DataFrame]
        Polars -->|Cálculo Vetorial| Financials[Módulos: CashFlow, RealOptions, ESG]
        Financials -->|Resultados Otimizados| Backend
    end

    subgraph "Inteligência Externa (ScoutAgent)"
        Backend -.->|Task Queue (Redis)| Worker
        Worker -->|Busca ao Vivo| Serper[API: Serper.dev / Google]
        Serper -->|Dados de Mercado| Worker
        Worker -.->|Atualização de Status| DB
    end

    Backend -->|Leitura/Escrita| DB
    Backend -->|Validação de Token| Auth
```

## Descrição dos Componentes

### 1. Entrada (Frontend)
-   **Tecnologia:** Next.js (React), Tailwind CSS.
-   **Função:** Interface "Stoic Premium", captura inputs do usuário (Terreno, Premissas) e exibe dashboards.
-   **Hospedagem:** Container Docker no Google Cloud Run.

### 2. Processamento (Backend & Worker)
-   **Tecnologia:** Python 3.11, FastAPI.
-   **O "Diamond Core":** Biblioteca **Polars** substitui loops Python e Pandas para cálculos financeiros massivos e instantâneos.
-   **Worker Assíncrono:** Separa tarefas pesadas (buscas na web, simulações Monte Carlo longas) da API principal para evitar bloqueios.
-   **ScoutAgent:** Módulo autônomo que varre a web em busca de preços concorrentes para alimentar o modelo.

### 3. Dados (Persistência)
-   **Tecnologia:** Supabase (PostgreSQL).
-   **Função:** Armazena usuários, projetos, premissas salvas e logs de auditoria.
-   **Integração:** Backend usa SQLAlchemy/Pydantic para garantir integridade dos dados antes de salvar.

### 4. Saída (Resultados)
-   **Formato:** JSON estrito validado por Pydantic.
-   **Consumo:** O Frontend recebe os dados processados e renderiza gráficos (Recharts) e tabelas dinâmicas sem lógica de negócio pesada no cliente.
