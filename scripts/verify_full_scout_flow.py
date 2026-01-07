import asyncio
import os
import sys
from decimal import Decimal

# Ensure backend and worker core are in path
sys.path.append(os.path.join(os.getcwd(), "apps", "backend"))
sys.path.append(os.path.join(os.getcwd(), "apps", "worker"))

from src.domain.schemas import ProjectTIV, P10FinancialInput, SimulationRequest, ESGAttributes
from core.scout_agent import ScoutAgent

async def test_full_scout_flow():
    print(">>> Testing Full Scout Flow within Worker logic...")
    
    # 1. Setup Mock Project (Mixed Use)
    project = ProjectTIV(
        id="test-sim-999",
        name="Singularity Tower",
        municipality="Nova Lima",
        is_mixed_use=True,
        esg=ESGAttributes(green_premium=0.005), # 50bps greenium
        financial_input=P10FinancialInput(
            total_units=200,
            sales_price_avg=Decimal("0.0"), # Triggers ScoutAgent
            construction_cost_total=Decimal("50000000.0"),
            land_cost=Decimal("15000000.0"),
            development_months=36
        )
    )
    
    request = SimulationRequest(
        simulation_id="test-999",
        project=project
    )
    
    # 2. Initialize ScoutAgent
    agent = ScoutAgent()
    
    # 3. Simulate Worker's Scouting Phase
    print(f"Project: {project.name} | Mixed Use: {project.is_mixed_use} | Price: {project.financial_input.sales_price_avg}")
    
    if project.is_mixed_use or float(project.financial_input.sales_price_avg) == 0:
        print("[TEST] Correctly identified need to scout.")
        competitors = await agent.scout_competitors(
            municipality=project.municipality,
            neighborhood="Vila da Serra",
            product_type="MISTO"
        )
        
        print(f"[TEST] Scout returned {len(competitors)} results.")
        assert len(competitors) > 0, "Scout should return at least mock results"
        
        for c in competitors:
            print(f"  - Found: {c['name']} | Price: {c['price_sqm']}")

    print("\n[SUCCESS] SCOUT FLOW VERIFIED.")

if __name__ == "__main__":
    asyncio.run(test_full_scout_flow())
