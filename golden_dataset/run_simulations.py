"""
VERTIV V7 — Golden Dataset Simulation Runner (v2 - Fixed)
Runs all engines P1→P10 + RealOptions on benchmark projects.

Fixes from v1:
- CashFlow→P3 data pipe: extract net_cash_flow from dataframe dicts
- Trim trailing zero months from cashflow before IRR calculation
- Correct IRR reading from CashFlow metrics (already ×100)
- Use CashFlow metrics as primary financial output

Usage: python golden_dataset/run_simulations.py
"""

import json
import math
import sys
import os
from pathlib import Path
from decimal import Decimal
from typing import Any

# Add backend paths: apps/backend (for 'from src.vertiv.biz') and
# apps/backend/src (for 'from engine.xxx' and 'from domain.xxx')
BACKEND_ROOT = Path(__file__).parent.parent / "apps" / "backend"
BACKEND_SRC = BACKEND_ROOT / "src"
sys.path.insert(0, str(BACKEND_ROOT))
sys.path.insert(0, str(BACKEND_SRC))

from domain.schemas import P1GarimpoInput, ESGAttributes
from engine.p1_screener import P1ScreenerEngine
from engine.p2_economic import P2EconomicEngine
from engine.p3_projection import P3ProjectionEngine
from engine.p4_vocation import P4VocationEngine
from engine.p5_legal import P5LegalEngine
from engine.p6_p9_market import (
    P6DemandEngine,
    P7SupplyEngine,
    P8AbsorptionEngine,
    P9ValidationEngine,
    P6DemandInput,
    P7SupplyInput,
    P8AbsorptionInput,
    P9ValidationInput,
    CompetitorProject,
)
from engine.cashflow import CashFlowEngine
from engine.real_options import RealOptionsEngine


