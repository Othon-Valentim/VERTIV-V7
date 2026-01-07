from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class MarketDataService(ABC):
    """
    Abstract Interface for fetching Market Data.
    Implementations:
    - BigQueryService (Production)
    - LocalStubService (Dev/Test)
    """

    @abstractmethod
    def get_selic_rate(self) -> float:
        pass

    @abstractmethod
    def get_ipca_rate(self) -> float:
        pass

    @abstractmethod
    def get_construction_index(self, state: str) -> float:
        pass


class LocalStubService(MarketDataService):
    def get_selic_rate(self) -> float:
        return 0.1125  # 11.25%

    def get_ipca_rate(self) -> float:
        return 0.045  # 4.5%

    def get_construction_index(self, state: str) -> float:
        return 1.05  # +5% INCC


class BigQueryService(MarketDataService):
    def __init__(self, project_id: str):
        self.project_id = project_id
        # self.client = bigquery.Client(project=project_id)

    def get_selic_rate(self) -> float:
        # TODO: Implement actual BigQuery Logic
        return 0.1125

    def get_ipca_rate(self) -> float:
        # TODO: Implement actual BigQuery Logic
        return 0.045

    def get_construction_index(self, state: str) -> float:
        # TODO: Implement actual BigQuery Logic
        return 1.05


# Singleton Factory
_market_data_cache: Dict[str, Any] = {}
_cache_ttl_seconds = 3600  # 1 Hour


def get_market_service() -> MarketDataService:
    # Logic to switch based on ENV or Feature Flag
    import os

    # Audit Requirement: Use Live Data.
    # We prefer BCBConnector which has built-in fallbacks.
    return BCBConnector()


import httpx
from datetime import datetime
import time


class BCBConnector(MarketDataService):
    """
    Connects to Banco Central do Brasil (SGS API).
    Includes fallbacks to fixed values if API fails to ensure stability.
    """

    def _get_cached(self, key: str) -> Optional[float]:
        if key in _market_data_cache:
            entry = _market_data_cache[key]
            if (time.time() - entry["timestamp"]) < _cache_ttl_seconds:
                return entry["value"]
        return None

    def _set_cache(self, key: str, value: float):
        _market_data_cache[key] = {"value": value, "timestamp": time.time()}

    def get_selic_rate(self) -> float:
        # Check Cache
        cached = self._get_cached("selic")
        if cached is not None:
            return cached

        # Code 432: Meta Selic (% p.a.)
        try:
            url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
            response = httpx.get(url, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            # Format: [{'data': '13/12/2025', 'valor': '11.25'}]
            val = float(data[0]["valor"])
            rate = val / 100.0
            self._set_cache("selic", rate)
            return rate
        except Exception as e:
            print(f"⚠️ Failed to fetch Selic from BCB: {e}. Fallback to 11.25%")
            return 0.1125

    def get_ipca_rate(self) -> float:
        # Check Cache
        cached = self._get_cached("ipca")
        if cached is not None:
            return cached

        # Code 13522: IPCA Acumulado 12 meses (% p.a.)
        try:
            url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.13522/dados/ultimos/1?formato=json"
            response = httpx.get(url, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            val = float(data[0]["valor"])
            rate = val / 100.0
            self._set_cache("ipca", rate)
            return rate
        except Exception as e:
            print(f"⚠️ Failed to fetch IPCA from BCB: {e}. Fallback to 4.5%")
            return 0.045

    def get_construction_index(self, state: str) -> float:
        # INCC-M (FGV) is strict. Using 5% p.a. placeholder for now as specific public API is limited.
        return 1.05


class AnbimaEstimator:
    """
    Estimates Greenium based on market proxies.
    Attempting to scrape public indicators or use spread logic.
    """

    @staticmethod
    def get_greenium_spread() -> float:
        # Real implementation would scrape https://www.anbima.com.br/pt_br/informar/taxas-de-titulos-publicos.htm
        # For now, we simulate the logic of "Looking at the spread"

        # Simulated Live Data Logic
        # If we could fetch NTN-B vs Green Debentures, we would return the delta.
        # Returning conservative 30bps (0.3%) discount.
        return 0.003
