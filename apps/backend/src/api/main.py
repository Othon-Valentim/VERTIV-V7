"""
VERTIV v6.0 API - Global Edition
Real Estate Viability Analysis Platform

Security Features:
- JWT Authentication via Supabase
- Rate Limiting (60 req/min, 10 req/sec)
- CORS Configuration
"""

# Carregar variáveis de ambiente do .env
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from src.infrastructure.repositories import SimulationRepository
from fastapi.middleware.cors import CORSMiddleware
from decimal import Decimal
from typing import Optional, AsyncGenerator
import os
import asyncio
import json

from src.domain.schemas import (
    ProjectTIV,
    P10FinancialOutput,
    SimulationRequest,
    SimulationStatus,
    SimulationResponse,
)
from src.engine.cashflow import CashFlowEngine
from src.engine.real_options import RealOptionsEngine
from src.api.routes import p1, analysis, ingest
from src.services.task_queue import TaskDispatcher
from src.services.search_engine import SearchEngine

# Security imports
from src.infrastructure.auth import (
    get_current_user,
    get_optional_user,
    get_user_from_token_param,
    CurrentUser,
)
from src.infrastructure.rate_limiter import (
    RateLimitMiddleware,
    default_limiter,
    check_simulation_rate_limit,
)

import uuid
import traceback

# Environment
ENV = os.getenv("ENV", "development")
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS", "https://vertiv.tech,http://localhost:3000"
).split(",")

app = FastAPI(
    title="VERTIV v6.0 API",
    version="7.0.0-SINGULARITY",
    description="Global Edition - Real Estate Viability Analysis Platform with Bank-Grade Security",
)

# CORS - Locked down for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ENV == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)

# Rate Limiting Middleware
app.add_middleware(
    RateLimitMiddleware,
    limiter=default_limiter,
    exclude_paths=["/health", "/docs", "/openapi.json", "/redoc"],
)

# Include routers
app.include_router(p1.router)
app.include_router(analysis.router)
app.include_router(ingest.router, prefix="/api/v7", tags=["V7 Ingestion"])
# V7: Wizard removed — Data Room ingestion replaces manual entry


# ============================================================================
# PUBLIC ENDPOINTS (No Auth Required)
# ============================================================================


@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {
        "status": "ok",
        "version": "6.1.0-SINGULARITY",
        "mode": "GLOBAL_EDITION",
        "security": "enabled",
    }


@app.get("/metrics/cache")
async def get_cache_metrics(user: CurrentUser = Depends(get_current_user)):
    """
    Retorna estatísticas do cache do SearchEngine (Serper).

    Métricas:
    - hits: Quantas vezes o cache foi utilizado
    - misses: Quantas vezes precisou chamar a API
    - hit_rate: Percentual de eficiência do cache
    - api_calls_saved: Chamadas de API economizadas ($$)
    """
    search_engine = SearchEngine()
    return {
        "cache": "serper_search",
        "stats": search_engine.get_cache_stats(),
        "ttl_days": 7,
    }


# ============================================================================
# PROTECTED ENDPOINTS (Auth Required)
# ============================================================================


@app.get("/simulations", response_model=list[dict])
async def list_simulations(
    limit: int = 10, offset: int = 0, user: CurrentUser = Depends(get_current_user)
):
    """
    List simulations for the authenticated user's portfolio view.
    Requires JWT authentication.
    """
    repo = SimulationRepository()
    return repo.get_latest(user.id, limit)


@app.get("/simulations/recent", response_model=list[dict])
async def get_recent_simulations(
    limit: int = 1, user: CurrentUser = Depends(get_current_user)
):
    """Get recent simulations for the authenticated user."""
    repo = SimulationRepository()
    return repo.get_latest(user.id, limit)


@app.get("/simulation/{simulation_id}", response_model=SimulationResponse)
async def get_simulation(
    simulation_id: str, user: CurrentUser = Depends(get_current_user)
):
    """
    Retrieves the status and result of a simulation.
    Requires JWT authentication.
    """
    repo = SimulationRepository()
    data = repo.get(simulation_id, user.id)

    if not data:
        raise HTTPException(status_code=404, detail="Simulation not found")

    return SimulationResponse(
        simulation_id=data["id"],
        status=data["status"],
        result=data.get("result"),
        error=data.get("result", {}).get("error") if data.get("result") else None,
    )


# ============================================================================
# SSE ENDPOINT - Real-time Updates (substitui polling)
# ============================================================================


