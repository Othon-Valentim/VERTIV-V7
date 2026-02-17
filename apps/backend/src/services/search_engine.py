import httpx
import os
import hashlib
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class CacheEntry:
    """Entrada de cache com TTL."""
    data: Dict[str, Any]
    created_at: float
    ttl_seconds: float = 604800  # 7 dias padrão

    def is_expired(self) -> bool:
        return time.time() > (self.created_at + self.ttl_seconds)


@dataclass
class CacheStats:
    """Estatísticas do cache para observabilidade."""
    hits: int = 0
    misses: int = 0
    api_calls_saved: int = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0


class SearchEngineCache:
    """
    Cache in-memory para resultados de busca Serper.

    Estratégia: Cache agressivo de 7 dias para dados de mercado imobiliário,
    que não mudam drasticamente em curtos períodos.

    TODO: Migrar para Redis em produção para persistência e escalabilidade.
    """

    def __init__(self, default_ttl_seconds: float = 604800):  # 7 dias
        self._cache: Dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl_seconds
        self.stats = CacheStats()

    def _generate_key(self, query: str, location: str) -> str:
        """Gera hash MD5 da query para usar como chave."""
        raw_key = f"{query.lower().strip()}|{location.lower().strip()}"
        return hashlib.md5(raw_key.encode()).hexdigest()

    def get(self, query: str, location: str) -> Optional[Dict[str, Any]]:
        """Busca no cache. Retorna None se não existir ou expirado."""
        key = self._generate_key(query, location)
        entry = self._cache.get(key)

        if entry is None:
            self.stats.misses += 1
            return None

        if entry.is_expired():
            del self._cache[key]
            self.stats.misses += 1
            return None

        self.stats.hits += 1
        self.stats.api_calls_saved += 1
        return entry.data

    def set(self, query: str, location: str, data: Dict[str, Any], ttl_seconds: Optional[float] = None):
        """Salva resultado no cache."""
        key = self._generate_key(query, location)
        self._cache[key] = CacheEntry(
            data=data,
            created_at=time.time(),
            ttl_seconds=ttl_seconds or self._default_ttl
        )

    def clear_expired(self):
        """Remove entradas expiradas (chamar periodicamente)."""
        expired_keys = [k for k, v in self._cache.items() if v.is_expired()]
        for key in expired_keys:
            del self._cache[key]
        return len(expired_keys)

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache."""
        return {
            "hits": self.stats.hits,
            "misses": self.stats.misses,
            "hit_rate": f"{self.stats.hit_rate:.1f}%",
            "api_calls_saved": self.stats.api_calls_saved,
            "cached_entries": len(self._cache)
        }


# Instância global do cache (compartilhada entre requests)
_search_cache = SearchEngineCache()


class SearchEngine:
    """
    Real-time Market Search Engine powered by Serper.dev.
    Extracts competitor data, pricing, and market trends.

    Features:
    - Cache agressivo de 7 dias para economia de API calls
    - Estatísticas de hit/miss para observabilidade
    - Fallback gracioso em caso de erro
    """

    def __init__(self, cache: Optional[SearchEngineCache] = None):
        self.api_key = os.getenv("SERPER_API_KEY", "")
        self.url = "https://google.serper.dev/search"
        self.headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        self.cache = cache or _search_cache

    async def search_market_data(
        self, query: str, location: str = "Brazil", bypass_cache: bool = False
    ) -> Dict[str, Any]:
        """
        Performs a Google search via Serper.dev to find market information.

        Args:
            query: Termo de busca
            location: Localização para contextualizar a busca
            bypass_cache: Se True, ignora cache e força nova busca

        Returns:
            Resultados da busca (do cache ou da API)
        """
        if not self.api_key:
            print("WARNING: SERPER_API_KEY not configured. Search will fail.")
            return {"error": "API Key missing"}

        # 1. Verificar cache primeiro (a menos que bypass_cache=True)
        if not bypass_cache:
            cached_result = self.cache.get(query, location)
            if cached_result:
                print(f"[CACHE HIT] Query: {query[:50]}... | Saved 1 API call")
                return {**cached_result, "_from_cache": True}

        # 2. Cache miss - fazer chamada à API
        print(f"[CACHE MISS] Query: {query[:50]}... | Calling Serper API")
        composed_query = f"{query} em {location}"
        payload = {"q": composed_query, "gl": "br", "hl": "pt-br"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.url, headers=self.headers, json=payload, timeout=10.0
                )
                response.raise_for_status()
                result = response.json()

                # 3. Salvar no cache para próximas chamadas
                self.cache.set(query, location, result)
                print(f"[CACHE SET] Query cached for 7 days")

                return {**result, "_from_cache": False}
            except Exception as e:
                print(f"Error executing search: {e}")
                return {"error": str(e)}

    def get_cache_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache para monitoramento."""
        return self.cache.get_stats()

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
