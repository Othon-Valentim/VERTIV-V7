"""
VERTIV V7 — Shadow Backtesting Engine
Runs all 15 golden projects through V7 engines and compares against
historical V6 simulation_results.json using GoldenEvaluator.

Usage: python golden_dataset/backtest_v7.py

Output:
  - golden_dataset/backtest_report.json  (full detail)
  - golden_dataset/backtest_summary.txt  (human-readable)
"""

import json
import math
import sys
import os
from pathlib import Path
from decimal import Decimal
from typing import Any, Dict, List, Tuple
from datetime import datetime

# ──── Path Setup ────
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_ROOT = PROJECT_ROOT / "apps" / "backend"
BACKEND_SRC = BACKEND_ROOT / "src"
WORKER_ROOT = PROJECT_ROOT / "apps" / "worker"
WORKER_SRC = WORKER_ROOT / "src"

sys.path.insert(0, str(BACKEND_ROOT))
sys.path.insert(0, str(BACKEND_SRC))
sys.path.insert(0, str(WORKER_SRC))

# ──── Import Engines (same as run_simulations.py) ────
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

# ──── Import V7 Validation ────
from services.validation.golden_evaluator import GoldenEvaluator
from services.validation.triage import determine_operation_level


def decimal_serializer(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return 0.0
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def trim_trailing_zeros(cashflow: list[float]) -> list[float]:
    if not cashflow:
        return cashflow
    last_nonzero = len(cashflow) - 1
    while last_nonzero > 0 and abs(cashflow[last_nonzero]) < 0.01:
        last_nonzero -= 1
    return cashflow[: last_nonzero + 2]


# ─────────────────────── Engine Runners (from run_simulations.py) ───────────────────────


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
    p10 = project["p10"]
    construction_months = p10["development_months"]
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
    engine = P3ProjectionEngine()
    df_rows = cashflow_result.get("dataframe", [])
    if not df_rows:
        return {"error": "No cashflow dataframe rows"}
    monthly_cashflow = [row.get("net_cash_flow", 0.0) for row in df_rows]
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


# ─────────────────────── Flatten for Comparison ───────────────────────


def flatten_financials(result: dict) -> Dict[str, Any]:
    """Extract critical financial fields for GoldenEvaluator comparison."""
    p3 = result.get("p3", {})
    cf = result.get("cashflow_metrics", {})
    p1 = result.get("p1", {})
    p5 = result.get("p5", {})
    p9 = result.get("p9", {})

    flat: Dict[str, Any] = {}

    # P3 — Core financials (VPL is the king metric)
    flat["npv"] = p3.get("npv", 0)
    flat["irr"] = p3.get("irr", 0)
    flat["roi"] = p3.get("roi", 0)
    flat["max_exposure"] = p3.get("max_exposure", 0)
    flat["payback_months"] = p3.get("payback_months", 0)
    flat["is_viable"] = p3.get("is_viable", False)

    # CashFlow metrics
    flat["total_revenue"] = cf.get("total_revenue", 0)
    flat["total_cost"] = cf.get("total_cost", 0)
    flat["total_profit"] = cf.get("total_profit", 0)
    flat["margin_pct"] = cf.get("margin_pct", 0)

    # P1 — Screener
    flat["p1_score"] = p1.get("score_attractiveness", 0)
    flat["p1_decision"] = p1.get("decision", "N/A")

    # P5 — Legal gate
    p5_gate = p5.get("gate_result", {})
    flat["p5_decision"] = p5_gate.get("decision", "N/A")
    flat["p5_compliance_score"] = p5.get("summary", {}).get("compliance_score", 0)

    # P9 — Market gate
    p9_gate = p9.get("gate_result", {})
    flat["p9_decision"] = p9_gate.get("decision", "N/A")
    flat["p9_ratio"] = p9.get("key_ratio", {}).get("gate_4_1_ratio", 0)

    # Real Options
    flat["real_options_value"] = result.get("real_options_value", 0)

    return flat


# ─────────────────────── Main Backtest ───────────────────────


def main() -> None:
    golden_path = Path(__file__).parent / "benchmark_projects.json"
    golden_results_path = Path(__file__).parent / "simulation_results.json"
    report_path = Path(__file__).parent / "backtest_report.json"
    summary_path = Path(__file__).parent / "backtest_summary.txt"

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  VERTIV V7 — SHADOW BACKTESTING ENGINE                     ║")
    print("║  GoldenEvaluator: MAPE ≤ 5% (campos) + MAPE ≤ 2% (VPL)    ║")
    print("║  Triage: 4 operation levels                                ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # Load inputs + golden reference
    projects = json.loads(golden_path.read_text(encoding="utf-8"))
    golden_results = json.loads(golden_results_path.read_text(encoding="utf-8"))
    golden_map = {r["dataset_id"]: r for r in golden_results}

    print(f"\n  📂 {len(projects)} projetos carregados")
    print(f"  📊 {len(golden_results)} golden references carregadas\n")

    evaluator = GoldenEvaluator()
    all_reports: List[dict] = []

    total_pass = 0
    total_fail = 0

    for i, project in enumerate(projects):
        dataset_id = project["dataset_id"]
        project_name = project["project_name"]
        golden_ref = golden_map.get(dataset_id)

        if not golden_ref:
            print(f"  ⚠️  {dataset_id} — Sem golden reference, pulando")
            continue

        print(f"\n{'─'*70}")
        print(f"  [{i+1:02d}/{len(projects)}] {project_name}")
        print(f"  ID: {dataset_id}")
        print(f"{'─'*70}")

        # ──── Re-run engines (fresh V7 execution) ────
        v7_result: Dict[str, Any] = {
            "dataset_id": dataset_id,
            "project_name": project_name,
        }

        errors: List[str] = []

        # P1
        try:
            v7_result["p1"] = run_p1(project)
            print(f"  [P1] ✅ Score: {v7_result['p1']['score_attractiveness']:.1f}")
        except Exception as e:
            v7_result["p1"] = {"error": str(e)}
            errors.append(f"P1: {e}")
            print(f"  [P1] ❌ {e}")

        # P2
        try:
            v7_result["p2"] = run_p2(project)
            print(f"  [P2] ✅ Score: {v7_result['p2']['p2i_lead_score']:.1f}")
        except Exception as e:
            v7_result["p2"] = {"error": str(e)}
            errors.append(f"P2: {e}")
            print(f"  [P2] ❌ {e}")

        # P4
        try:
            v7_result["p4"] = run_p4(project)
            print(f"  [P4] ✅")
        except Exception as e:
            v7_result["p4"] = {"error": str(e)}
            errors.append(f"P4: {e}")
            print(f"  [P4] ❌ {e}")

        # P5
        try:
            v7_result["p5"] = run_p5(project)
            print(f"  [P5] ✅")
        except Exception as e:
            v7_result["p5"] = {"error": str(e)}
            errors.append(f"P5: {e}")
            print(f"  [P5] ❌ {e}")

        # P6
        try:
            v7_result["p6"] = run_p6(project)
            print(
                f"  [P6] ✅ Demand: {v7_result['p6']['summary']['qualified_demand_units']:,}"
            )
        except Exception as e:
            v7_result["p6"] = {"error": str(e)}
            errors.append(f"P6: {e}")
            print(f"  [P6] ❌ {e}")

        # P7
        try:
            v7_result["p7"] = run_p7(project)
            print(f"  [P7] ✅")
        except Exception as e:
            v7_result["p7"] = {"error": str(e)}
            errors.append(f"P7: {e}")
            print(f"  [P7] ❌ {e}")

        # P8
        try:
            v7_result["p8"] = run_p8(project)
            print(f"  [P8] ✅")
        except Exception as e:
            v7_result["p8"] = {"error": str(e)}
            errors.append(f"P8: {e}")
            print(f"  [P8] ❌ {e}")

        # P9
        try:
            v7_result["p9"] = run_p9(
                project, v7_result["p6"], v7_result["p7"], v7_result["p8"]
            )
            decision = v7_result["p9"]["gate_result"]["decision"]
            print(f"  [P9] ✅ Gate: {decision}")
        except Exception as e:
            v7_result["p9"] = {"error": str(e)}
            errors.append(f"P9: {e}")
            print(f"  [P9] ❌ {e}")

        # CashFlow + P3
        try:
            cf_result = run_cashflow(project)
            v7_result["cashflow_metrics"] = cf_result.get("metrics", {})
            v7_result["p3"] = run_p3(cf_result)
            npv = v7_result["p3"].get("npv", 0)
            irr = v7_result["p3"].get("irr", 0) * 100
            print(f"  [P3] ✅ VPL: R$ {npv:,.2f} | TIR: {irr:.1f}%")
        except Exception as e:
            v7_result["cashflow_metrics"] = {"error": str(e)}
            v7_result["p3"] = {"error": str(e)}
            errors.append(f"P3/CF: {e}")
            print(f"  [P3] ❌ {e}")

        # Real Options
        try:
            v7_result["real_options_value"] = run_real_options(project)
            print(f"  [RO] ✅ R$ {v7_result['real_options_value']:,.2f}")
        except Exception as e:
            v7_result["real_options_value"] = 0.0
            errors.append(f"RO: {e}")
            print(f"  [RO] ❌ {e}")

        # ──── Golden Evaluation ────
        v7_flat = flatten_financials(v7_result)
        golden_flat = flatten_financials(golden_ref)

        # VPL for Step 2
        v7_vpl = v7_flat.get("npv", 0)
        golden_vpl = golden_flat.get("npv", 0)

        accuracy_score, validation_metrics = evaluator.evaluate(
            ai_extracted=v7_flat,
            golden_reference=golden_flat,
            ai_vpl=float(v7_vpl),
            golden_vpl=float(golden_vpl),
        )

        # ──── Triage ────
        kill_reasons = []
        if errors:
            kill_reasons = [f"Engine error: {e}" for e in errors]

        healing_corrections = 0  # No LLM extraction in backtest mode
        has_blocking_errors = any("P3" in e or "CF" in e for e in errors)

        operation_level = determine_operation_level(
            accuracy_score=accuracy_score,
            kill_reasons=kill_reasons,
            has_blocking_errors=has_blocking_errors,
            normalization_logs=[],  # No LLM extraction in backtest mode
        )

        # VPL MAPE
        vpl_mape_val = (
            validation_metrics.get("step_2_impact", {})
            .get("details", {})
            .get("vpl_mape", None)
        )
        vpl_mape_str = f"{vpl_mape_val*100:.2f}%" if vpl_mape_val is not None else "N/A"

        is_pass = accuracy_score >= 92 and len(kill_reasons) == 0
        if is_pass:
            total_pass += 1
        else:
            total_fail += 1

        status_icon = "✅" if is_pass else "⚠️" if accuracy_score >= 85 else "❌"

        print(f"\n  ═══ GOLDEN EVAL ═══")
        print(f"  Score:     {accuracy_score:.1f}/100 {status_icon}")
        print(f"  VPL MAPE:  {vpl_mape_str}")
        print(f"  Triage:    {operation_level}")
        print(f"  Errors:    {len(errors)}")

        report = {
            "dataset_id": dataset_id,
            "project_name": project_name,
            "accuracy_score": accuracy_score,
            "operation_level": operation_level,
            "vpl_mape": vpl_mape_val,
            "v7_npv": v7_vpl,
            "golden_npv": golden_vpl,
            "v7_irr": v7_flat.get("irr", 0),
            "golden_irr": golden_flat.get("irr", 0),
            "v7_roi": v7_flat.get("roi", 0),
            "golden_roi": golden_flat.get("roi", 0),
            "v7_viable": v7_flat.get("is_viable", False),
            "golden_viable": golden_flat.get("is_viable", False),
            "validation_metrics": validation_metrics,
            "kill_reasons": kill_reasons,
            "engine_errors": errors,
        }
        all_reports.append(report)

    # ──── Final Summary ────
    print(f"\n\n{'='*70}")
    print(f"  ✅ SHADOW BACKTESTING COMPLETO")
    print(f"{'='*70}")

    total = len(all_reports)
    avg_score = (
        sum(r["accuracy_score"] for r in all_reports) / total if total > 0 else 0
    )
    vpl_mapes = [r["vpl_mape"] for r in all_reports if r["vpl_mape"] is not None]
    avg_vpl_mape = sum(vpl_mapes) / len(vpl_mapes) if vpl_mapes else 0
    max_vpl_mape = max(vpl_mapes) if vpl_mapes else 0

    print(f"\n  RESULTADOS AGREGADOS:")
    print(f"  ─────────────────────────────────")
    print(f"  Projetos testados:   {total}")
    print(f"  PASS (≥92):          {total_pass}")
    print(f"  FAIL (<92):          {total_fail}")
    print(f"  Score médio:         {avg_score:.1f}")
    print(f"  VPL MAPE médio:      {avg_vpl_mape*100:.2f}%")
    print(f"  VPL MAPE máximo:     {max_vpl_mape*100:.2f}%")
    print(f"  VPL MAPE ≤ 2%:       {'SIM ✅' if max_vpl_mape <= 0.02 else 'NÃO ❌'}")

    # Table
    print(
        f"\n  {'ID':<13} {'Projeto':<45} {'Score':>7} {'VPL MAPE':>10} {'Triage':<25} {'Status':>6}"
    )
    print(f"  {'─'*110}")

    for r in all_reports:
        name = r["project_name"][:42]
        vpl_m = f"{r['vpl_mape']*100:.2f}%" if r["vpl_mape"] is not None else "N/A"
        status = (
            "✅" if r["accuracy_score"] >= 92 and len(r["kill_reasons"]) == 0 else "❌"
        )
        print(
            f"  {r['dataset_id']:<13} {name:<45} {r['accuracy_score']:>6.1f} {vpl_m:>10} {r['operation_level']:<25} {status:>6}"
        )

    # ──── Save Reports ────
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(
            all_reports, f, indent=2, ensure_ascii=False, default=decimal_serializer
        )

    # Summary text
    summary_lines = [
        f"VERTIV V7 SHADOW BACKTEST — {datetime.now().isoformat()}",
        f"Projetos: {total} | PASS: {total_pass} | FAIL: {total_fail}",
        f"Score médio: {avg_score:.1f} | VPL MAPE médio: {avg_vpl_mape*100:.2f}% | Max: {max_vpl_mape*100:.2f}%",
        "",
        f"{'ID':<13} {'VPL V7':>18} {'VPL Golden':>18} {'MAPE':>8} {'Score':>7} {'Viable V7':>10} {'Viable Gold':>12} {'Triage':<25}",
        "─" * 120,
    ]
    for r in all_reports:
        v_mape = f"{r['vpl_mape']*100:.2f}%" if r["vpl_mape"] is not None else "N/A"
        summary_lines.append(
            f"{r['dataset_id']:<13} "
            f"{r['v7_npv']:>18,.2f} "
            f"{r['golden_npv']:>18,.2f} "
            f"{v_mape:>8} "
            f"{r['accuracy_score']:>6.1f} "
            f"{str(r['v7_viable']):>10} "
            f"{str(r['golden_viable']):>12} "
            f"{r['operation_level']:<25}"
        )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))

    print(f"\n  📄 Report: {report_path}")
    print(f"  📊 Summary: {summary_path}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
