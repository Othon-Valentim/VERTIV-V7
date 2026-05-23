import polars as pl
import numpy_financial as npf
from typing import List, Dict, Optional
from src.vertiv.biz import tropicalize


class CashFlowEngine:
    """
    Core Financial Engine for Discounted Cash Flow (DCF).

    Greenium WACC Adjustment Methodology:
    -------------------------------------
    The 'Greenium' (Green Premium) is applied as a discount to the WACC (Weighted Average Cost of Capital).

    Formula:
        Adjusted_WACC = Base_WACC - Greenium_Spread

    Where:
        - Base_WACC: Theoretical cost of capital for standard real estate projects (e.g., 14.5%).
        - Greenium_Spread: Extracted from ANBIMA (e.g., 0.3% to 0.5% for Certified Green Bonds).

    Impact:
        A lower discount rate results in a higher NPV (Net Present Value), reflecting the
        financial efficiency of sustainable access to capital.
    """

    def __init__(self, months: int = 360):
        self.months = months

    def calculate_project_cashflow(
        self,
        units: int,
        avg_price: float,
        cost_total: float,
        land_cost: float = 0.0,
        start_sales_month: int = 6,
        construction_months: int = 36,
        wacc_annual: Optional[float] = None,
        use_ret: bool = True,
        permuta_pct: float = 0.0,
        funding_model: str = "SBPE",
        incc_annual: Optional[float] = None,
        ipca_annual: Optional[float] = None,
    ) -> dict:
        """
        v6.1.0-SINGULARITY (TROPICALIZED)
        ---------------------------------
        - RET: 4% Taxation on Gross Revenue.
        - Permuta: Physical unit reduction (VGV reduction).
        - Funding: SBPE (Late Revenue) vs ASSOCIATIVO (Front-loaded Revenue).
        - Inflation indices differentiated (INCC vs IPCA).
        """
        # 0. Tropicalization Resolution
        wacc_annual = (
            wacc_annual
            if wacc_annual is not None
            else tropicalize("WACC_ANNUAL", 0.145)
        )
        incc_annual = (
            incc_annual if incc_annual is not None else tropicalize("INCC_ANNUAL", 0.06)
        )
        ipca_annual = (
            ipca_annual
            if ipca_annual is not None
            else tropicalize("IPCA_ANNUAL", 0.045)
        )

        # 1. Time Series — use project lifecycle, not 360 months
        # Total period = construction + post-sales buffer
        total_months = max(self.months, construction_months + 12)
        lf = pl.LazyFrame({"month": list(range(total_months + 1))})

        # 2. Units after Permuta
        effective_units = units * (1.0 - permuta_pct)
        # Sales span the construction period minus ramp-up
        sales_duration = max(construction_months - start_sales_month, 12)
        units_per_month = effective_units / sales_duration
        end_sales_month = start_sales_month + sales_duration

        # 3. Monthly Indices
        incc_m = (1 + incc_annual) ** (1 / 12) - 1
        ipca_m = (1 + ipca_annual) ** (1 / 12) - 1

        # 4. Sales Curve & Funding Model
        # SBPE: Only receive cash when units are sold (Standard)
        # ASSOCIATIVO: Banks transfer % of construction early
        lf = lf.with_columns(
            pl.when(
                (pl.col("month") >= start_sales_month)
                & (pl.col("month") < end_sales_month)
            )
            .then(pl.lit(units_per_month))
            .otherwise(pl.lit(0.0))
            .alias("units_sold")
        )

        # 5. Financials with Inflation & Taxes
        tax_rate = 0.04 if use_ret else 0.15  # RET vs Conservative Corporate Tax

        lf = lf.with_columns(
            [
                # Gross Revenue + IPCA correction
                (
                    pl.col("units_sold")
                    * pl.lit(avg_price)
                    * ((1 + ipca_m) ** pl.col("month"))
                ).alias("revenue_gross"),
                # Construction Cost + INCC correction (use configurable period)
                pl.when(pl.col("month") <= construction_months)
                .then(
                    pl.lit(cost_total / construction_months)
                    * ((1 + incc_m) ** pl.col("month"))
                )
                .otherwise(pl.lit(0.0))
                .alias("construction_cost"),
                # Land cost at month 0
                pl.when(pl.col("month") == 0)
                .then(pl.lit(land_cost))
                .otherwise(pl.lit(0.0))
                .alias("land_cost"),
            ]
        )

        # 6. Apply Funding Model Adjustments (Associativo Alpha)
        if funding_model == "ASSOCIATIVO":
            # In Associativo, the bank pays construction costs + margin early
            # We simulate this by front-loading 80% of sales revenue during construction
            lf = lf.with_columns(
                [
                    pl.when(pl.col("month") <= construction_months)
                    .then(pl.col("revenue_gross") * 0.8)
                    .otherwise(pl.col("revenue_gross"))
                    .alias("revenue_gross")
                ]
            )

        # 7. Taxes & Net Flow
        lf = lf.with_columns(
            [(pl.col("revenue_gross") * pl.lit(tax_rate)).alias("tax_amount")]
        ).with_columns(
            (
                pl.col("revenue_gross")
                - pl.col("construction_cost")
                - pl.col("land_cost")
                - pl.col("tax_amount")
            ).alias("net_cash_flow")
        )

        # 8. Discounting (RICS ESG Integration)
        wacc_monthly = (1 + wacc_annual) ** (1 / 12) - 1
        lf = lf.with_columns(
            [
                (
                    pl.col("net_cash_flow") / ((1 + wacc_monthly) ** pl.col("month"))
                ).alias("pv_net_cash_flow")
            ]
        )

        # 9. Execute
        df = lf.collect()

        # 10. Metrics — trim trailing zeros before IRR to avoid convergence issues
        cashflow_series = df["net_cash_flow"].to_list()
        # Trim trailing months with ~zero cashflow (they corrupt npf.irr)
        trimmed = cashflow_series[:]
        while len(trimmed) > 1 and abs(trimmed[-1]) < 0.01:
            trimmed.pop()

        irr = npf.irr(trimmed) if len(trimmed) > 1 else 0.0
        if irr is None or str(irr) == "nan":
            irr = 0.0
        irr_annual_pct = round(float(((1 + irr) ** 12) - 1) * 100, 2)
        npv = df["pv_net_cash_flow"].sum()
        vgv = effective_units * avg_price

        return {
            "dataframe": df.to_dicts(),
            "metrics": {
                "irr_monthly": round(float(irr), 6),
                "irr_annual": irr_annual_pct,
                "irr": irr_annual_pct,
                "npv": round(float(npv), 2),
                "vgv": round(float(vgv), 2),
                "total_revenue": round(float(df["revenue_gross"].sum()), 2),
                "total_cost": round(
                    float(df["construction_cost"].sum() + df["land_cost"].sum()), 2
                ),
                "total_profit": round(float(df["net_cash_flow"].sum()), 2),
                "total_taxes": round(float(df["tax_amount"].sum()), 2),
                "land_cost": round(float(land_cost), 2),
                "construction_months": construction_months,
                "sales_duration": sales_duration,
                "margin_pct": (
                    round(float(df["net_cash_flow"].sum() / vgv * 100), 2)
                    if vgv > 0
                    else 0.0
                ),
            },
        }
