import numpy as np
from typing import Optional


class BinomialTreeEngine:
    """
    Real Options Valuation using Binomial Lattice (CRR Model).
    Supports American Options (Exercise Early) - crucial for Land Banking.
    """

    @staticmethod
    def calculate_american_option(
        S: float,  # Current Land Value (Spot Price)
        K: float,  # Development Cost (Strike Price)
        T: float,  # Time to Permit (Years)
        r: float,  # Risk-free Rate
        sigma: float,  # Volatility
        N: int = 100,  # Number of Time Steps
        q: float = 0.0,  # Dividend Yield (Cost of Carry or Yield from interim use)
    ) -> float:
        """
        Calculates the value of an American Call Option using the CRR Binomial Tree.
        Value = Max(Hold, Develop) at each node.
        """
        if T <= 0 or sigma <= 0:
            return max(0.0, S - K)

        # Delta T
        dt = T / N

        # Up and Down factors (CRR)
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u

        # Risk-neutral probability
        # p = (e^(r-q)dt - d) / (u - d)
        a = np.exp((r - q) * dt)
        p = (a - d) / (u - d)

        # Discount factor per step
        df = np.exp(-r * dt)

        # 1. Initialize Asset Prices at Value Date (Leaf Nodes)
        # S_T = S * u^j * d^(N-j)
        asset_values = np.zeros(N + 1)
        for j in range(N + 1):
            asset_values[j] = S * (u**j) * (d ** (N - j))

        # 2. Initialize Option Values at Maturity
        # Payoff = Max(S_T - K, 0)
        option_values = np.maximum(asset_values - K, 0.0)

        # 3. Backward Induction
        for i in range(N - 1, -1, -1):
            for j in range(i + 1):
                # Continuation Value (Hold)
                hold_value = df * (
                    p * option_values[j + 1] + (1 - p) * option_values[j]
                )

                # Asset Value at this node (for Early Exercise check)
                # Recompute S at node (i, j)
                # Or optimize by storing/updating asset_values array in place?
                # S_node = S * (u**j) * (d**(i-j))
                # optimization: asset_values[j] currently stores S_{i+1, j} or S_{i+1, j+1}?
                # Let's recompute to be safe/clear, or use the property S_down = S_current * d.
                # Actually, standard optimization reduces array size. Let's start simple.
                S_node = S * (u**j) * (d ** (i - j))

                # Exercise Value (Develop Now)
                exercise_value = S_node - K

                # American Option: Max(Hold, Exercise)
                option_values[j] = max(hold_value, exercise_value)

        return float(option_values[0])
