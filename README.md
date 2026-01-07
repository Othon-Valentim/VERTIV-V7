# VERTIV™ v6.1.0-SINGULARITY: Protocol Achieved 🌍🏛️

> *"The first Real Estate Investment Engine that thinks like a Wall Street Quant and executes like a Global CEO."*

![Version](https://img.shields.io/badge/Version-6.1.0--SINGULARITY-gold?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-GLOBAL_LEADER-000000?style=for-the-badge)
![Stack](https://img.shields.io/badge/Core-MODULAR_MONOLITH-blue?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-BANK_GRADE-green?style=for-the-badge)

**Live:** [https://vertiv.tech](https://vertiv.tech) | **API:** [https://api.vertiv.tech](https://api.vertiv.tech)

---

## 📜 The Manifesto

Real Estate development is broken. Traditional spreadsheets (DCF) are **deterministic**—they assume the world is static. But the market is chaotic.

**VERTIV v6.1.0-SINGULARITY** is not a "calculator". It is a **Stochastic Intelligence Platform**.
It uses the **T.I.V. (Tese de Investimento Vertical)** methodology to price **Uncertainty** as an **Asset**.

### What's New in SINGULARITY?

| Feature | Description |
|---------|-------------|
| **Bank-Grade Security** | JWT Authentication + Rate Limiting (60 req/min) |
| **Dynamic Metrics** | ROE, Payback, Max Exposure calculated in real-time |
| **Live Web Intelligence** | AI Agents with real-time Serper web search |
| **IT-11 Compliance** | Fire safety penalty engine for mixed-use buildings |

---

## 🏗️ Architecture: The Modular Monolith

We rejected Microservices. We embraced **Unity**.

*   **Frontend**: Next.js 14 (The Executive View)
*   **Backend**: FastAPI (The Orchestrator)
*   **Worker**: Python Financial Engine (The Quant)
*   **Agents**: MCP-based AI Intelligence Swarm
*   **Persistence**: Supabase + RLS (The Vault)

> *See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full blueprint.*

---

## 🚀 Quick Start

### Prerequisites
*   Docker & Orbit (Google Cloud Run)
*   Supabase Credentials
*   Serper API Key (for live search)

### Launch Sequence
```bash
# 1. Clone the Protocol
git clone https://github.com/vertiv-capital/v6-global.git

# 2. Configure Environment
cp .env.production.example .env
# Edit .env with your credentials

# 3. Ignite the Engines
./scripts/orbit_deploy.sh
```

---

## 🔮 The Singularity Features

| Feature | Description | Status |
| :--- | :--- | :--- |
| **P1 Garimpo** | Rapid land screening algorithm | ✅ Live |
| **Real Options** | Black-Scholes-Merton for Land Banking | ✅ Live |
| **AI Thesis** | Automated Investment Committee Memos | ✅ Live |
| **Portfolio** | Multi-asset governance grid | ✅ Live |
| **JWT Auth** | Bank-grade API security | ✅ v6.1.0 |
| **Rate Limiting** | DDoS protection (60/min, 10/sec) | ✅ v6.1.0 |
| **Dynamic ROE** | Real-time equity calculations | ✅ v6.1.0 |
| **Live Search** | Serper-powered web intelligence | ✅ v6.1.0 |

---

## 📚 Documentation Suite

*   **[API CONTRACT](docs/API_CONTRACT.md)**: Complete API specification
*   **[WHITE PAPER](docs/WHITE_PAPER.md)**: The mathematical philosophy behind TIV
*   **[USER MANUAL](docs/USER_MANUAL.md)**: Operator's guide for the C-Suite
*   **[ARCHITECTURE](docs/ARCHITECTURE.md)**: Technical specifications

---

## 🔐 Security

VERTIV v6.1.0 implements enterprise-grade security:

- **Authentication**: Supabase JWT with role-based access
- **Rate Limiting**: 60 requests/minute global, 30/minute for simulations
- **CORS**: Locked to production domains
- **Input Validation**: Pydantic schema enforcement

---

## 📊 Load Testing

```bash
# Run load tests
locust -f tests/load/locustfile.py --headless -u 100 -r 10 --run-time 1m

# Cleanup test data
psql -f scripts/cleanup_load_test.sql
```

---

*"We do not predict the future. We structure the present to profit from the future's volatility."*

**© 2025 VERTIV CAPITAL. All Rights Reserved.**
