from src.engine.regulatory import RegulatoryEngine
from src.domain.schemas import ProjectTIV


def test_it11_compliance():
    print(">>> Testing IT-11 Compliance Logic...")

    # 1. Test Penalty Application
    base_eff = 0.82
    adjusted_eff = RegulatoryEngine.apply_it11_efficiency_penalty("MISTO", base_eff)
    expected_eff = base_eff * 0.85

    print(f"Base Efficiency: {base_eff}")
    print(f"Adjusted Efficiency (MISTO): {adjusted_eff}")

    assert (
        abs(adjusted_eff - expected_eff) < 1e-9
    ), f"Penalty logic failed! Expected {expected_eff}, got {adjusted_eff}"

    # 2. Test Core Access Validation
    # Case: Mixed Use without separate cores
    p1 = ProjectTIV(
        id="sim-001",
        name="Test 1",
        is_mixed_use=True,
        separate_access_cores=False,
        efficiency=0.8,
    )

    compliant, reasons = RegulatoryEngine.check_it11_compliance(p1)
    print(f"Compliance (Mixed & No Separate Cores): {compliant}")
    assert compliant is False, "Should be non-compliant"
    assert "FATAL" in reasons[0], "Should have a fatal reason"

    # Case: Mixed Use with separate cores
    p2 = ProjectTIV(
        id="sim-002",
        name="Test 2",
        is_mixed_use=True,
        separate_access_cores=True,
        efficiency=0.8,
    )
    compliant, reasons = RegulatoryEngine.check_it11_compliance(p2)
    print(f"Compliance (Mixed & Separate Cores): {compliant}")
    assert compliant is True, "Should be compliant"

    print("\n[SUCCESS] IT-11 COMPLIANCE VERIFIED.")


if __name__ == "__main__":
    try:
        test_it11_compliance()
    except Exception as e:
        print(f"\n[FAILURE] IT-11 Compliance test failed: {e}")
        exit(1)
