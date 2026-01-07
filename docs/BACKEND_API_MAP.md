# Backend API Endpoints Map

**VERTIV v6.1.0-SINGULARITY**
**Gerado em:** 2025-12-24
**Base URL:** `/api` (via proxy) ou diretamente na porta 8000

---

## Resumo

| Modulo | Endpoints | Autenticacao |
|--------|-----------|--------------|
| Core | 6 | Misto |
| P1 Garimpo | 1 | Nao |
| TIV Wizard (P2-P9) | 8 | Nao |
| Wizard Session | 3 | Nao |
| Analysis | 1 | Nao |
| **TOTAL** | **19** | - |

---

## Core API

**Arquivo:** `apps/backend/src/api/main.py`

### Health Check (Publico)

| Metodo | Rota | Funcao | Descricao |
|--------|------|--------|-----------|
| `GET` | `/health` | `health_check()` | Health check para load balancers e monitoramento |

**Response:**
```json
{
  "status": "ok",
  "version": "6.1.0-SINGULARITY",
  "mode": "GLOBAL_EDITION",
  "security": "enabled"
}
```

---

### Simulations (Autenticado)

| Metodo | Rota | Funcao | Auth | Rate Limit |
|--------|------|--------|------|------------|
| `GET` | `/simulations` | `list_simulations()` | JWT | 60/min |
| `GET` | `/simulations/recent` | `get_recent_simulations()` | JWT | 60/min |
| `GET` | `/simulation/{simulation_id}` | `get_simulation()` | JWT | 60/min |
| `POST` | `/calculate/quick` | `calculate_quick()` | JWT | 30/min |

#### GET /simulations
Lista simulacoes do portfolio do usuario autenticado.

**Query Params:**
- `limit` (int, default=10): Numero maximo de resultados
- `offset` (int, default=0): Paginacao

---

#### GET /simulations/recent
Retorna simulacoes recentes do usuario.

**Query Params:**
- `limit` (int, default=1): Numero de resultados

---

#### GET /simulation/{simulation_id}
Recupera status e resultado de uma simulacao especifica.

**Path Params:**
- `simulation_id` (string): UUID da simulacao

**Response Model:** `SimulationResponse`

---

#### POST /calculate/quick
Dispara simulacao assincrona via Cloud Tasks.

**Request Body:** `ProjectTIV`
```json
{
  "land_price": 1500000,
  "land_area_sqm": 5000,
  "sellable_area_sqm": 3000,
  "unit_price_avg": 180000,
  "total_units": 30,
  "construction_cost_per_sqm": 1200,
  "sales_months": 24,
  "construction_months": 18
}
```

**Response:** `SimulationResponse` com status PENDING

---

### User Info (Autenticado)

