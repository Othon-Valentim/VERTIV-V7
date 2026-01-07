import asyncio
import os
import sys

# Ensure backend src is in path
sys.path.append(os.path.join(os.getcwd(), "apps", "backend"))

from src.services.search_engine import SearchEngine


async def test_search():
    print(">>> Testing Search Engine (Serper.dev)...")

    # Check if key is available
    if not os.getenv("SERPER_API_KEY"):
        print("SKIP: SERPER_API_KEY environment variable not set.")
        return

    engine = SearchEngine()
    results = await engine.search_market_data("Loteamentos em Nova Lima MG")

    if "error" in results:
        print(f"Search failed: {results['error']}")
        return

    competitors = engine.parse_competitors(results)
    print(f"Found {len(competitors)} potential market items.")
    for c in competitors:
        print(f"- {c['title']}")

    assert len(competitors) > 0, "No results found"
    print("\n[SUCCESS] SEARCH INTEGRATION VERIFIED.")


if __name__ == "__main__":
    asyncio.run(test_search())
