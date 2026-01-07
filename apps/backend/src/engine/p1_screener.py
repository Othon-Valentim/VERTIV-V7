import polars as pl
from decimal import Decimal
from typing import Optional
from datetime import datetime

from src.domain.schemas import (
    P1GarimpoInput,
    P1GarimpoOutput,
    MarketCyclePhase,
    GoNoGoDecision,
)


class P1ScreenerEngine:
    """
    Engine for P1: Garimpo & Ciclo.
    Analyzes the initial land data to provide a Go/No-Go decision.

    CONSTITUTIONAL COMPLIANCE:
    - All financial math uses Polars (Vectorized).
    """

    # Mock Benchmark Price for the region (R$/m²)
    BENCHMARK_PRICE_SQM = 600.00

    def analyze(self, input_data: P1GarimpoInput) -> P1GarimpoOutput:
        """
        Analyzes the land opportunity using Polars vectorization.
        Implementing ONDA 1: Market Cycle Scoring (0-25 pts).
        """
        # 1. Create Polars LazyFrame from input
        lf = pl.LazyFrame(
            [
                {
                    "area_sqm": input_data.area_sqm,
                    "asking_price": float(input_data.asking_price),
                    "benchmark_price": self.BENCHMARK_PRICE_SQM,
                }
            ]
        )

        # 2. Vectorized Math
        lf = lf.with_columns(
            [(pl.col("asking_price") / pl.col("area_sqm")).alias("price_per_sqm")]
        ).with_columns(
            [(pl.col("benchmark_price") / pl.col("price_per_sqm")).alias("ratio")]
        )

        # 3. Market Cycle Logic (ONDA 1 - 25% weight in P1 score)
        # Heuristic for demo: larger areas + higher price = likely later in cycle.
        # This should eventually be driven by P2 Economic data.
        lf = lf.with_columns(
            [
                pl.when(pl.col("area_sqm") > 10000)
                .then(pl.lit(MarketCyclePhase.RECOVERY))
                .when(pl.col("area_sqm") > 5000)
                .then(pl.lit(MarketCyclePhase.EXPANSION))
                .when(pl.col("area_sqm") > 1000)
                .then(pl.lit(MarketCyclePhase.DECELERATION))
                .otherwise(pl.lit(MarketCyclePhase.RECESSION))
                .alias("cycle_phase")
            ]
        )

        # Cycle Scoring (0-25 pts)
        lf = lf.with_columns(
            [
                pl.when(pl.col("cycle_phase") == MarketCyclePhase.RECOVERY)
                .then(pl.lit(25.0))
                .when(pl.col("cycle_phase") == MarketCyclePhase.EXPANSION)
                .then(pl.lit(20.0))
                .when(pl.col("cycle_phase") == MarketCyclePhase.DECELERATION)
                .then(pl.lit(10.0))
                .otherwise(pl.lit(5.0))
                .alias("cycle_score")
            ]
        )

        # Atratitivity Score (0-100)
        # Formula: 25% Cycle + 75% Price Ratio
        lf = lf.with_columns(
            [
                (pl.col("cycle_score") + (pl.col("ratio") * pl.lit(50.0))).alias(
                    "raw_score"
                )
            ]
        )

        # Cap score
        lf = lf.with_columns([pl.col("raw_score").clip(0, 100).alias("final_score")])

        # 4. Decision Matrix
        lf = lf.with_columns(
            [
                pl.when(pl.col("final_score") >= 70)
                .then(pl.lit(GoNoGoDecision.GO))
                .when(pl.col("final_score") >= 40)
                .then(pl.lit(GoNoGoDecision.CAUTION))
                .otherwise(pl.lit(GoNoGoDecision.NO_GO))
                .alias("decision")
            ]
        )

        # 5. Execute
        results = lf.collect().to_dicts()[0]

        return P1GarimpoOutput(
            cycle_phase=results["cycle_phase"],
            score_attractiveness=float(results["final_score"]),
            decision=results["decision"],
        )
