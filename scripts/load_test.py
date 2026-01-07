import asyncio
import httpx
import time
import random
import os
from typing import List

# Configuration
BASE_URL = os.getenv("API_URL", "http://localhost:8000")
ENDPOINT = f"{BASE_URL}/calculate/quick"
TOTAL_REQUESTS = int(
    os.getenv("TOTAL_REQUESTS", "1000")
)  # Default 1k for local safety, scale to 10k via ENV
CONCURRENCY = 50

# Mock Data Generators
PRODUCT_TYPES = [
    "LOTEAMENTO_ABERTO",
    "CONDOMINIO_FECHADO",
    "VERTICAL_RESIDENCIAL",
    "VERTICAL_COMERCIAL",
    "MISTO",
]


def generate_payload(i: int) -> dict:
    typology = random.choice(PRODUCT_TYPES)
    # Mixed use has ~20% chance
    is_mixed = typology == "MISTO"

    return {
        "simulation_id": f"load_test_{int(time.time())}_{i}",
        "project": {
            "id": f"proj_{i}",
            "name": f"Project Delta {i}",
            "is_mixed_use": is_mixed,
            "separate_access_cores": True,  # Compliant by default
            "fire_load_category": "Residencial",
            "financial_input": {
                "total_units": random.randint(50, 500),
                "sales_price_avg": random.uniform(5000, 15000),
                "construction_cost_total": random.uniform(10_000_000, 100_000_000),
                "land_cost": random.uniform(2_000_000, 20_000_000),
                "development_months": random.randint(24, 48),
            },
            "real_options": {
                "land_value_current": random.uniform(2_000_000, 5_000_000),
                "development_cost_forcing": random.uniform(15_000_000, 30_000_000),
                "time_to_permit_years": random.uniform(1, 3),
                "volatility": 0.20,
                "risk_free_rate": 0.11,
            },
        },
    }


async def send_request(client: httpx.AsyncClient, payload: dict, stats: dict):
    start = time.perf_counter()
    try:
        response = await client.post(ENDPOINT, json=payload)
        duration = time.perf_counter() - start

        stats["latencies"].append(duration)
        if response.status_code in [200, 202]:
            stats["success"] += 1
        else:
            stats["fail"] += 1
            # print(f"Fail: {response.text}")
    except Exception as e:
        stats["errors"] += 1
        # print(f"Error: {e}")


async def load_test():
    print(f"🚀 Iniciando Teste de Carga: {TOTAL_REQUESTS} requests")
    print(f"🎯 Target: {ENDPOINT}")
    print(f"⚡ Concurrency: {CONCURRENCY}")

    stats = {"success": 0, "fail": 0, "errors": 0, "latencies": []}

    start_time = time.perf_counter()

    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = []
        for i in range(TOTAL_REQUESTS):
            if len(tasks) >= CONCURRENCY:
                # Wait for some to finish to maintain concurrency window
                done, pending = await asyncio.wait(
                    tasks, return_when=asyncio.FIRST_COMPLETED
                )
                tasks = list(pending)

            payload = generate_payload(i)
            tasks.append(asyncio.create_task(send_request(client, payload, stats)))

        if tasks:
            await asyncio.wait(tasks)

    total_time = time.perf_counter() - start_time

    # Results
    avg_latency = (
        sum(stats["latencies"]) / len(stats["latencies"]) if stats["latencies"] else 0
    )
    rps = stats["success"] / total_time

    print("\n--- 📊 Relatório de Carga ---")
    print(f"Total Tempo: {total_time:.2f}s")
    print(f"Total Requests: {TOTAL_REQUESTS}")
    print(f"✅ Sucesso: {stats['success']}")
    print(f"❌ Falhas: {stats['fail']}")
    print(f"⚠️ Erros de Rede: {stats['errors']}")
    print(f"⏱️ Latência Média: {avg_latency*1000:.2f}ms")
    print(f"🔥 Throughput: {rps:.2f} req/s")


if __name__ == "__main__":
    asyncio.run(load_test())
