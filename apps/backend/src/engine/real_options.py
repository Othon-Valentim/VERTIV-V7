import numpy as np
from scipy.stats import norm
from typing import Union, List


class RealOptionsEngine:
    @staticmethod
    def black_scholes_vectorized(
        S: Union[float, np.ndarray],
        K: Union[float, np.ndarray],
        T: Union[float, np.ndarray],
        r: float,
        sigma: float,
        option_type: str = "call",
    ) -> Union[float, np.ndarray]:
        """
        Vectorized Black-Scholes-Merton calculation.

        S: Spot Price (PV of Asset)
        K: Strike Price (Investment Cost)
        T: Time to Expiration (Years)
        r: Risk-free rate
        sigma: Volatility
        """

        # Prevent division by zero
        if sigma <= 0 or T <= 0:
            return max(0.0, S - K) if option_type == "call" else max(0.0, K - S)

        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if option_type == "call":
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

        return price

    @staticmethod
    def calculate_land_option_value(
        land_value_current: float,
        development_cost: float,
        time_to_permit_years: float,
        volatility: float = 0.20,
        risk_free_rate: float = 0.11,
    ) -> float:
        """
        Calculates the Real Option value of a Land Bank asset.
        """
        return RealOptionsEngine.black_scholes_vectorized(
            S=land_value_current,
            K=development_cost,
            T=time_to_permit_years,
            r=risk_free_rate,
            sigma=volatility,
            option_type="call",
        )
