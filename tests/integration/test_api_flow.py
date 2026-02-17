import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi.testclient import TestClient

# Mock infrastructure components
class MockRepository:
    def create(self, *args, **kwargs):
        pass
    def get(self, *args, **kwargs):
        return {"id": "test-sim-uuid", "status": "PENDING"}

class MockDispatcher:
    @staticmethod
    async def dispatch_simulation(*args, **kwargs):
        return "test-task-name"

# Mock infrastructure BEFORE importing app
with patch("src.infrastructure.repositories.SimulationRepository", return_value=MockRepository()), \
     patch("src.services.task_queue.TaskDispatcher", MockDispatcher), \
     patch("src.infrastructure.database.get_supabase_client"):
    from src.api.main import app

from src.infrastructure.auth import get_current_user, CurrentUser

# mock user
def mock_get_current_user():
    return CurrentUser(id="test-user-uuid", email="test@vertiv.tech", role="authenticated")

# override dependency
app.dependency_overrides[get_current_user] = mock_get_current_user

client = TestClient(app)

def test_api_quick_calculate_dispatch():
    """
    Test that /calculate/quick accepts a valid project and returns a simulation_id.
    """
    payload = {
        "id": "test-proj-001",
        "name": "Test Integration Project",
        "municipality": "Belo Horizonte",
        "financial_input": {
            "total_units": 100,
            "sales_price_avg": 10000.0,
            "construction_cost_total": 5000000.0,
            "land_cost": 1000000.0,
            "development_months": 24,
            "use_ret_taxation": True,
            "funding_model": "SBPE"
        }
    }
    
    response = client.post("/calculate/quick", json=payload)
    
    # We expect 200 or 202
    assert response.status_code == 200
    data = response.json()
    assert "simulation_id" in data
    assert data["status"] == "PENDING"

def test_p1_analyze_secured():
    """
    Test P1 analyze endpoint with mock auth.
    """
    payload = {
        "location_municipality": "Belo Horizonte",
        "location_neighborhood": "Savassi",
        "area_sqm": 1000,
        "asking_price": 5000000
    }
    
    response = client.post("/p1/analyze", json=payload)
    assert response.status_code == 200
    assert "decision" in response.json()
