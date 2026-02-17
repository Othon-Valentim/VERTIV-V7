"""
VERTIV v6.1.0-SINGULARITY Worker
Financial Calculation Engine with Dynamic ROE/Payback
"""

from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
import math
from decimal import Decimal
import traceback
from supabase import create_client

# Supabase Client
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
supabase_client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"WARNING: Could not init Supabase: {e}")

# Backend Path Tropicalization (Support for Docker and Local)
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../apps/worker/core
root_dir = os.path.abspath(os.path.join(current_dir, "../../..")) # .../VERTIV_V6_GLOBAL
backend_path_local = os.path.join(root_dir, "apps", "backend")

BACKEND_PATH_DOCKER = "/apps/backend"

if os.path.exists(BACKEND_PATH_DOCKER):
    if BACKEND_PATH_DOCKER not in sys.path:
        sys.path.insert(0, BACKEND_PATH_DOCKER)
elif os.path.exists(backend_path_local):
    if backend_path_local not in sys.path:
        sys.path.insert(0, backend_path_local)
else:
    print(f"WARNING: Backend path not found. Local: {backend_path_local}, Docker: {BACKEND_PATH_DOCKER}")

try:
    from src.domain.schemas import (
        SimulationRequest,
        SimulationResponse,
        SimulationStatus,
        P10FinancialOutput,
    )
    from src.engine.cashflow import CashFlowEngine
    from src.engine.real_options import RealOptionsEngine
    from core.scout_agent import ScoutAgent
    from src.vertiv.biz import tropicalize

    scout_agent = ScoutAgent()
    print("[WORKER] Backend Modules & ScoutAgent Imported Successfully")
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import backend modules: {e}")
    SimulationRequest = BaseModel
    SimulationResponse = BaseModel
    SimulationStatus = None
    CashFlowEngine = None
    RealOptionsEngine = None
    tropicalize = lambda k, d: d  # Fallback if import fails

app = FastAPI(title="VERTIV Worker", version="6.1.0-SINGULARITY")


def safe_float(v):
    try:
        if v is None:
            return 0.0
        val = float(v)
        if math.isnan(val) or math.isinf(val):
            return 0.0
        return val
    except:
        return 0.0


def to_dec(v):
    try:
        return Decimal(str(safe_float(v)))
    except:
        return Decimal("0")


def calculate_roe(
    total_profit: float, land_cost: float, equity_pct: float = 0.30
) -> float:
    """ROE = Net Profit / Equity Invested (30% equity standard)."""
    if land_cost <= 0 or equity_pct <= 0:
        return 0.0
    equity = land_cost * equity_pct
    return round(total_profit / equity, 4) if equity > 0 else 0.0


def calculate_payback_months(cashflow_series: list) -> int:
    """Month where cumulative CF turns positive."""
    if not cashflow_series:
        return 0
    cumulative = 0.0
    for month, cf in enumerate(cashflow_series):
        cumulative += cf
        if cumulative > 0:
            return month + 1
    return len(cashflow_series)


def calculate_max_exposure(cashflow_series: list) -> float:
    """Maximum Cash Exposure (Cash Valley)."""
    if not cashflow_series:
        return 0.0
    cumulative = 0.0
    min_val = 0.0
    for cf in cashflow_series:
        cumulative += cf
        min_val = min(min_val, cumulative)
    return abs(min_val)


