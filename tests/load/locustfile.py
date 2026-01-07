"""
VERTIV v6.1.0-SINGULARITY Load Test Suite
Uses Locust for distributed load testing.

Run with:
    locust -f tests/load/locustfile.py --headless -u 100 -r 10 --run-time 1m
    locust -f tests/load/locustfile.py --host https://api.vertiv.tech
"""

import random
import json
import time
import os
from locust import HttpUser, task, between, events


# Configuration
AUTH_TOKEN = os.getenv("LOAD_TEST_AUTH_TOKEN", "")
MAX_POLL_ATTEMPTS = 10
POLL_INTERVAL = 0.5  # seconds


class SimulateUser(HttpUser):
    """Simulates a user creating and polling simulations."""

    wait_time = between(1, 5)
    host = os.getenv("API_URL", "http://localhost:8000")

    def on_start(self):
        """Called when a simulated user starts."""
        self.auth_headers = {
            "Content-Type": "application/json",
        }
        if AUTH_TOKEN:
            self.auth_headers["Authorization"] = f"Bearer {AUTH_TOKEN}"

    @task(3)
    def create_and_poll_simulation(self):
        """
        Main test task: Create simulation and poll until complete.
        Weight: 3 (most common operation)
        """
        project_id = f"proj_{random.randint(1000, 9999)}"

        payload = {
            "id": project_id,
            "name": f"Load Test Project {project_id}",
            "is_mixed_use": random.choice([True, False]),
            "separate_access_cores": True,
            "fire_load_category": "Residencial",
            "efficiency": 0.85,
            "financial_input": {
                "total_units": random.randint(50, 500),
                "sales_price_avg": random.randint(8000, 15000),
                "construction_cost_total": random.randint(30000000, 100000000),
                "land_cost": random.randint(5000000, 30000000),
                "development_months": random.randint(24, 48),
            },
            "real_options": {
                "land_value_current": random.randint(5000000, 30000000),
                "development_cost_forcing": random.randint(50000000, 150000000),
                "time_to_permit_years": random.uniform(1.0, 3.0),
                "volatility": 0.20,
                "risk_free_rate": 0.1375,
            },
        }

        # Step 1: Create simulation
        with self.client.post(
            "/calculate/quick",
            json=payload,
            headers=self.auth_headers,
            catch_response=True,
            name="/calculate/quick [CREATE]"
        ) as response:
            if response.status_code in [200, 202]:
                try:
                    data = response.json()
                    simulation_id = data.get("simulation_id")
                    response.success()

                    # Step 2: Poll for results
                    if simulation_id:
                        self._poll_simulation(simulation_id)
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            elif response.status_code == 401:
                response.failure("Authentication required - set LOAD_TEST_AUTH_TOKEN")
            elif response.status_code == 429:
                response.failure("Rate limited")
            else:
                response.failure(f"Status {response.status_code}: {response.text[:100]}")

    def _poll_simulation(self, simulation_id: str):
        """Poll simulation status until complete or timeout."""
        for attempt in range(MAX_POLL_ATTEMPTS):
            time.sleep(POLL_INTERVAL)

            with self.client.get(
                f"/simulation/{simulation_id}",
                headers=self.auth_headers,
                catch_response=True,
                name="/simulation/{id} [POLL]"
            ) as response:
                if response.status_code == 200:
                    try:
                        data = response.json()
                        status = data.get("status")

                        if status == "COMPLETED":
                            response.success()
                            return
                        elif status == "FAILED":
                            response.failure(f"Simulation failed: {data.get('error')}")
                            return
                        else:
                            # Still pending/processing
                            response.success()
                    except json.JSONDecodeError:
                        response.failure("Invalid JSON")
                        return
                elif response.status_code == 404:
                    response.failure("Simulation not found")
                    return
                else:
                    response.failure(f"Poll error: {response.status_code}")
                    return

    @task(1)
    def list_simulations(self):
        """
        Test listing simulations.
        Weight: 1 (less common)
        """
        with self.client.get(
            "/simulations?limit=10",
            headers=self.auth_headers,
            catch_response=True,
            name="/simulations [LIST]"
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                response.failure("Auth required")
            else:
                response.failure(f"Status {response.status_code}")

    @task(1)
    def health_check(self):
        """
        Test health endpoint (no auth required).
        Weight: 1
        """
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed: {response.status_code}")


class StressTestUser(HttpUser):
    """
    Aggressive stress test user for maximum throughput testing.
    Use with caution - can trigger rate limits.
    """

    wait_time = between(0.1, 0.5)
    host = os.getenv("API_URL", "http://localhost:8000")

    @task
    def rapid_fire_simulation(self):
        """Send simulations as fast as possible."""
        payload = {
            "id": f"stress_{random.randint(1, 99999)}",
            "name": "Stress Test",
            "financial_input": {
                "total_units": 100,
                "sales_price_avg": 10000,
                "construction_cost_total": 50000000,
                "land_cost": 10000000,
                "development_months": 36,
            },
        }

        self.client.post(
            "/calculate/quick",
            json=payload,
            headers={"Content-Type": "application/json"}
        )


# Event hooks for custom reporting
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("\n" + "="*60)
    print("VERTIV v6.1.0-SINGULARITY Load Test Started")
    print("="*60)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("\n" + "="*60)
    print("Load Test Completed")
    print("="*60)
