import requests
import time
import sys
import json
import os

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")


def main():
    print(f"🚀 Starting Integration Verification against {API_URL}")

    # 1. Health Check
    try:
        resp = requests.get(f"{API_URL}/health")
        resp.raise_for_status()
        print("✅ Backend Health: OK")
    except Exception as e:
        print(f"❌ Backend not reachable: {e}")
        sys.exit(1)

    # 2. Trigger Simulation
    print("\n📬 Triggering Simulation...")
    payload = {
        "name": "Integration Test Project",
        "description": "Automated verification",
        "financial_input": {
            "total_units": 100,
            "sales_price_avg": 500000,
            "construction_cost_total": 20000000,
            "development_months": 24,
        },
        "real_options": {
            "land_value_current": 5000000,
            "development_cost_forcing": 20000000,
            "time_to_permit_years": 1.5,
            "volatility": 0.2,
            "risk_free_rate": 0.05,
        },
        "esg": {"green_premium": 1000000, "brown_discount": 500000},
    }

    try:
        post_resp = requests.post(f"{API_URL}/calculate/quick", json=payload)
        post_resp.raise_for_status()
        data = post_resp.json()
        sim_id = data.get("simulation_id")
        status = data.get("status")
        print(f"✅ Simulation Triggered: ID={sim_id}, Initial Status={status}")
    except Exception as e:
        print(f"❌ Failed to trigger simulation: {e}")
        # Print response body if available
        # print(post_resp.text)
        sys.exit(1)

    # 3. Poll for Completion
    print(f"\n⏳ Polling for completion (ID: {sim_id})...")
    max_retries = 20
    for i in range(max_retries):
        try:
            poll_resp = requests.get(f"{API_URL}/simulation/{sim_id}")
            poll_resp.raise_for_status()
            poll_data = poll_resp.json()
            current_status = poll_data.get("status")

            print(f"   Attempt {i+1}: Status = {current_status}")

            if current_status == "COMPLETED":
                print("\n🎉 Simulation COMPLETED!")
                print(json.dumps(poll_data.get("result"), indent=2))
                return
            elif current_status == "FAILED":
                print(f"\n❌ Simulation FAILED: {poll_data.get('error')}")
                sys.exit(1)

            time.sleep(2)

        except Exception as e:
            print(f"⚠️ Polling Error: {e}")
            time.sleep(2)

    print("\n⏰ Timeout waiting for simulation completion.")
    sys.exit(1)


if __name__ == "__main__":
    main()