def sanitize_payload(data):
    try:
        import numpy as np
    except ImportError:
        np = None
    try:
        import polars as pl
    except ImportError:
        pl = None

    if isinstance(data, dict):
        return {k: sanitize_payload(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_payload(v) for v in data]
    elif isinstance(data, Decimal):
        return float(data)
    elif np and isinstance(data, (np.integer, np.int64, np.int32)):
        return int(data)
    elif np and isinstance(data, (np.floating, np.float64, np.float32)):
        return float(data)
    elif np and isinstance(data, np.ndarray):
        return sanitize_payload(data.tolist())
    elif pl and isinstance(data, pl.DataFrame):
        return sanitize_payload(data.to_dicts())
    elif pl and isinstance(data, pl.Series):
        return sanitize_payload(data.to_list())
    return data


@app.post("/tasks/process-simulation", response_model=SimulationResponse)
async def process_simulation(payload: SimulationRequest):
    """v6.1.0-SINGULARITY: Dynamic ROE, Payback, Max Exposure."""
    print(f"[WORKER] Processing: {payload.simulation_id}")

    project = payload.project
    f_input = project.financial_input

    if not f_input:
        return SimulationResponse(
            simulation_id=payload.simulation_id,
            status=SimulationStatus.FAILED,
            error="Missing financial_input",
        )

    # 1. Scout Intelligence (v6.1.0 Singularity)
    # If the project is mixed-use or missing pricing details, we scout.
    if project.is_mixed_use or (f_input and safe_float(f_input.sales_price_avg) == 0):
        try:
            print(f"[WORKER] Launching ScoutAgent for project: {project.name}")
            # Update Narrative for Frontend
            if supabase_client:
                supabase_client.table("simulations").update(
                    {"narrative_status": "Obtendo inteligencia de mercado (Serper.dev)..."}
                ).eq("id", payload.simulation_id).execute()

            municipality = getattr(project, 'municipality', 'Belo Horizonte')
            neighborhood = getattr(project, 'neighborhood', 'Centro')
            
            # Since we are in an async endpoint, we await
            competitors = await scout_agent.scout_competitors(
                municipality=municipality,
                neighborhood=neighborhood,
                product_type="MISTO" if project.is_mixed_use else "RESIDENCIAL"
            )
            print(f"[WORKER] ScoutAgent found {len(competitors)} results.")

            # Calculate detected market average if possible
            if competitors:
                valid_prices = [c['price_sqm'] for c in competitors if c['price_sqm'] > 0]
                if valid_prices:
                    market_avg = sum(valid_prices) / len(valid_prices)
                    print(f"[WORKER] Market Intelligence: Avg Price detected at R$ {market_avg:,.2f}/m2")
                    # Optionally adjust project pricing if it was zero
                    if safe_float(f_input.sales_price_avg) == 0:
                        f_input.sales_price_avg = market_avg

            if supabase_client:
                msg = f"Inteligência de mercado sincronizada ({len(competitors)} fontes). Preço detectado: R$ {f_input.sales_price_avg:,.2f}/m2"
                supabase_client.table("simulations").update(
                    {"narrative_status": msg}
                ).eq("id", payload.simulation_id).execute()

        except Exception as scout_e:
            print(f"[WORKER] ScoutAgent failed: {scout_e}")
            if supabase_client:
                supabase_client.table("simulations").update(
                    {"narrative_status": "Busca em tempo real falhou. Usando médias históricas conservadoras."}
                ).eq("id", payload.simulation_id).execute()

    land_cost = safe_float(f_input.land_cost)
    construction_cost = safe_float(f_input.construction_cost_total)

    # 1. Cash Flow & ESG (RICS Integration)
    try:
        base_wacc = tropicalize("WACC_ANNUAL", 0.145)  # Standard 14.5%
        greenium = safe_float(project.esg.green_premium)
        brown_discount = safe_float(project.esg.brown_discount)

        # RICS Adjusted WACC logic
        adjusted_wacc = base_wacc - greenium + brown_discount
        print(
            f"[WORKER] WACC Logic | Base: {base_wacc:.2%} | Greenium: -{greenium:.2%} | Brown: +{brown_discount:.2%} | Final: {adjusted_wacc:.2%}"
        )

        cf_engine = CashFlowEngine(months=f_input.development_months + 24)
        cf_results = cf_engine.calculate_project_cashflow(
            units=f_input.total_units,
            avg_price=safe_float(f_input.sales_price_avg),
            cost_total=construction_cost,
            start_sales_month=6,
            wacc_annual=adjusted_wacc,
            # v6.1.0 Tropicalization Params
            use_ret=f_input.use_ret_taxation,
            permuta_pct=f_input.permuta_physical_pct,
            funding_model=f_input.funding_model,
            incc_annual=f_input.incc_annual_rate,
            ipca_annual=f_input.ipca_annual_rate,
        )
        metrics = cf_results["metrics"]
        cashflow_data = cf_results.get("dataframe", [])
        cashflow_series = [row.get("net_cash_flow", 0) for row in cashflow_data]

        dcf_npv = safe_float(metrics["npv"])
        irr_val = safe_float(metrics["irr"])
        print(
            f"[WORKER] Metrics | NPV: {dcf_npv:,.2f} | IRR: {irr_val:.2f}% | Taxes: {safe_float(metrics.get('total_taxes')):,.2f}"
        )

    except Exception as e:
        traceback.print_exc()
        return SimulationResponse(
            simulation_id=payload.simulation_id,
            status=SimulationStatus.FAILED,
            error=f"CashFlow Error: {str(e)}",
        )

    # 2. Dynamic Metrics
    roe_val = calculate_roe(dcf_npv, land_cost)
    payback = calculate_payback_months(cashflow_series)
    max_exp = calculate_max_exposure(cashflow_series)
    print(
        f"[WORKER] ROE: {roe_val:.2%} | Payback: {payback}mo | MaxExp: {max_exp:,.2f}"
    )

    # 3. Real Options
    ro_value = 0.0
    if project.real_options:
        try:
            ro_value = safe_float(
                RealOptionsEngine.calculate_land_option_value(
                    land_value_current=safe_float(
                        project.real_options.land_value_current
                    ),
                    development_cost=safe_float(
                        project.real_options.development_cost_forcing
                    ),
                    time_to_permit_years=safe_float(
                        project.real_options.time_to_permit_years
                    ),
                    volatility=safe_float(project.real_options.volatility),
                    risk_free_rate=safe_float(project.real_options.risk_free_rate),
                )
            )
        except Exception as ro_e:
            print(f"[WORKER] RO Error: {ro_e}")

    # 4. Final Aggregation
    final_npv = dcf_npv + ro_value

    # 5. Build Result
    try:
        result = P10FinancialOutput(
            npv=to_dec(dcf_npv),
            irr=irr_val,
            roe=roe_val,
            payback_months=payback,
            exposure_max=to_dec(max_exp),
            esg_adjusted_npv=to_dec(final_npv),
            real_option_land_value=ro_value,
        )
        clean = sanitize_payload(result.model_dump())
        final_result = P10FinancialOutput(**clean)
    except Exception as e:
        traceback.print_exc()
        return SimulationResponse(
            simulation_id=payload.simulation_id,
            status=SimulationStatus.FAILED,
            error=f"Output Error: {str(e)}",
        )

    # 6. DB Update
    if supabase_client:
        try:
            supabase_client.table("simulations").update(
                {"status": "COMPLETED", "result": final_result.model_dump(mode="json")}
            ).eq("id", payload.simulation_id).execute()
            print(f"[WORKER] DB Updated: {payload.simulation_id}")
        except Exception as db_e:
            print(f"[WORKER] DB Error: {db_e}")

    return SimulationResponse(
        simulation_id=payload.simulation_id,
        status=SimulationStatus.COMPLETED,
        result=final_result,
    )


@app.get("/health")
def health():
    return {"status": "ok", "service": "worker", "version": "6.1.0-SINGULARITY"}