async def simulation_status_stream(
    simulation_id: str,
    repo: SimulationRepository,
    user_id: str,
    timeout_seconds: int = 300,  # 5 minutos max
) -> AsyncGenerator[str, None]:
    """
    Generator que emite eventos SSE com status da simulação.

    Formato SSE:
    - event: status
    - data: JSON com {status, result?, error?}

    Encerra quando:
    - Status = COMPLETED ou FAILED
    - Timeout atingido
    """
    start_time = asyncio.get_event_loop().time()
    check_interval = (
        1.0  # Verifica a cada 1 segundo (muito mais eficiente que polling do cliente)
    )

    while True:
        # Verificar timeout
        elapsed = asyncio.get_event_loop().time() - start_time
        if elapsed > timeout_seconds:
            yield f"event: timeout\ndata: {json.dumps({'error': 'Stream timeout after 5 minutes'})}\n\n"
            break

        # Buscar status atual
        data = repo.get(simulation_id, user_id)

        if not data:
            yield f"event: error\ndata: {json.dumps({'error': 'Simulation not found'})}\n\n"
            break

        status = data.get("status", "PENDING")
        result = data.get("result")

        # Emitir evento SSE
        payload = {
            "simulation_id": simulation_id,
            "status": status,
            "elapsed_seconds": round(elapsed, 1),
        }

        if status == "COMPLETED":
            payload["result"] = result
            yield f"event: completed\ndata: {json.dumps(payload)}\n\n"
            break
        elif status == "FAILED":
            payload["error"] = result.get("error") if result else "Unknown error"
            yield f"event: failed\ndata: {json.dumps(payload)}\n\n"
            break
        else:
            # PENDING ou PROCESSING - continuar streaming
            yield f"event: status\ndata: {json.dumps(payload)}\n\n"

        # Aguardar antes da próxima verificação
        await asyncio.sleep(check_interval)


@app.get("/simulation/{simulation_id}/stream")
async def stream_simulation_status(
    simulation_id: str,
    request: Request,
    token: Optional[str] = None,
    user: CurrentUser = Depends(get_user_from_token_param),
):
    """
    SSE Endpoint para streaming de status de simulação.

    Substitui o polling do frontend por Server-Sent Events.
    O cliente recebe atualizações em tempo real sem fazer requisições repetidas.

    Autenticação via query param (SSE não suporta headers customizados):
    ```
    GET /simulation/{id}/stream?token=JWT_TOKEN
    ```

    Uso no frontend:
    ```javascript
    const token = localStorage.getItem('access_token');
    const eventSource = new EventSource(`/simulation/{id}/stream?token=${token}`);
    eventSource.addEventListener('completed', (e) => {
        const data = JSON.parse(e.data);
        console.log('Resultado:', data.result);
        eventSource.close();
    });
    ```

    Eventos emitidos:
    - status: Atualização periódica (PENDING/PROCESSING)
    - completed: Simulação finalizada com sucesso
    - failed: Simulação falhou
    - timeout: Stream encerrado por timeout (5 min)
    - error: Erro ao buscar simulação
    """
    repo = SimulationRepository()

    # Verificar se simulação existe
    data = repo.get(simulation_id, user.id)
    if not data:
        raise HTTPException(status_code=404, detail="Simulation not found")

    print(f"[SSE] User {user.email} connected to stream for simulation {simulation_id}")

    return StreamingResponse(
        simulation_status_stream(simulation_id, repo, user.id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Desabilita buffering no nginx
        },
    )


@app.post("/calculate/quick", response_model=SimulationResponse)
async def calculate_quick(
    project: ProjectTIV,
    request: Request,
    user: CurrentUser = Depends(get_current_user),
    _rate_limit: None = Depends(check_simulation_rate_limit),
):
    """
    Async Simulation Endpoint.

    Security:
    - Requires JWT authentication
    - Rate limited (30 req/min for simulations)

    Dispatches job to Worker via Cloud Tasks (or local stub).
    Returns 202-like response with SimulationID.
    """
    # Generate Simulation ID
    sim_id = str(uuid.uuid4())

    # Log authenticated request
    print(f"[AUTH] Simulation {sim_id} requested by user {user.id} ({user.email})")

    # Create Payload with user context
    request_payload = SimulationRequest(simulation_id=sim_id, project=project)

    # Save to DB (PENDING) - Include user_id for RLS
    repo = SimulationRepository()
    try:
        project_data = project.model_dump(mode="json")
        repo.create(sim_id, project_data, user.id)
    except Exception as e:
        print(f"Database Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Database Persistence Failed: {str(e)}"
        )

    # Dispatch Request
    try:
        task_name = await TaskDispatcher.dispatch_simulation(request_payload)
        print(f"[DISPATCH] Simulation {sim_id}: Task {task_name}")

        return SimulationResponse(
            simulation_id=sim_id, status=SimulationStatus.PENDING, result=None
        )
    except Exception as e:
        traceback.print_exc()
        return SimulationResponse(
            simulation_id=sim_id, status=SimulationStatus.FAILED, error=str(e)
        )


# ============================================================================
# USER INFO ENDPOINT
# ============================================================================


@app.get("/me")
async def get_current_user_info(user: CurrentUser = Depends(get_current_user)):
    """
    Returns information about the currently authenticated user.
    Useful for frontend to verify authentication status.
    """
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "authenticated": True,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
