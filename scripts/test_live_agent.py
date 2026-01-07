import asyncio
import sys
import os

# Add agents path to verify imports if needed, though we test via server interaction usually.
# Since we are running the server code directly/importing for unit test style:
sys.path.append(os.path.join(os.path.dirname(__file__), "../apps/agents/src"))

from server import find_master_plan, get_neighborhood_price, benchmark_greenium_search


async def test_live_agents():
    print("--- [AUDIT] Phase 2: Live Agent Awakening ---")

    # 1. Scout: Master Plan Search
    print("\n🔍 Testing Scout (The Librarian) - find_master_plan('Sao Paulo')...")
    try:
        # We query for Sao Paulo to see if it finds "Gestão Urbana" or similar Trusted Domain
        scout_result = await find_master_plan("Sao Paulo")
        print(f"Result Len: {len(scout_result)} chars")
        if "MOCK" in scout_result and "Serper Error" not in scout_result:
            print("⚠️ WARNING: Returned MOCK data. Is SERPER_API_KEY set?")
        elif "TRUSTED" in scout_result:
            print("✅ PASS: Trusted Domain Found in Search Results.")
        else:
            print("ℹ️ Note: No 'TRUSTED' tag explicit, but search returned live data.")

        # print(scout_result[:500] + "...")
    except Exception as e:
        print(f"❌ FAIL: Scout crashed: {e}")

    # 2. Benchmark: Price Scan
    print(
        "\n🕵️ Testing Benchmark (The Spy) - get_neighborhood_price('Vila Madalena')..."
    )
    try:
        price_result = await get_neighborhood_price("Vila Madalena")
        print(f"Result: {price_result}")
        if price_result["source"].startswith("Live"):
            print("✅ PASS: Live Price Scanned via Regex.")
            print(f"   Avg Price: R$ {price_result['avg_price_sqm']:.2f}")
        else:
            print(
                "⚠️ WARNING: Returned Mock Price. (Search might have failed to extract regex)"
            )
    except Exception as e:
        print(f"❌ FAIL: Benchmark crashed: {e}")

    # 3. Greenium
    print("\n🌿 Testing Greenium Search...")
    try:
        greenium = await benchmark_greenium_search()
        print(f"Result: {greenium}")
        if greenium["greenium_rate"] > 0:
            print("✅ PASS: Greenium Rate Positive.")
    except Exception as e:
        print(f"❌ FAIL: Greenium crashed: {e}")


if __name__ == "__main__":
    # Check Env
    if not os.getenv("SERPER_API_KEY"):
        print("⚠️ SERPER_API_KEY not found in env. Expecting FALLBACK behaviors.")

    asyncio.run(test_live_agents())
