"""
VERTIV Business Logic & Tropicalization Module
Centralizes financial constants, inflation indices, and market parameters.
"""

import os
from typing import Any, TypeVar

T = TypeVar("T")

# Tropicalized Defaults (Brazil Market 2026)
_DEFAULTS = {
    "WACC_ANNUAL": 0.145,      # 14.5% Standard Real Estate WACC
    "INCC_ANNUAL": 0.06,       # 6.0% Construction Inflation
    "IPCA_ANNUAL": 0.045,      # 4.5% General Inflation
    "SELIC_RATE": 11.25,       # 11.25% Base Interest Rate
    "CDI_RATE": 11.15,         # 11.15% Interbank Rate
    "UNEMPLOYMENT_RATE": 7.5,  # 7.5% Target
    "GDP_GROWTH": 2.5,         # 2.5% Target
    "RET_TAX_RATE": 0.04,      # 4% Regime Especial de Tributação
    "CORP_TAX_RATE": 0.15,     # 15% Presumed Profit Baseline
    "EQUITY_REQUIRED": 0.30,   # 30% Equity / 70% Debt
}

def tropicalize(key: str, default: T) -> T:
    """
    Retrieves a 'tropicalized' value for a given business key.
    
    Priority:
    1. Environment Variable (VERTIV_{KEY})
    2. Internal Defaults Dictionary (_DEFAULTS)
    3. Provided Default (Code fallback)
    """
    env_key = f"VERTIV_{key}"
    env_val = os.getenv(env_key)
    
    if env_val is not None:
        # Simple type conversion attempts
        if isinstance(default, bool):
            return str(env_val).lower() in ("true", "1", "yes") # type: ignore
        if isinstance(default, int):
            try:
                return int(env_val) # type: ignore
            except ValueError:
                pass
        if isinstance(default, float):
            try:
                return float(env_val) # type: ignore
            except ValueError:
                pass
        return env_val # type: ignore

    if key in _DEFAULTS:
        val = _DEFAULTS[key]
        # Type safety check could go here, but keeping it loose for speed
        return val # type: ignore

    return default