def load_benchmark_projects(path: str) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def decimal_serializer(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return 0.0
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def trim_trailing_zeros(cashflow: list[float]) -> list[float]:
    """Remove trailing zero-value months that corrupt IRR calculation.

    The CashFlow engine generates 361 months but only ~36 are active.
    Trailing zeros make npf.irr() converge to nonsensical values.
    Keep at least 1 trailing zero to mark project end.
    """
    if not cashflow:
        return cashflow
    last_nonzero = len(cashflow) - 1
    while last_nonzero > 0 and abs(cashflow[last_nonzero]) < 0.01:
        last_nonzero -= 1
    # Keep 1 extra month after last nonzero for clean termination
    return cashflow[: last_nonzero + 2]


# ─────────────────────── Engine Runners ───────────────────────


def run_p1(project: dict) -> dict:
    engine = P1ScreenerEngine()
    p1_data = project["p1"]
    input_data = P1GarimpoInput(
        location_municipality=p1_data["location_municipality"],
        location_neighborhood=p1_data["location_neighborhood"],
        area_sqm=p1_data["area_sqm"],
        asking_price=Decimal(str(p1_data["asking_price"])),
    )
    result = engine.analyze(input_data)
    return result.model_dump()


def run_p2(project: dict) -> dict:
    engine = P2EconomicEngine()
    pop = project["p6"]["influence_area_population"]
    return engine.analyze_sync(
        municipality=project["municipality"],
        municipality_population=pop,
        is_metropolitan=pop > 500000,
    )


def run_p4(project: dict) -> dict:
    engine = P4VocationEngine()
    p4_data = project["p4"].copy()
    p4_data["land_price_per_sqm"] = Decimal(str(p4_data["land_price_per_sqm"]))
    from engine.p4_vocation import P4VocationInput

    return engine.analyze(P4VocationInput(**p4_data))


def run_p5(project: dict) -> dict:
    engine = P5LegalEngine()
    from engine.p5_legal import P5LegalInput

    return engine.analyze(P5LegalInput(**project["p5"]))


def run_p6(project: dict) -> dict:
    engine = P6DemandEngine()
    p6_data = project["p6"].copy()
    p6_data["average_household_income"] = Decimal(
        str(p6_data["average_household_income"])
    )
    p6_data["unit_price_min"] = Decimal(str(p6_data["unit_price_min"]))
    p6_data["unit_price_max"] = Decimal(str(p6_data["unit_price_max"]))
    return engine.analyze(P6DemandInput(**p6_data))


def run_p7(project: dict) -> dict:
    import asyncio

    engine = P7SupplyEngine()
    p7_data = project["p7"].copy()
    competitors = []
    for c in p7_data.get("competitors", []):
        c_copy = c.copy()
        c_copy["price_per_sqm"] = Decimal(str(c_copy["price_per_sqm"]))
        competitors.append(CompetitorProject(**c_copy))
    p7_data["competitors"] = competitors
    if p7_data.get("market_average_price_sqm") is not None:
        p7_data["market_average_price_sqm"] = Decimal(
            str(p7_data["market_average_price_sqm"])
        )
    return asyncio.run(engine.analyze(P7SupplyInput(**p7_data)))


def run_p8(project: dict) -> dict:
    engine = P8AbsorptionEngine()
    p8_data = project["p8"].copy()
    p8_data["project_price_avg"] = Decimal(str(p8_data["project_price_avg"]))
    return engine.analyze(P8AbsorptionInput(**p8_data))


def run_p9(project: dict, p6_result: dict, p7_result: dict, p8_result: dict) -> dict:
    engine = P9ValidationEngine()
    p = project["p8"]
    input_data = P9ValidationInput(
        municipality=project["municipality"],
        qualified_demand=p6_result["summary"]["qualified_demand_units"],
        active_inventory=p7_result["summary"]["active_inventory_units"],
        competitors_count=p7_result["summary"]["competitors_count"],
        projected_absorption_months=p8_result["absorption_projection"][
            "projected_absorption_months"
        ],
        project_units=p["project_units"],
        project_price_sqm=(
            Decimal(str(p7_result["pricing_analysis"]["average_price_sqm"]))
            if p7_result["pricing_analysis"]["average_price_sqm"]
            else Decimal("5000")
        ),
        market_price_sqm=(
            Decimal(str(p7_result["pricing_analysis"]["average_price_sqm"]))
            if p7_result["pricing_analysis"]["average_price_sqm"]
            else Decimal("5000")
        ),
    )
    return engine.analyze(input_data)


def run_cashflow(project: dict) -> dict:
    """Run CashFlow Engine with project-specific construction period."""
    p10 = project["p10"]
    construction_months = p10["development_months"]
    # CashFlow engine period = construction + 12 month buffer
    engine = CashFlowEngine(months=construction_months + 12)
    return engine.calculate_project_cashflow(
        units=p10["total_units"],
        avg_price=p10["sales_price_avg"],
        cost_total=p10["construction_cost_total"],
        land_cost=p10.get("land_cost", project.get("p1", {}).get("asking_price", 0)),
        start_sales_month=6,
        construction_months=construction_months,
        wacc_annual=None,
        use_ret=p10.get("use_ret_taxation", True),
        permuta_pct=p10.get("permuta_physical_pct", 0.0),
        funding_model=p10.get("funding_model", "SBPE"),
        incc_annual=p10.get("incc_annual_rate"),
        ipca_annual=p10.get("ipca_annual_rate"),
    )


def run_p3(cashflow_result: dict) -> dict:
    """Run P3 Projection Engine on cashflow dataframe output.

    FIX: CashFlow returns {dataframe: [{month, net_cash_flow, ...}, ...], metrics: {...}}
    We extract net_cash_flow from each row and trim trailing zeros.
    """
    engine = P3ProjectionEngine()
    df_rows = cashflow_result.get("dataframe", [])
    if not df_rows:
        return {"error": "No cashflow dataframe rows"}

    # Extract the monthly net_cash_flow series
    monthly_cashflow = [row.get("net_cash_flow", 0.0) for row in df_rows]

    # Trim trailing zeros to fix IRR convergence
    monthly_cashflow = trim_trailing_zeros(monthly_cashflow)

    if not monthly_cashflow:
        return {"error": "Empty cashflow after trimming"}

    return engine.calculate_indicators(monthly_cashflow)


def run_real_options(project: dict) -> float:
    engine = RealOptionsEngine()
    ro = project.get("real_options")
    if not ro:
        return 0.0
    return engine.calculate_land_option_value(
        land_value_current=ro["land_value_current"],
        development_cost=ro["development_cost_forcing"],
        time_to_permit_years=ro["time_to_permit_years"],
        volatility=ro.get("volatility", 0.20),
        risk_free_rate=ro.get("risk_free_rate", 0.11),
    )


# ─────────────────────── Main Pipeline ───────────────────────


def run_full_simulation(project: dict) -> dict:
    """Run all engines P1→P10 + RealOptions for a project."""
    project_name = project["project_name"]
    dataset_id = project["dataset_id"]

    print(f"\n{'='*70}")
    print(f"  SIMULAÇÃO: {project_name}")
    print(f"  ID: {dataset_id}")
    print(f"{'='*70}")

    results: dict[str, Any] = {
        "dataset_id": dataset_id,
        "project_name": project_name,
        "municipality": project["municipality"],
    }

    # P1: Screener
    try:
        print("  [P1] Garimpo Screener...", end=" ")
        results["p1"] = run_p1(project)
        print(
            f"✅ Score: {results['p1']['score_attractiveness']:.1f} | {results['p1']['decision']}"
        )
    except Exception as e:
        results["p1"] = {"error": str(e)}
        print(f"❌ {e}")

    # P2: Economic
    try:
        print("  [P2] Economic Analysis...", end=" ")
        results["p2"] = run_p2(project)
        print(
            f"✅ Score: {results['p2']['p2i_lead_score']:.1f} | {'GO' if results['p2']['is_favorable'] else 'NO-GO'}"
        )
    except Exception as e:
        results["p2"] = {"error": str(e)}
        print(f"❌ {e}")

    # P4: Vocation
    try:
        print("  [P4] Vocation Analysis...", end=" ")
        results["p4"] = run_p4(project)
        print("✅")
    except Exception as e:
        results["p4"] = {"error": str(e)}
        print(f"❌ {e}")

    # P5: Legal
    try:
        print("  [P5] Legal Due Diligence...", end=" ")
        results["p5"] = run_p5(project)
        print("✅")
    except Exception as e:
        results["p5"] = {"error": str(e)}
        print(f"❌ {e}")

    # P6: Demand
    try:
        print("  [P6] Demand Funnel...", end=" ")
        results["p6"] = run_p6(project)
        demand_units = results["p6"]["summary"]["qualified_demand_units"]
        print(f"✅ Qualified Demand: {demand_units:,} units")
    except Exception as e:
        results["p6"] = {"error": str(e)}
        print(f"❌ {e}")

    # P7: Supply
    try:
        print("  [P7] Supply Analysis...", end=" ")
        results["p7"] = run_p7(project)
        sat = results["p7"]["summary"]["market_saturation"]
        print(f"✅ Saturation: {sat}")
    except Exception as e:
        results["p7"] = {"error": str(e)}
        print(f"❌ {e}")

    # P8: Absorption
    try:
        print("  [P8] Absorption VSO...", end=" ")
        results["p8"] = run_p8(project)
        months = results["p8"]["absorption_projection"]["projected_absorption_months"]
        assess = results["p8"]["absorption_projection"]["assessment"]
        print(f"✅ {months} months | {assess}")
    except Exception as e:
        results["p8"] = {"error": str(e)}
        print(f"❌ {e}")

    # P9: Validation Gate 4:1
    try:
        print("  [P9] Gate 4:1 Validation...", end=" ")
        results["p9"] = run_p9(project, results["p6"], results["p7"], results["p8"])
        decision = results["p9"]["gate_result"]["decision"]
        ratio = results["p9"]["key_ratio"]["gate_4_1_ratio"]
        print(f"✅ Decision: {decision} | Ratio: {ratio}")
    except Exception as e:
        results["p9"] = {"error": str(e)}
        print(f"❌ {e}")

    # CashFlow + P3 (Financial Projection)
    try:
        print("  [CF] CashFlow Engine...", end=" ")
        cf_result = run_cashflow(project)
        # Don't store the full dataframe in results (too large)
        results["cashflow_metrics"] = cf_result.get("metrics", {})
        total_rev = cf_result.get("metrics", {}).get("total_revenue", 0)
        print(f"✅ Total Revenue: R$ {total_rev:,.2f}")

        print("  [P3] Financial Projection...", end=" ")
        results["p3"] = run_p3(cf_result)
        npv = results["p3"].get("npv", 0)
        # P3 returns irr as annual decimal (e.g., 0.25 = 25%)
        irr_annual = results["p3"].get("irr", 0)
        roi = results["p3"].get("roi", 0)
        is_viable = results["p3"].get("is_viable", False)
        print(
            f"✅ VPL: R$ {npv:,.2f} | TIR: {irr_annual*100:.1f}% a.a. | ROI: {roi*100:.1f}% | {'VIÁVEL ✅' if is_viable else 'INVIÁVEL ❌'}"
        )
    except Exception as e:
        results["cashflow_metrics"] = {"error": str(e)}
        results["p3"] = {"error": str(e)}
        print(f"❌ {e}")

    # Real Options
    try:
        print("  [RO] Real Options (Black-Scholes)...", end=" ")
        results["real_options_value"] = run_real_options(project)
        print(f"✅ Option Value: R$ {results['real_options_value']:,.2f}")
    except Exception as e:
        results["real_options_value"] = 0.0
        print(f"❌ {e}")

    # ──── FINAL SUMMARY ────
    print(f"\n  {'─'*55}")
    p3 = results.get("p3", {})
    p9 = results.get("p9", {})
    cf = results.get("cashflow_metrics", {})

    npv_val = p3.get("npv", 0)
    irr_val = p3.get("irr", 0) * 100  # Already annualized by P3
    roi_val = p3.get("roi", 0) * 100
    p9_gate = p9.get("gate_result", {}).get("decision", "N/A")
    viable = p3.get("is_viable", False)

    print(f"  📊 RESULTADO FINAL:")
    print(f"     VPL (NPV):     R$ {npv_val:>18,.2f}")
    print(f"     TIR (IRR):        {irr_val:>15.1f}% a.a.")
    print(f"     ROI:              {roi_val:>15.1f}%")
    print(f"     Lucro Total:   R$ {cf.get('total_profit', 0):>18,.2f}")
    print(f"     Gate P9:          {p9_gate:>15}")
    print(f"     Viável:           {'SIM ✅' if viable else 'NÃO ❌':>15}")
    print(f"  {'─'*55}")

    return results


def main() -> None:
    """Run full simulation pipeline on all benchmark projects."""
    golden_path = Path(__file__).parent / "benchmark_projects.json"
    output_path = Path(__file__).parent / "simulation_results.json"
    summary_path = Path(__file__).parent / "summary_output.txt"

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  VERTIV V7 — GOLDEN DATASET SIMULATION RUNNER (v2)         ║")
    print("║  Calibração de Engines P1→P10 + Real Options               ║")
    print("║  Fixes: CashFlow→P3 pipe, IRR trim, correct field names    ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    projects = load_benchmark_projects(str(golden_path))
    print(f"\n  📂 {len(projects)} projetos carregados de benchmark_projects.json")

    all_results = []
    for project in projects:
        result = run_full_simulation(project)
        all_results.append(result)

    # Save full results JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            all_results, f, indent=2, ensure_ascii=False, default=decimal_serializer
        )

    # Save summary table
    header = f"{'ID':<13}{'Projeto':<50}{'VPL (R$)':>18}{'TIR %aa':>10}{'ROI%':>10}{'Viavel':>8}{'P9':>10}{'RealOpt':>15}"
    sep = "─" * 134
    lines = [header, sep]

    for r in all_results:
        p3 = r.get("p3", {})
        npv = p3.get("npv", 0)
        irr = p3.get("irr", 0) * 100
        roi = p3.get("roi", 0) * 100
        viable = p3.get("is_viable", False)
        p9 = r.get("p9", {}).get("gate_result", {}).get("decision", "N/A")
        ro = r.get("real_options_value", 0)
        lines.append(
            f"{r['dataset_id']:<13}"
            f"{r['project_name'][:47]:<50}"
            f"{npv:>18,.2f}"
            f"{irr:>9.1f}%"
            f"{roi:>9.1f}%"
            f"{'True' if viable else 'False':>8}"
            f"{p9:>10}"
            f"{ro:>15,.2f}"
        )

    # P2 scores
    lines.append("")
    lines.append("P2 Economic Scores:")
    for r in all_results:
        p2 = r.get("p2", {})
        score = p2.get("p2i_lead_score", 0)
        decision = "GO" if p2.get("is_favorable") else "NO-GO"
        selic = p2.get("live_indicators", {}).get("selic_rate", "?")
        lines.append(
            f"  {r['dataset_id']}: Score={score}/50 Decision={decision} Selic={selic}%"
        )

    # P6 Demand scores
    lines.append("")
    lines.append("P6 Demand (Qualified Units):")
    for r in all_results:
        p6 = r.get("p6", {})
        demand = p6.get("summary", {}).get("qualified_demand_units", 0)
        eff = p6.get("funnel_efficiency", 0)
        lines.append(
            f"  {r['dataset_id']}: Demand={demand:,} units | Funnel Eff={eff}%"
        )

    # P9 Gate details
    lines.append("")
    lines.append("P9 Gate 4:1 Details:")
    for r in all_results:
        p9 = r.get("p9", {})
        ratio = p9.get("key_ratio", {}).get("gate_4_1_ratio", 0)
        demand = p9.get("key_ratio", {}).get("qualified_demand", 0)
        supply = p9.get("key_ratio", {}).get("total_supply", 0)
        decision = p9.get("gate_result", {}).get("decision", "N/A")
        lines.append(
            f"  {r['dataset_id']}: Ratio={ratio} (Demand={demand:,}/Supply={supply:,}) → {decision}"
        )

    summary_text = "\n".join(lines)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(f"\n\n{'='*70}")
    print(f"  ✅ RESULTADOS SALVOS:")
    print(f"     📄 {output_path}")
    print(f"     📊 {summary_path}")
    print(f"{'='*70}")

    # Final summary table
    print(f"\n  {'Projeto':<50} {'VPL (R$)':>18} {'TIR':>9} {'ROI':>9} {'P9':>8}")
    print(f"  {'─'*96}")
    for r in all_results:
        name = r["project_name"][:47]
        p3 = r.get("p3", {})
        npv = p3.get("npv", 0)
        irr = p3.get("irr", 0) * 100
        roi = p3.get("roi", 0) * 100
        p9 = r.get("p9", {}).get("gate_result", {}).get("decision", "N/A")
        print(f"  {name:<50} {npv:>18,.2f} {irr:>8.1f}% {roi:>8.1f}% {p9:>8}")


if __name__ == "__main__":
    main()
