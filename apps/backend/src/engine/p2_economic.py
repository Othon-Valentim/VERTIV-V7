"""
P2: Dinâmica Econômica - Economic Dynamics Engine
VERTIV v6.0 Global Edition

Framework: P2i-Lead Index (0-50 points)
Integrates live BCB data for macroeconomic analysis.

Reference: KB_CORE v6.0 Section 2.4
"""

from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
import httpx
from datetime import datetime, timedelta
from src.vertiv.biz import tropicalize


@dataclass
class EconomicIndicators:
    """Live economic indicators from BCB and other sources."""

    selic_rate: float  # Taxa SELIC anual
    ipca_12m: float  # IPCA acumulado 12 meses
    pib_growth: float  # Crescimento PIB
    unemployment_rate: float  # Taxa de desemprego
    consumer_confidence: float  # Índice de confiança do consumidor (0-200)
    credit_expansion: float  # Expansão do crédito imobiliário YoY
    formal_employment_growth: float  # CAGED - variação emprego formal


class P2EconomicEngine:
    """
    P2 Economic Dynamics Analysis Engine.

    Calculates P2i-Lead score (0-50 points) based on:
    - Leading indicators (25 pts): Employment, Credit, Confidence
    - Lagging indicators (15 pts): IPCA, PIB, Selic
    - Contextual factors (10 pts): Regional adjustments

    Gate: P2i-Lead >= 28 for GO
    """

    # BCB SGS Series Codes
    BCB_SELIC = 432  # Taxa SELIC
    BCB_IPCA = 433  # IPCA mensal
    BCB_DESEMPREGO = 24369  # Taxa de desocupação

    def __init__(self):
        self._cache = {}
        self._cache_expiry = datetime.now()

    async def fetch_bcb_indicator(
        self, series_code: int, periods: int = 12
    ) -> Optional[float]:
        """Fetch indicator from BCB SGS API with caching."""
        cache_key = f"bcb_{series_code}"

        if cache_key in self._cache and datetime.now() < self._cache_expiry:
            return self._cache[cache_key]

        try:
            url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_code}/dados/ultimos/{periods}?formato=json"
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        # Return the latest value
                        latest = float(data[-1]["valor"])
                        self._cache[cache_key] = latest
                        self._cache_expiry = datetime.now() + timedelta(hours=1)
                        return latest
        except Exception as e:
            print(f"BCB API Error for series {series_code}: {e}")

        return None

    async def get_live_indicators(self) -> EconomicIndicators:
        """Fetch all live economic indicators."""
        # Fetch from BCB (with fallbacks)
        selic = await self.fetch_bcb_indicator(self.BCB_SELIC) or tropicalize(
            "SELIC_RATE", 11.25
        )
        # IPCA in p2 is percent (e.g. 4.5), but biz module stores decimal (0.045). Converting:
        ipca = await self.fetch_bcb_indicator(self.BCB_IPCA) or (
            tropicalize("IPCA_ANNUAL", 0.045) * 100
        )
        unemployment = await self.fetch_bcb_indicator(
            self.BCB_DESEMPREGO
        ) or tropicalize("UNEMPLOYMENT_RATE", 7.5)

        # Simulated indicators (would come from other APIs in production)
        # These should integrate with IBGE, CAGED, FGV in production
        return EconomicIndicators(
            selic_rate=selic,
            ipca_12m=ipca,
            pib_growth=2.5,  # Would fetch from IBGE
            unemployment_rate=unemployment,
            consumer_confidence=98.5,  # Would fetch from FGV ICC
            credit_expansion=12.0,  # Would fetch from BCB
            formal_employment_growth=1.8,  # Would fetch from CAGED
        )

    def get_offline_indicators(self) -> EconomicIndicators:
        """Return hardcoded fallback indicators for offline/sync execution.

        Values calibrated to Brazil Q4 2024 / Q1 2025:
        - Selic: 13.25% (BCB Jan/2025)
        - IPCA 12m: 4.77% (IBGE Jan/2025)
        - PIB: 3.1% (IBGE 2024)
        - Desemprego: 6.6% (PNAD Q4/2024)
        - ICC: 91.2 (FGV Jan/2025)
        - Crédito Imob: 14.5% YoY (BCB)
        - CAGED: 1.7% (MTE)
        """
        return EconomicIndicators(
            selic_rate=13.25,
            ipca_12m=4.77,
            pib_growth=3.1,
            unemployment_rate=6.6,
            consumer_confidence=91.2,
            credit_expansion=14.5,
            formal_employment_growth=1.7,
        )

    def calculate_leading_score(self, indicators: EconomicIndicators) -> float:
        """
        Calculate Leading Indicators Score (0-25 pts).

        Components:
        - Employment Growth (0-10): CAGED formal employment
        - Credit Expansion (0-8): Real estate credit YoY
        - Consumer Confidence (0-7): FGV ICC index
        """
        # Employment Growth Score (0-10)
        if indicators.formal_employment_growth >= 3.0:
            employment_score = 10.0
        elif indicators.formal_employment_growth >= 1.5:
            employment_score = 8.0
        elif indicators.formal_employment_growth >= 0:
            employment_score = 5.0
        else:
            employment_score = max(0, 5.0 + indicators.formal_employment_growth)

        # Credit Expansion Score (0-8)
        if indicators.credit_expansion >= 15.0:
            credit_score = 8.0
        elif indicators.credit_expansion >= 10.0:
            credit_score = 6.0
        elif indicators.credit_expansion >= 5.0:
            credit_score = 4.0
        else:
            credit_score = max(0, indicators.credit_expansion * 0.4)

        # Consumer Confidence Score (0-7)
        # ICC ranges 0-200, neutral at 100
        if indicators.consumer_confidence >= 110:
            confidence_score = 7.0
        elif indicators.consumer_confidence >= 100:
            confidence_score = 5.0
        elif indicators.consumer_confidence >= 90:
            confidence_score = 3.0
        else:
            confidence_score = max(0, (indicators.consumer_confidence - 70) * 0.1)

        return round(employment_score + credit_score + confidence_score, 2)

    def calculate_lagging_score(self, indicators: EconomicIndicators) -> float:
        """
        Calculate Lagging Indicators Score (0-15 pts).

        Components:
        - Inflation Control (0-5): IPCA within target
        - Economic Growth (0-5): PIB growth
        - Interest Rate Environment (0-5): SELIC level
        """
        # IPCA Score (0-5) - Target is 3.25% ± 1.5%
        if 1.75 <= indicators.ipca_12m <= 4.75:
            ipca_score = 5.0
        elif indicators.ipca_12m < 1.75:
            ipca_score = 3.0  # Deflation risk
        elif indicators.ipca_12m <= 6.0:
            ipca_score = 3.0
        else:
            ipca_score = max(0, 5.0 - (indicators.ipca_12m - 4.75) * 0.5)

        # PIB Score (0-5)
        if indicators.pib_growth >= 3.0:
            pib_score = 5.0
        elif indicators.pib_growth >= 2.0:
            pib_score = 4.0
        elif indicators.pib_growth >= 1.0:
            pib_score = 3.0
        elif indicators.pib_growth >= 0:
            pib_score = 2.0
        else:
            pib_score = max(0, 2.0 + indicators.pib_growth)

        # SELIC Score (0-5) - Lower is better for real estate
        if indicators.selic_rate <= 9.0:
            selic_score = 5.0
        elif indicators.selic_rate <= 11.0:
            selic_score = 4.0
        elif indicators.selic_rate <= 13.0:
            selic_score = 3.0
        elif indicators.selic_rate <= 14.5:
            selic_score = 2.0
        else:
            selic_score = max(0, 5.0 - (indicators.selic_rate - 9.0) * 0.3)

        return round(ipca_score + pib_score + selic_score, 2)

    def calculate_contextual_score(
        self,
        indicators: EconomicIndicators,
        municipality_population: int = 50000,
        is_metropolitan: bool = False,
    ) -> float:
        """
        Calculate Contextual Adjustment Score (0-10 pts).

        Components:
        - Market Size (0-4): Population tier
        - Metropolitan Effect (0-3): Urban premium
        - Unemployment Delta (0-3): Local vs national
        """
        # Population Tier Score (0-4)
        if municipality_population >= 500000:
            pop_score = 4.0
        elif municipality_population >= 100000:
            pop_score = 3.0
        elif municipality_population >= 50000:
            pop_score = 2.0
        else:
            pop_score = 1.0

        # Metropolitan Premium (0-3)
        metro_score = 3.0 if is_metropolitan else 1.0

        # Unemployment vs National (0-3)
        # Assuming local unemployment similar to national for now
        unemployment_delta_score = 2.0 if indicators.unemployment_rate < 8.0 else 1.0

        return round(pop_score + metro_score + unemployment_delta_score, 2)

    async def analyze(
        self,
        municipality: str,
        municipality_population: int = 50000,
        is_metropolitan: bool = False,
    ) -> dict:
        """
        Execute full P2 Economic Dynamics analysis.

        Returns:
            dict with p2i_lead_score, indicators, decision, and breakdown
        """
        # Fetch live indicators
        indicators = await self.get_live_indicators()

        # Calculate component scores
        leading_score = self.calculate_leading_score(indicators)
        lagging_score = self.calculate_lagging_score(indicators)
        contextual_score = self.calculate_contextual_score(
            indicators, municipality_population, is_metropolitan
        )

        # Total P2i-Lead Score (0-50)
        p2i_lead_score = leading_score + lagging_score + contextual_score

        # Decision Gate: P2i-Lead >= 28 for GO
        if p2i_lead_score >= 35:
            decision = "GO"
            recommendation = "Ambiente macroeconômico altamente favorável para desenvolvimento imobiliário."
        elif p2i_lead_score >= 28:
            decision = "GO"
            recommendation = (
                "Ambiente macroeconômico favorável. Prosseguir com análise detalhada."
            )
        elif p2i_lead_score >= 22:
            decision = "CAUTION"
            recommendation = (
                "Ambiente macroeconômico neutro. Avaliar timing e mitigações."
            )
        else:
            decision = "HOLD"
            recommendation = "Ambiente macroeconômico desfavorável. Aguardar melhora dos indicadores."

        return {
            "municipality": municipality,
            "p2i_lead_score": round(p2i_lead_score, 2),
            "max_score": 50,
            "decision": decision,
            "recommendation": recommendation,
            "is_favorable": p2i_lead_score >= 28,
            "breakdown": {
                "leading_indicators": {
                    "score": leading_score,
                    "max": 25,
                    "components": {
                        "employment_growth": indicators.formal_employment_growth,
                        "credit_expansion": indicators.credit_expansion,
                        "consumer_confidence": indicators.consumer_confidence,
                    },
                },
                "lagging_indicators": {
                    "score": lagging_score,
                    "max": 15,
                    "components": {
                        "ipca_12m": indicators.ipca_12m,
                        "pib_growth": indicators.pib_growth,
                        "selic_rate": indicators.selic_rate,
                    },
                },
                "contextual_factors": {
                    "score": contextual_score,
                    "max": 10,
                    "components": {
                        "municipality_population": municipality_population,
                        "is_metropolitan": is_metropolitan,
                        "unemployment_rate": indicators.unemployment_rate,
                    },
                },
            },
            "live_indicators": {
                "selic_rate": indicators.selic_rate,
                "ipca_12m": indicators.ipca_12m,
                "pib_growth": indicators.pib_growth,
                "unemployment_rate": indicators.unemployment_rate,
                "consumer_confidence": indicators.consumer_confidence,
                "credit_expansion": indicators.credit_expansion,
                "formal_employment_growth": indicators.formal_employment_growth,
            },
            "data_timestamp": datetime.now().isoformat(),
        }

    def analyze_sync(
        self,
        municipality: str,
        municipality_population: int = 50000,
        is_metropolitan: bool = False,
    ) -> dict:
        """Synchronous analysis using offline fallback indicators.

        Use this for Golden Dataset calibration and offline testing.
        For production with live BCB data, use the async `analyze()` method.
        """
        indicators = self.get_offline_indicators()

        leading_score = self.calculate_leading_score(indicators)
        lagging_score = self.calculate_lagging_score(indicators)
        contextual_score = self.calculate_contextual_score(
            indicators, municipality_population, is_metropolitan
        )

        p2i_lead_score = leading_score + lagging_score + contextual_score

        if p2i_lead_score >= 35:
            decision = "GO"
            recommendation = "Ambiente macroeconômico altamente favorável."
        elif p2i_lead_score >= 28:
            decision = "GO"
            recommendation = "Ambiente macroeconômico favorável. Prosseguir."
        elif p2i_lead_score >= 22:
            decision = "CAUTION"
            recommendation = "Ambiente neutro. Avaliar timing."
        else:
            decision = "HOLD"
            recommendation = "Ambiente desfavorável. Aguardar."

        return {
            "municipality": municipality,
            "p2i_lead_score": round(p2i_lead_score, 2),
            "max_score": 50,
            "decision": decision,
            "recommendation": recommendation,
            "is_favorable": p2i_lead_score >= 28,
            "breakdown": {
                "leading_indicators": {"score": leading_score, "max": 25},
                "lagging_indicators": {"score": lagging_score, "max": 15},
                "contextual_factors": {"score": contextual_score, "max": 10},
            },
            "live_indicators": {
                "selic_rate": indicators.selic_rate,
                "ipca_12m": indicators.ipca_12m,
                "pib_growth": indicators.pib_growth,
                "unemployment_rate": indicators.unemployment_rate,
                "consumer_confidence": indicators.consumer_confidence,
                "credit_expansion": indicators.credit_expansion,
                "formal_employment_growth": indicators.formal_employment_growth,
            },
            "data_source": "OFFLINE_FALLBACK_Q1_2025",
            "data_timestamp": datetime.now().isoformat(),
        }
