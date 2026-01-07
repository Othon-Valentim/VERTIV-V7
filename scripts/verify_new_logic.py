import sys
from pathlib import Path
from decimal import Decimal

# Add project root and backend to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "apps" / "backend"))
sys.path.insert(0, str(PROJECT_ROOT))

# Mock domain schemas if necessary or import them
from apps.backend.src.engine.p1_screener import P1ScreenerEngine
from apps.backend.src.engine.cashflow import CashFlowEngine
from apps.backend.src.domain.schemas import P1GarimpoInput, MarketCyclePhase


def test_p1_polars_logic():
    print("\n--- [TEST] P1 Polars & Cycle Scoring ---")
    engine = P1ScreenerEngine()

    # Test Case A: Recovery (Large area, low price)
    input_a = P1GarimpoInput(
        location_municipality="Leopoldina",
        location_neighborhood="Centro",
        area_sqm=12000,
        asking_price=Decimal("3600000"),  # 300/sqm (Cheap, Benchmark is 600)
    )
    result_a = engine.analyze(input_a)
    print(
        f"Case A (Recovery/Cheap): Score={result_a.score_attractiveness}, Phase={result_a.cycle_phase}, Decision={result_a.decision}"
    )

    assert result_a.cycle_phase == MarketCyclePhase.RECOVERY
    # Cycle(25) + Ratio(2.0)*50 = 125, capped at 100
    assert result_a.score_attractiveness == 100.0

    # Test Case B: Recession (Small area, high price)
    input_b = P1GarimpoInput(
        location_municipality="Leopoldina",
        location_neighborhood="Periferia",
        area_sqm=500,
        asking_price=Decimal("600000"),  # 1200/sqm (Expensive, Benchmark is 600)
    )
    result_b = engine.analyze(input_b)
    print(
        f"Case B (Recession/Expensive): Score={result_b.score_attractiveness}, Phase={result_b.cycle_phase}, Decision={result_b.decision}"
    )

    assert result_b.cycle_phase == MarketCyclePhase.RECESSION
    # Cycle(5) + Ratio(0.5)*50 = 30.0
    assert result_b.score_attractiveness == 30.0
    print("✅ P1 Polars & Cycle Logic: PASS")


def test_esg_wacc_npv_logic():
    print("\n--- [TEST] RICS ESG WACC NPV Adjustment ---")
    engine = CashFlowEngine(months=12)

    # Base params
    units = 100
    price = 5000.0
    cost = 200000.0

    # Case 1: Base WACC (14.5%)
    res_base = engine.calculate_project_cashflow(units, price, cost, wacc_annual=0.145)
    npv_base = res_base["metrics"]["npv"]

    # Case 2: Green WACC (14.0% - Greenium of 0.5%)
    res_green = engine.calculate_project_cashflow(units, price, cost, wacc_annual=0.140)
    npv_green = res_green["metrics"]["npv"]

    print(f"Base NPV (14.5%): {npv_base:,.2f}")
    print(f"Green NPV (14.0%): {npv_green:,.2f}")

    assert npv_green > npv_base
    diff = npv_green - npv_base
    print(
        f"✅ ESG Integration: PASS (NPV increased by {diff:,.2f} due to Greenium WACC)"
    )


if __name__ == "__main__":
    try:
        test_p1_polars_logic()
        test_esg_wacc_npv_logic()
        print("\n🚀 ALL NEW LOGIC TESTS PASSED")
    except Exception as e:
        import traceback

        traceback.print_exc()
        sys.exit(1)
