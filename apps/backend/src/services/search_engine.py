import httpx
import os
from typing import List, Dict, Any, Optional


class SearchEngine:
    """
    Real-time Market Search Engine powered by Serper.dev.
    Extracts competitor data, pricing, and market trends.
    """

    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY", "")
        self.url = "https://google.serper.dev/search"
        self.headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}

    async def search_market_data(
        self, query: str, location: str = "Brazil"
    ) -> Dict[str, Any]:
        """
        Performs a Google search via Serper.dev to find market information.
        """
        if not self.api_key:
            print("WARNING: SERPER_API_KEY not configured. Search will fail.")
            return {"error": "API Key missing"}

        composed_query = f"{query} em {location}"
        payload = {"q": composed_query, "gl": "br", "hl": "pt-br"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.url, headers=self.headers, json=payload, timeout=10.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error executing search: {e}")
                return {"error": str(e)}

    def parse_competitors(self, search_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Simplistic parser to extract potential competitor names from organic results.
        Refined in future steps.
        """
        competitors = []
        if "organic" in search_results:
            for item in search_results["organic"][:5]:
                competitors.append(
                    {
                        "title": item.get("title"),
                        "link": item.get("link"),
                        "snippet": item.get("snippet"),
                    }
                )
        return competitors
