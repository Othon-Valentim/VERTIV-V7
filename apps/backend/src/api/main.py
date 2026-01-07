"""
VERTIV v6.0 API - Global Edition
Real Estate Viability Analysis Platform

Security Features:
- JWT Authentication via Supabase
- Rate Limiting (60 req/min, 10 req/sec)
- CORS Configuration
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from src.infrastructure.repositories import SimulationRepository
from fastapi.middleware.cors import CORSMiddleware
from decimal import Decimal
from typing import Optional
import os

from src.domain.schemas import (
    ProjectTIV,
    P10FinancialOutput,
    SimulationRequest,
    SimulationStatus,
    SimulationResponse,
)
from src.engine.cashflow import CashFlowEngine
from src.engine.real_options import RealOptionsEngine
from src.api.routes import p1, analysis, wizard
from src.services.task_queue import TaskDispatcher

# Security imports
from src.infrastructure.auth import (
    get_current_user,
    get_optional_user,
    CurrentUser
)
from src.infrastructure.rate_limiter import (
    RateLimitMiddleware,
    default_limiter,
    check_simulation_rate_limit
)

import uuid
import traceback

# Environment
ENV = os.getenv("ENV", "development")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://vertiv.tech,http://localhost:3000").split(",")

app = FastAPI(
    title="VERTIV v6.0 API",
    version="6.1.0-SINGULARITY",
    description="Global Edition - Real Estate Viability Analysis Platform with Bank-Grade Security"
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
    exclude_paths=["/health", "/docs", "/openapi.json", "/redoc"]
)

# Include routers
app.include_router(p1.router)
app.include_router(analysis.router)
app.include_router(wizard.router)


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
        "security": "enabled"
    }


# ============================================================================
# PROTECTED ENDPOINTS (Auth Required)
# ============================================================================

@app.get("/simulations", response_model=list[dict])
async def list_simulations(
    limit: int = 10,
    offset: int = 0,
    user: CurrentUser = Depends(get_current_user)
):
    """
    List simulations for the authenticated user's portfolio view.
    Requires JWT authentication.
    """
    repo = SimulationRepository()
    return repo.get_latest(limit)


@app.get("/simulations/recent", response_model=list[dict])
async def get_recent_simulations(
    limit: int = 1,
    user: CurrentUser = Depends(get_current_user)
):
    """Get recent simulations for the authenticated user."""
    repo = SimulationRepository()
    return repo.get_latest(limit)


@app.get("/simulation/{simulation_id}", response_model=SimulationResponse)
async def get_simulation(
    simulation_id: str,
    user: CurrentUser = Depends(get_current_user)
):
    """
    Retrieves the status and result of a simulation.
    Requires JWT authentication.
    """
    repo = SimulationRepository()
    data = repo.get(simulation_id)

    if not data:
        raise HTTPException(status_code=404, detail="Simulation not found")

    return SimulationResponse(
        simulation_id=data["id"],
        status=data["status"],
        result=data.get("result"),
        error=data.get("result", {}).get("error") if data.get("result") else None,
    )


@app.post("/calculate/quick", response_model=SimulationResponse)
async def calculate_quick(
    project: ProjectTIV,
    request: Request,
    user: CurrentUser = Depends(get_current_user),
    _rate_limit: None = Depends(check_simulation_rate_limit)
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
        project_data["user_id"] = user.id
        repo.create(sim_id, project_data)
    except Exception as e:
        print(f"Database Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database Persistence Failed: {str(e)}"
        )

    # Dispatch Request
    try:
        task_name = await TaskDispatcher.dispatch_simulation(request_payload)
        print(f"[DISPATCH] Simulation {sim_id}: Task {task_name}")

        return SimulationResponse(
            simulation_id=sim_id,
            status=SimulationStatus.PENDING,
            result=None
        )
    except Exception as e:
        traceback.print_exc()
        return SimulationResponse(
            simulation_id=sim_id,
            status=SimulationStatus.FAILED,
            error=str(e)
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
        "authenticated": True
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
