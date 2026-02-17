import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Mock Supabase BEFORE importing app to avoid initialization errors
with patch("supabase.create_client"):
    from apps.worker.core.main import app

client = TestClient(app)

def test_worker_process_simulation_logic():
    """
    Test that the worker correctly processes a simulation payload.
    It should perform calculations and return a COMPLETED status.
    """
    payload = {
        "simulation_id": "test-sim-001",
        "project": {
            "id": "proj-001",
            "name": "Worker Test Project",
            "municipality": "Sao Paulo",
            "financial_input": {
                "total_units": 50,
                "sales_price_avg": 12000.0,
                "construction_cost_total": 3000000.0,
                "land_cost": 1500000.0,
                "development_months": 36,
                "use_ret_taxation": True,
                "funding_model": "SBPE"
            }
        }
    }
    
    # Ensure supabase_client is mocked or None during the call
    with patch("apps.worker.core.main.supabase_client") as mock_supabase:
        response = client.post("/tasks/process-simulation", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "COMPLETED"
        assert "result" in data
        assert "npv" in data["result"]
        # Verify that NPV is numeric (can be float or string-decimal)
        npv_val = data["result"]["npv"]
        assert isinstance(npv_val, (float, int, str))
        if isinstance(npv_val, str):
            float(npv_val) # Should not raise