| Metodo | Rota | Funcao | Auth |
|--------|------|--------|------|
| `GET` | `/me` | `get_current_user_info()` | JWT |

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "role": "user",
  "authenticated": true
}
```

---

## P1: Garimpo (Screener)

**Arquivo:** `apps/backend/src/api/routes/p1.py`
**Prefix:** `/p1`
**Tags:** `P1: Garimpo`

| Metodo | Rota | Funcao | Descricao |
|--------|------|--------|-----------|
| `POST` | `/p1/analyze` | `analyze_opportunity()` | Analisa oportunidade de terreno (Go/No-Go) |

**Request Body:** `P1GarimpoInput`
```json
{
  "municipality": "Leopoldina",
  "neighborhood": "Centro",
  "land_area_sqm": 5000,
  "land_price_per_sqm": 150,
  "market_phase": "EXPANSION"
}
```

**Response:** `P1GarimpoOutput`

---

## TIV Wizard (P2-P9)

**Arquivo:** `apps/backend/src/api/routes/wizard.py`
**Prefix:** `/wizard`
**Tags:** `TIV Wizard`

### P2: Dinamica Economica

| Metodo | Rota | Funcao | Descricao |
|--------|------|--------|-----------|
| `POST` | `/wizard/p2/analyze` | `analyze_p2_economic()` | Analise P2i-Lead (0-50 pontos) |

**Request:**
```json
{
  "municipality": "Leopoldina",
  "municipality_population": 50000,
  "is_metropolitan": false
}
```

**Gate:** P2i-Lead >= 28 para GO

---

### P4: Vocacao Imobiliaria

| Metodo | Rota | Funcao | Descricao |
|--------|------|--------|-----------|
| `POST` | `/wizard/p4/analyze` | `analyze_p4_vocation()` | Matriz de Atratividade 3 Pilares |

**Request:**
```json
{
  "municipality": "Leopoldina",
  "neighborhood": "Centro",
  "zoning_type": "ZR2",
  "max_height_floors": 4,
  "max_coverage_ratio": 0.6,
  "max_floor_area_ratio": 2.0,
  "distance_city_center_km": 2.0,
  "infrastructure_level": "COMPLETE",
  "land_area_sqm": 5000,
  "land_price_per_sqm": 150.0,
  "target_segment": "MEDIO"
}
```

**Pilares:**
- Pilar 1: Zoning & Potencial (30%)
- Pilar 2: Centralidade & Acessibilidade (40%)
- Pilar 3: Infraestrutura (30%)

---

### P5: Due Diligence Legal

| Metodo | Rota | Funcao | Descricao |
|--------|------|--------|-----------|
| `POST` | `/wizard/p5/analyze` | `analyze_p5_legal()` | Verificacao PASS/FAIL legal |

**Request:**
```json
{
  "land_registration_number": "12345",
  "municipality": "Leopoldina",
  "has_clear_title": true,
  "is_registered": true,
  "has_pending_lawsuits": false,
  "is_in_app": false,
  "complies_with_zoning": true
}
```

**Gate:** Binario PASS/FAIL

---

### P6: Demanda Qualificada

| Metodo | Rota | Funcao | Descricao |
|--------|------|--------|-----------|
| `POST` | `/wizard/p6/analyze` | `analyze_p6_demand()` | Funil de 5 estagios de demanda |

**Request:**
```json
{
  "municipality": "Leopoldina",
  "influence_area_population": 50000,
  "average_household_income": 5000.0,
  "target_segment": "MEDIO",
  "unit_price_min": 150000.0,
  "unit_price_max": 250000.0,
  "unit_type": "LOTE"
}
```

**Funil:**
1. Familias Totais
2. Qualificadas por Renda
3. Fit de Produto
4. Intencao de Compra
5. Demanda Efetiva

---

### P7: Oferta & Concorrencia

| Metodo | Rota | Funcao | Descricao |
|--------|------|--------|-----------|
| `POST` | `/wizard/p7/analyze` | `analyze_p7_supply()` | Analise de inventario e pricing |

**Request:**
```json
{
  "municipality": "Leopoldina",
  "influence_area_km": 5.0,
  "competitors": [
    {
      "name": "Projeto A",
      "developer": "Construtora X",
      "total_units": 100,
      "units_sold": 60,
      "units_available": 40,
      "price_per_sqm": 280.0
    }
  ]
}
```

---

### P8: Absorcao (VSO)

| Metodo | Rota | Funcao | Descricao |
|--------|------|--------|-----------|
| `POST` | `/wizard/p8/analyze` | `analyze_p8_absorption()` | Velocidade de vendas e timeline |

**Request:**
```json
{
  "municipality": "Leopoldina",
  "project_units": 30,
  "project_price_avg": 180000.0,
  "qualified_demand": 200,
  "active_inventory": 50,
  "market_vso_monthly": 0.08
}
```

---

### P9: Validacao Estrategica

| Metodo | Rota | Funcao | Descricao |
|--------|------|--------|-----------|
| `POST` | `/wizard/p9/analyze` | `analyze_p9_validation()` | Gate 4:1 final antes do P10 |

**Request:**
```json
{
  "municipality": "Leopoldina",
  "qualified_demand": 200,
  "active_inventory": 50,
  "competitors_count": 3,
  "projected_absorption_months": 24,
  "project_units": 30,
  "project_price_sqm": 300.0,
  "market_price_sqm": 280.0
}
```

**Gate:** Ratio Demanda:Oferta >= 4:1

---

## Wizard Session Management

| Metodo | Rota | Funcao | Descricao |
|--------|------|--------|-----------|
| `POST` | `/wizard/session/create` | `create_wizard_session()` | Cria nova sessao do wizard |
| `POST` | `/wizard/session/save-step` | `save_wizard_step()` | Salva dados de um step |
| `GET` | `/wizard/session/{session_id}` | `get_wizard_session()` | Recupera dados da sessao |

### POST /wizard/session/create
```json
{
  "project_name": "Residencial Aurora",
  "municipality": "Leopoldina"
}
```

**Response:**
```json
{
  "session_id": "A1B2C3D4",
  "status": "created"
}
```

### POST /wizard/session/save-step
```json
{
  "session_id": "A1B2C3D4",
  "step": "p2",
  "data": { ... }
}
```

---

## Analysis (LLM)

**Arquivo:** `apps/backend/src/api/routes/analysis.py`

| Metodo | Rota | Funcao | Descricao |
|--------|------|--------|-----------|
| `POST` | `/analyze/thesis` | `generate_thesis()` | Gera tese de investimento via LLM |

**Request:**
```json
{
  "financial_data": {
    "roi": 0.25,
    "payback_months": 36,
    "npv": 1500000,
    "irr": 0.18
  }
}
```

**Response:**
```json
{
  "thesis": "Analise de investimento gerada pelo LLM..."
}
```

---

## Seguranca

### Autenticacao JWT
- Header: `Authorization: Bearer <token>`
- Provider: Supabase Auth
- Validacao: RSA256 com JWKS

### Rate Limiting
| Tier | Limite | Endpoints |
|------|--------|-----------|
| Global | 60 req/min, 10 req/sec | Todos |
| Simulations | 30 req/min | `/calculate/quick` |

### CORS
- **Producao:** `https://vertiv.tech`
- **Desenvolvimento:** `*`

---

## Arquitetura de Rotas

```
main.py (FastAPI App)
|
+-- /health                    [PUBLIC]
+-- /me                        [AUTH]
+-- /simulations               [AUTH]
+-- /simulations/recent        [AUTH]
+-- /simulation/{id}           [AUTH]
+-- /calculate/quick           [AUTH + RATE_LIMIT]
|
+-- routes/p1.py
|   +-- /p1/analyze
|
+-- routes/wizard.py
|   +-- /wizard/p2/analyze
|   +-- /wizard/p4/analyze
|   +-- /wizard/p5/analyze
|   +-- /wizard/p6/analyze
|   +-- /wizard/p7/analyze
|   +-- /wizard/p8/analyze
|   +-- /wizard/p9/analyze
|   +-- /wizard/session/create
|   +-- /wizard/session/save-step
|   +-- /wizard/session/{id}
|
+-- routes/analysis.py
    +-- /analyze/thesis
```

---

## Swagger UI

Disponivel em:
- **Local:** http://localhost:8000/docs
- **Producao:** https://api.vertiv.tech/docs

---

**Gerado por:** Filesystem MCP + Claude Code
**Projeto:** VERTIV v6.0 - GLOBAL EDITION
