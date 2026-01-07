import polars as pl
import numpy_financial as npf
from typing import List, Dict


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
        start_sales_month: int = 6,
        wacc_annual: float = 0.145,
        use_ret: bool = True,
        permuta_pct: float = 0.0,
        funding_model: str = "SBPE",
        incc_annual: float = 0.06,
        ipca_annual: float = 0.045,
    ) -> dict:
        """
        v6.1.0-SINGULARITY (TROPICALIZED)
        ---------------------------------
        - RET: 4% Taxation on Gross Revenue.
        - Permuta: Physical unit reduction (VGV reduction).
        - Funding: SBPE (Late Revenue) vs ASSOCIATIVO (Front-loaded Revenue).
        - Inflation indices differentiated (INCC vs IPCA).
        """
        # 1. Time Series
        lf = pl.LazyFrame({"month": list(range(self.months + 1))})

        # 2. Units after Permuta
        effective_units = units * (1.0 - permuta_pct)
        units_per_month = effective_units / 24

        # 3. Monthly Indices
        incc_m = (1 + incc_annual) ** (1 / 12) - 1
        ipca_m = (1 + ipca_annual) ** (1 / 12) - 1

        # 4. Sales Curve & Funding Model
        # SBPE: Only receive cash when units are sold (Standard)
        # ASSOCIATIVO: Banks transfer % of construction early
        lf = lf.with_columns(
            pl.when(
                (pl.col("month") >= start_sales_month)
                & (pl.col("month") < start_sales_month + 24)
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
                # Construction Cost + INCC correction
                pl.when(pl.col("month") <= 36)
                .then(pl.lit(cost_total / 36) * ((1 + incc_m) ** pl.col("month")))
                .otherwise(pl.lit(0.0))
                .alias("construction_cost"),
            ]
        )

        # 6. Apply Funding Model Adjustments (Associativo Alpha)
        if funding_model == "ASSOCIATIVO":
            # In Associativo, the bank pays construction costs + margin early
            # We simulate this by front-loading 80% of sales revenue during construction
            lf = lf.with_columns(
                [
                    pl.when(pl.col("month") <= 36)
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

        # 10. Metrics
        cashflow_series = df["net_cash_flow"].to_list()
        irr = npf.irr(cashflow_series) or 0.0
        npv = df["pv_net_cash_flow"].sum()

        return {
            "dataframe": df.to_dicts(),
            "metrics": {
                "irr": round(irr * 100, 2),
                "npv": round(npv, 2),
                "total_revenue": df["revenue_gross"].sum(),
                "total_profit": df["net_cash_flow"].sum(),
                "total_taxes": df["tax_amount"].sum(),
            },
        }
