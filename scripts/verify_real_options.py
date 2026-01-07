import sys
import os
import math

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../apps/backend"))

from src.engine.real_options import RealOptionsEngine
from src.engine.real_options_binomial import BinomialTreeEngine


def test_convergence():
    # Parameters
    S = 100.0  # Land Value
    K = 100.0  # Dev Cost (ATM)
    T = 1.0  # 1 Year
    r = 0.05  # 5% Risk Free
    sigma = 0.20  # 20% Volatility

    # 1. Black-Scholes (European)
    # Using existing engine (assuming it matches standard BS)
    bs_value = RealOptionsEngine.calculate_land_option_value(S, K, T, sigma, r)

    # 2. Binomial (European via American algo with no dividends/early exercise check effectively same for Call on non-div?)
    # Call options on non-dividend paying assets are never exercised early.
    # So American Call Value == European Call Value.

    steps = [50, 100, 500]
    print(f"--- Real Options Verification ---")
    print(f"BS Value: {bs_value:.6f}")

    for N in steps:
        bin_value = BinomialTreeEngine.calculate_american_option(S, K, T, r, sigma, N)
        diff = abs(bin_value - bs_value)
        print(f"Binomial (N={N}): {bin_value:.6f} | Diff: {diff:.6f}")

    if abs(diff) < 0.05:
        print("✅ SUCCESS: Binomial Converges to Black-Scholes")
    else:
        print("❌ FAILURE: Divergence too high")


if __name__ == "__main__":
    test_convergence()
