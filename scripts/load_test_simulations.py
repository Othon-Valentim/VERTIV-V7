from locust import HttpUser, task, between
import uuid
import random

class VertivLoadTest(HttpUser):
    wait_time = between(1, 2)

    @task
    def process_simulation(self):
        sim_id = f"locust-{uuid.uuid4()}"
        payload = {
            "simulation_id": sim_id,
            "project": {
                "id": sim_id,
                "name": f"Stress Test Project {sim_id[:8]}",
                "municipality": random.choice(["Belo Horizonte", "Nova Lima", "Sao Paulo"]),
                "is_mixed_use": random.choice([True, False]),
                "esg": {"green_premium": 0.003},
                "financial_input": {
                    "total_units": random.randint(50, 500),
                    "sales_price_avg": random.randint(5000, 15000),
                    "construction_cost_total": random.randint(10000000, 100000000),
                    "land_cost": random.randint(5000000, 30000000),
                    "development_months": random.randint(24, 60)
                }
            }
        }
        self.client.post("/tasks/process-simulation", json=payload)
