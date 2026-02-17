"""
P3: Financial Projection Engine
VERTIV v6.0 Global Edition

Responsible for calculating core financial indicators (NPV, IRR, ROI)
and applying the 'Golden Rule' of viability.
"""

from typing import List, Dict, Any, Optional
import numpy_financial as npf
from src.vertiv.biz import tropicalize

class P3ProjectionEngine:
    """
    Financial Projection Engine (P3).
    
    Standardizes the calculation of:
    - NPV (Net Present Value) / VPL
    - IRR (Internal Rate of Return) / TIR
    - Payback Period
    - Maximum Cash Exposure (Vale da Morte)
    - ROI (Return on Investment)
    """

    @staticmethod
    def calculate_indicators(cashflow: List[float]) -> Dict[str, Any]:
        """
        Calculates financial indicators from a monthly cashflow series.
        
        Args:
            cashflow: List of monthly net cash flow values.
            
        Returns:
            Dictionary containing financial metrics and viability flags.
        """
        if not cashflow:
            return {
                "npv": 0.0,
                "irr": 0.0,
                "roi": 0.0,
                "max_exposure": 0.0,
                "payback_months": 0,
                "is_viable": False,
                "viability_reason": "No cashflow data provided."
            }

        # 1. Tropicalized Parameters
        wacc_annual = tropicalize("WACC_ANNUAL", 0.145)
        wacc_monthly = (1 + wacc_annual) ** (1 / 12) - 1

        # 2. NPV (VPL)
        # numpy_financial.npv expects the rate per period (monthly)
        npv_val = npf.npv(wacc_monthly, cashflow)

        # 3. IRR (TIR)
        # numpy_financial.irr returns the rate per period. 
        # We assume monthly periods, so we annualize it.
        # IRR calculation might fail for non-convergent series (e.g. all positive).
        try:
            irr_monthly = npf.irr(cashflow)
            # Handle NaN/None cases from library
            if irr_monthly is None or str(irr_monthly) == 'nan': 
                irr_monthly = 0.0
                
            irr_annual = ((1 + irr_monthly) ** 12) - 1
        except:
            irr_annual = 0.0

        # 4. Max Cash Exposure (Vale da Morte) & ROI
        cumulative_cash = 0.0
        min_cumulative = 0.0
        total_profit = 0.0
        payback_month = 0
        found_payback = False

        for i, val in enumerate(cashflow):
            cumulative_cash += val
            if cumulative_cash < min_cumulative:
                min_cumulative = cumulative_cash
            
            # Identify first month where cumulative turns positive and stays positive (simplified)
            if not found_payback and cumulative_cash > 0:
                payback_month = i
                found_payback = True
            
        total_profit = cumulative_cash  # Final cumulative is total profit/loss
        max_exposure = abs(min_cumulative)

        # ROI = Net Profit / Max Investment (Exposure)
        # If no exposure (pure profit), ROI is infinite, but we cap/handle it.
        if max_exposure > 0:
            roi = total_profit / max_exposure
        else:
            roi = 0.0 # Or undefined. 0.0 is safer for JSON.

        # 5. Golden Rule (Viability Check)
        # Viable if IRR >= WACC (approximated "Selic + Risco")
        # In strictly financial terms, NPV > 0 implies IRR > WACC.
        is_viable = irr_annual >= wacc_annual

        viability_reason = "Viable"
        if not is_viable:
            viability_reason = f"IRR ({irr_annual:.2%}) below WACC ({wacc_annual:.2%})."

        return {
            "npv": float(round(npv_val, 2)),
            "irr": float(round(irr_annual, 4)),
            "roi": float(round(roi, 4)),
            "max_exposure": float(round(max_exposure, 2)),
            "payback_months": payback_month,
            "is_viable": is_viable,
            "viability_reason": viability_reason
        }
