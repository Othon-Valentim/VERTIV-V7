import asyncio
import httpx
import time
import random
import os

# Configuration
BASE_URL = os.getenv("API_URL", "http://localhost:8000")
ENDPOINT = f"{BASE_URL}/calculate/quick"
TOTAL_REQUESTS = 10000
CONCURRENCY = 100


async def send_request(client: httpx.AsyncClient, i: int, stats: dict):
    payload = {
        "id": f"proj_flood_{i}",
        "name": f"Flood Project {i}",
        "is_mixed_use": random.choice([True, False]),
        "financial_input": {
            "total_units": 100,
            "sales_price_avg": 10000,
            "construction_cost_total": 50000000,
            "land_cost": 10000000,
            "development_months": 36,
        },
    }

    try:
        await client.post(ENDPOINT, json=payload, timeout=10.0)
        stats["sent"] += 1
    except Exception:
        stats["error"] += 1


async def flood():
    print(f"🌊 STARTING FLOOD: {TOTAL_REQUESTS} requests -> {ENDPOINT}")
    stats = {"sent": 0, "error": 0}
    start = time.perf_counter()

    async with httpx.AsyncClient(
        limits=httpx.Limits(
            max_keepalive_connections=CONCURRENCY, max_connections=CONCURRENCY
        )
    ) as client:
        tasks = []
        for i in range(TOTAL_REQUESTS):
            if len(tasks) >= CONCURRENCY:
                done, pending = await asyncio.wait(
                    tasks, return_when=asyncio.FIRST_COMPLETED
                )
                tasks = list(pending)

            tasks.append(asyncio.create_task(send_request(client, i, stats)))

        if tasks:
            await asyncio.wait(tasks)

    duration = time.perf_counter() - start
    print(f"🏁 FLOOD FINISHED in {duration:.2f}s")
    print(f"throughput: {TOTAL_REQUESTS/duration:.0f} req/s")
    print(f"Stats: {stats}")


if __name__ == "__main__":
    asyncio.run(flood())
