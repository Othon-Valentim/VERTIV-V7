import requests
import time
import json
import traceback

# Configuration
BACKEND_URL = "http://localhost:8000"
AUTH_TOKEN = "" # Set this via environment or paste here for testing


def verify_golden_path():
    print("--- GOLDEN PATH VALIDATION ---")
    
    headers = {}
    if AUTH_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
    else:
        print("WARNING: No AUTH_TOKEN provided. Tests may fail on secured routes.")

    # 1. Health
    print("1. Checking Health...")
    try:
        resp = requests.get(f"{BACKEND_URL}/health")
        if resp.status_code == 200:
            print("Health OK")
        else:
            print(f"Health FAIL: {resp.status_code}")
            return
    except Exception as e:
        print(f"Health Connection FAIL: {e}")
        return

    # 2. Simulation
    print("2. Submitting Simulation (Leopoldina Mixed-Use)...")

    # Correct Payload: Must be ProjectTIV (flat), not SimulationRequest (nested)
    payload = {
        "id": "proj-golden-001",
        "name": "Leopoldina Complex",
        "type": "mixed_use",
        "financial_input": {
            "development_months": 36,
            "total_units": 200,
            "sales_price_avg": 12500.0,
            "construction_cost_total": 45000000.0,
            "land_cost": 15000000.0,  # Added mandatory field
        },
        "real_options": {
            "land_value_current": 15000000.0,
            "development_cost_forcing": 45000000.0,
            "time_to_permit_years": 1.5,
            "volatility": 0.20,
            "risk_free_rate": 0.11,
        },
        "esg": {"green_premium": 2500000.0, "brown_discount": 500000.0},
    }

    try:
        start_t = time.time()
        # Backend /calculate/quick takes ProjectTIV
        resp = requests.post(f"{BACKEND_URL}/calculate/quick", json=payload, headers=headers, timeout=30)
        dur = time.time() - start_t

        if resp.status_code == 200:
            data = resp.json()
            # The backend returns { status: PENDING, simulation_id: ... }
            # Wait! The backend returns PENDING immediately.
            # We need to POLL or check logs for actual calculation success if we want to confirm 200 OK from Worker.
            # But here we just want to ensure Backend accepted it and didn't crash.
            # AND ideally we want to see if Worker processed it.

            print(f"Submission Valid ({dur:.2f}s)")
            print(f"Response: {data}")

            sim_id = data.get("simulation_id")
            if sim_id:
                print(
                    "GOLDEN PATH PASSED (Submission). Check Worker Logs for Calc Results."
                )
            else:
                print("GOLDEN PATH WARN: No Simulation ID returned.")

        else:
            print(f"Status Unexpected: {resp.json().get('status', 'Unknown')}")
            print(resp.json())

    except Exception as e:
        print(f"Connection FAIL: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    verify_golden_path()
