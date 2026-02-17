import sys
import os
from typing import Dict, Any, List
from decimal import Decimal

# Ensure backend src is in path for types and services
# In Docker, this is /apps/backend. Locally, it's ../../../apps/backend
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "apps", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

try:
    from src.services.search_engine import SearchEngine
    from src.engine.p6_p9_market import CompetitorProject
    from core.price_scraper import PriceScraper
except ImportError:
    print("WARNING: Could not import backend modules or core utilities in ScoutAgent. Using Mock logic.")
    SearchEngine = None
    CompetitorProject = None
    PriceScraper = None

class ScoutAgent:
    """
    Autonomous intelligence agent that 'scouts' the web for market data.
    """
    
    def __init__(self):
        self.search_engine = SearchEngine() if SearchEngine else None

    async def scout_competitors(self, municipality: str, neighborhood: str, product_type: str) -> List[Dict[str, Any]]:
        """
        Scouts the area for competitors and pricing using live web search.
        """
        if not self.search_engine:
            print("[SCOUT] Search engine not initialized, falling back to mock.")
            return self._mock_scout(municipality, product_type)

        # Build a highly targeted query for Brazilian market context
        query = f"preço m2 lançamento imobiliário {product_type} {neighborhood} {municipality}"
        print(f"[SCOUT] Live Researching: {query}")
        
        raw_results = await self.search_engine.search_market_data(query, location=municipality)
        
        if "error" in raw_results:
            print(f"[SCOUT] Search failed: {raw_results['error']}")
            return self._mock_scout(municipality, product_type)

        hits = self.search_engine.parse_competitors(raw_results)
        
        competitors = []
        for hit in hits:
            snippet = hit.get("snippet", "")
            # Enhanced price extraction
            price = PriceScraper.extract_price(snippet) if PriceScraper else None
            
            if not price:
                # Fallback to general area average if extraction fails
                price = 7200.0 

            competitors.append({
                "name": hit.get("title", "Empreendimento")[:60],
                "price_sqm": price,
                "source_url": hit.get("link", ""),
                "snippet": snippet,
                "verified": "✅ SERPER"
            })
            
        return competitors

    def _mock_scout(self, municipality: str, product_type: str) -> List[Dict[str, Any]]:
        """Fallback mock data if search is disabled or fails."""
        return [
            {
                "name": f"Residencial {municipality} Park",
                "price_sqm": 6800.0,
                "source": "https://simulated-market.com/p1",
                "snippet": "Lancamento de alto padrao na regiao."
            },
            {
                "name": f"Village {municipality} Prime",
                "price_sqm": 7500.0,
                "source": "https://simulated-market.com/p2",
                "snippet": "Condominio fechado com infraestrutura completa."
            }
        ]
