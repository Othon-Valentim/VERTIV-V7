import pytest
from decimal import Decimal
from src.engine.cashflow import CashFlowEngine
from src.domain.schemas import ProjectTIV, FinancialAssumptions

# Mock Data
@pytest.fixture
def basic_project():
    return ProjectTIV(
        name="Test Project",
        land_area=1000,
        construction_area=2000,
        assumptions=FinancialAssumptions(
            sale_price_per_sqm=10000,
            construction_cost_per_sqm=5000,
            land_cost=2000000,
            discount_rate=0.10
        )
    )

def test_cashflow_generation(basic_project):
    """
    Test that cashflow engine generates the correct number of periods
    and positive NPV for a profitable project.
    """
    engine = CashFlowEngine(basic_project)
    result = engine.calculate_npv()
    
    # Check Structure
    assert "npv" in result
    assert "irr" in result
    assert "cash_flow" in result
    
    # Check Values
    assert result["npv"] > 0
    assert len(result["cash_flow"]) == 25 # 0..24 months

def test_negative_project():
    """
    Test that a highly expensive project produces negative NPV.
    """
    bad_project = ProjectTIV(
        name="Bad Project",
        land_area=1000,
        construction_area=2000,
        assumptions=FinancialAssumptions(
            sale_price_per_sqm=1000, # Very low
            construction_cost_per_sqm=5000,
            land_cost=2000000,
            discount_rate=0.10
        )
    )
    engine = CashFlowEngine(bad_project)
    result = engine.calculate_npv()
    
    assert result["npv"] < 0
