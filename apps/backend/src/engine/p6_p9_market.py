"""
P6-P9: Market Analysis Engines
VERTIV v6.0 Global Edition

P6: Demanda Qualificada - Qualified Demand (5-Stage Funnel)
P7: Oferta & Mercado - Supply Analysis (Competitive Benchmark)
P8: Absorção VSO - Sales Velocity (Absorption Rate)
P9: Convalidação 4:1 - Strategic Validation Gate

Reference: KB_CORE v6.0 Sections 2.8-2.11
"""

from typing import Optional, List, Any
from pydantic import BaseModel, Field
from decimal import Decimal
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


# ==================== P6: DEMAND ENGINE ====================


class IncomeSegment(str, Enum):
    """Target income segments based on MCMV tiers."""

    ECONOMICO_1 = "FAIXA_1"  # Up to R$ 2,640
    ECONOMICO_2 = "FAIXA_2"  # R$ 2,640 - R$ 4,400
    ECONOMICO_3 = "FAIXA_3"  # R$ 4,400 - R$ 8,000
    MEDIO = "MEDIO"  # R$ 8,000 - R$ 20,000
    ALTO = "ALTO"  # Above R$ 20,000


class P6DemandInput(BaseModel):
    """Input for P6 Demand Analysis."""

    municipality: str
    influence_area_population: int = Field(..., gt=0)
    average_household_income: Decimal = Field(..., gt=0)
    target_segment: IncomeSegment = IncomeSegment.MEDIO
    unit_price_min: Decimal = Field(..., gt=0)
    unit_price_max: Decimal = Field(..., gt=0)
    unit_type: str = "LOTE"  # LOTE, APARTAMENTO, CASA


class P6DemandEngine:
    """
    P6 Qualified Demand Analysis Engine.

    Implements 5-Stage Demand Funnel:
    1. Total Families in Influence Area
    2. Income-Qualified Families
    3. Product-Fit Families
    4. Intent-to-Purchase
    5. Effective Demand (Qualified)

    Reference: Harvard ULI Demand Analysis Framework
    """

    # Income ranges by segment (BRL/month)
    INCOME_RANGES = {
        IncomeSegment.ECONOMICO_1: (0, 2640),
        IncomeSegment.ECONOMICO_2: (2640, 4400),
        IncomeSegment.ECONOMICO_3: (4400, 8000),
        IncomeSegment.MEDIO: (8000, 20000),
        IncomeSegment.ALTO: (20000, float("inf")),
    }

    # Funnel conversion rates (calibrated from TIV historical data)
    FUNNEL_RATES = {
        "income_qualification": 0.35,  # 35% in target income bracket
        "product_fit": 0.25,  # 25% interested in product type
        "purchase_intent": 0.15,  # 15% have purchase intent (next 24m)
        "effective_conversion": 0.40,  # 40% become effective demand
    }

    def analyze(self, input_data: P6DemandInput) -> dict:
        """
        Execute 5-Stage Demand Funnel analysis.
        """
        # Stage 1: Total Families
        avg_household_size = 3.1  # IBGE average
        total_families = int(input_data.influence_area_population / avg_household_size)

        # Stage 2: Income-Qualified
        income_range = self.INCOME_RANGES.get(input_data.target_segment, (8000, 20000))
        income_qualified = int(
            total_families * self.FUNNEL_RATES["income_qualification"]
        )

        # Adjust based on actual average income
        avg_income = float(input_data.average_household_income)
        if avg_income < income_range[0]:
            income_qualified = int(
                income_qualified * 0.5
            )  # Reduce if area income is lower
        elif avg_income > income_range[1]:
            income_qualified = int(income_qualified * 0.7)  # Some may be above range

        # Stage 3: Product-Fit
        product_fit = int(income_qualified * self.FUNNEL_RATES["product_fit"])

        # Stage 4: Purchase Intent
        purchase_intent = int(product_fit * self.FUNNEL_RATES["purchase_intent"])

        # Stage 5: Effective Demand
        effective_demand = int(
            purchase_intent * self.FUNNEL_RATES["effective_conversion"]
        )

        # Calculate affordability
        max_affordable_price = avg_income * 12 * 3.5  # 3.5x annual income rule

        return {
            "municipality": input_data.municipality,
            "funnel_stages": {
                "stage_1_total_families": {
                    "count": total_families,
                    "description": "Total de famílias na área de influência",
                },
                "stage_2_income_qualified": {
                    "count": income_qualified,
                    "rate": self.FUNNEL_RATES["income_qualification"],
                    "description": f"Famílias na faixa de renda {input_data.target_segment.value}",
                },
                "stage_3_product_fit": {
                    "count": product_fit,
                    "rate": self.FUNNEL_RATES["product_fit"],
                    "description": "Famílias com fit para o produto",
                },
                "stage_4_purchase_intent": {
                    "count": purchase_intent,
                    "rate": self.FUNNEL_RATES["purchase_intent"],
                    "description": "Famílias com intenção de compra (24 meses)",
                },
                "stage_5_effective_demand": {
                    "count": effective_demand,
                    "rate": self.FUNNEL_RATES["effective_conversion"],
                    "description": "Demanda efetiva qualificada",
                },
            },
            "summary": {
                "qualified_demand_units": effective_demand,
                "target_segment": input_data.target_segment.value,
                "income_bracket_min": income_range[0],
                "income_bracket_max": (
                    income_range[1] if income_range[1] != float("inf") else None
                ),
                "max_affordable_price": round(max_affordable_price, 2),
                "average_household_income": float(input_data.average_household_income),
            },
            "product_parameters": {
                "unit_price_min": float(input_data.unit_price_min),
                "unit_price_max": float(input_data.unit_price_max),
                "unit_type": input_data.unit_type,
            },
            "funnel_efficiency": (
                round(effective_demand / total_families * 100, 2)
                if total_families > 0
                else 0
            ),
            "analysis_timestamp": datetime.now().isoformat(),
        }


# ==================== P7: SUPPLY ENGINE ====================


class CompetitorProject(BaseModel):
    """Competitor project data."""

    name: str
    developer: str
    total_units: int
    units_sold: int
    units_available: int
    price_per_sqm: Decimal
    launch_date: Optional[str] = None
    product_type: str


class P7SupplyInput(BaseModel):
    """Input for P7 Supply Analysis."""

    municipality: str
    influence_area_km: float = 5.0
    competitors: List[CompetitorProject] = []
    market_average_price_sqm: Optional[Decimal] = None


class P7SupplyEngine:
    """
    P7 Supply & Market Analysis Engine.

    Analyzes competitive landscape, inventory levels,
    and pricing benchmarks.
    """

    def __init__(self, search_engine: Optional[Any] = None):
        self.search_engine = search_engine

    async def discover_competitors(
        self, municipality: str, product_type: str
    ) -> List[CompetitorProject]:
        """
        Uses SearchEngine to find competitors in the market.
        """
        if not self.search_engine:
            return []

        query = f"{product_type} em {municipality} lancamentos"
        results = await self.search_engine.search_market_data(
            query, location=municipality
        )

        # In a real scenario, we'd use an LLM or a more complex parser
        # to convert snippets into many CompetitorProject objects.
        # For v6.1.0, we provide a structured placeholder based on search hits.
        raw_competitors = self.search_engine.parse_competitors(results)

        discovered = []
        for i, raw in enumerate(raw_competitors):
            # Mapping fuzzy search results to structured CompetitorProject
            discovered.append(
                CompetitorProject(
                    name=raw["title"][:50],
                    developer="Unknown (Search Hit)",
                    total_units=100,  # Estimates
                    units_sold=50,
                    units_available=50,
                    price_per_sqm=Decimal("7500.00"),  # Baseline for Nova Lima/MG
                    product_type=product_type,
                )
            )

        return discovered

    async def analyze(self, input_data: P7SupplyInput) -> dict:
        """
        Execute Supply Analysis.
        """
        competitors = input_data.competitors

        if not competitors:
            # Return empty analysis if no competitors
            return {
                "municipality": input_data.municipality,
                "summary": {
                    "competitors_count": 0,
                    "active_inventory_units": 0,
                    "total_launched_units": 0,
                    "average_price_sqm": (
                        float(input_data.market_average_price_sqm)
                        if input_data.market_average_price_sqm
                        else 0
                    ),
                    "market_saturation": "LOW",
                },
                "competitors_detail": [],
                "pricing_analysis": {
                    "min_price_sqm": 0,
                    "max_price_sqm": 0,
                    "average_price_sqm": 0,
                    "price_spread_pct": 0,
                },
                "inventory_analysis": {
                    "total_available": 0,
                    "absorption_rate_avg": 0,
                    "months_of_supply": 0,
                },
                "analysis_timestamp": datetime.now().isoformat(),
            }

        # Aggregate metrics
        total_units = sum(c.total_units for c in competitors)
        total_sold = sum(c.units_sold for c in competitors)
        total_available = sum(c.units_available for c in competitors)

        # Pricing analysis
        prices = [float(c.price_per_sqm) for c in competitors]
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        price_spread = (
            ((max_price - min_price) / avg_price * 100) if avg_price > 0 else 0
        )

        # Absorption metrics
        avg_sales_rate = total_sold / len(competitors) if competitors else 0
        months_of_supply = (
            total_available / (avg_sales_rate / 12) if avg_sales_rate > 0 else 999
        )

        # Market saturation assessment
        if months_of_supply > 36:
            saturation = "HIGH"
        elif months_of_supply > 24:
            saturation = "MEDIUM"
        else:
            saturation = "LOW"

        return {
            "municipality": input_data.municipality,
            "summary": {
                "competitors_count": len(competitors),
                "active_inventory_units": total_available,
                "total_launched_units": total_units,
                "total_sold_units": total_sold,
                "average_price_sqm": round(avg_price, 2),
                "market_saturation": saturation,
            },
            "competitors_detail": [
                {
                    "name": c.name,
                    "developer": c.developer,
                    "total_units": c.total_units,
                    "units_sold": c.units_sold,
                    "units_available": c.units_available,
                    "sell_through_rate": (
                        round(c.units_sold / c.total_units * 100, 1)
                        if c.total_units > 0
                        else 0
                    ),
                    "price_per_sqm": float(c.price_per_sqm),
                    "product_type": c.product_type,
                }
                for c in competitors
            ],
            "pricing_analysis": {
                "min_price_sqm": round(min_price, 2),
                "max_price_sqm": round(max_price, 2),
                "average_price_sqm": round(avg_price, 2),
                "price_spread_pct": round(price_spread, 1),
            },
            "inventory_analysis": {
                "total_available": total_available,
                "months_of_supply": round(months_of_supply, 1),
                "market_health": (
                    "HEALTHY"
                    if months_of_supply <= 18
                    else "CAUTIOUS" if months_of_supply <= 30 else "SATURATED"
                ),
            },
            "analysis_timestamp": datetime.now().isoformat(),
        }


# ==================== P8: ABSORPTION ENGINE ====================


class P8AbsorptionInput(BaseModel):
    """Input for P8 Absorption Analysis."""

    municipality: str
    project_units: int = Field(..., gt=0)
    project_price_avg: Decimal = Field(..., gt=0)
    qualified_demand: int = Field(..., gt=0)  # From P6
    active_inventory: int = Field(default=0, ge=0)  # From P7
    market_vso_monthly: float = Field(default=0.08, ge=0, le=1)  # Historical VSO


class P8AbsorptionEngine:
    """
    P8 Sales Velocity (VSO) Analysis Engine.

    Calculates projected absorption rate and timeline
    based on demand/supply dynamics.
    """

    # VSO benchmarks by product type (units/month per 100 units inventory)
    VSO_BENCHMARKS = {
        "LOTEAMENTO": 0.06,  # 6% per month
        "CONDOMINIO": 0.08,  # 8% per month
        "VERTICAL_MEDIO": 0.05,  # 5% per month
        "VERTICAL_ALTO": 0.03,  # 3% per month
    }

    def analyze(self, input_data: P8AbsorptionInput) -> dict:
        """
        Execute Absorption Analysis.
        """
        # Calculate total market inventory
        total_inventory = input_data.project_units + input_data.active_inventory

        # Demand/Supply ratio (the famous 4:1 factor)
        demand_supply_ratio = (
            input_data.qualified_demand / total_inventory if total_inventory > 0 else 0
        )

        # Adjust VSO based on demand/supply ratio
        base_vso = input_data.market_vso_monthly
        if demand_supply_ratio >= 4.0:
            adjusted_vso = base_vso * 1.3  # Strong demand premium
        elif demand_supply_ratio >= 2.0:
            adjusted_vso = base_vso * 1.1
        elif demand_supply_ratio >= 1.0:
            adjusted_vso = base_vso
        else:
            adjusted_vso = base_vso * 0.7  # Weak demand penalty

        # Monthly sales velocity
        monthly_sales = input_data.project_units * adjusted_vso

        # Absorption timeline
        if monthly_sales > 0:
            absorption_months = int(input_data.project_units / monthly_sales)
        else:
            absorption_months = 999

        # Assessment
        if absorption_months <= 18:
            assessment = "EXCELLENT"
            recommendation = "Velocidade de vendas projetada é excelente. Prosseguir."
        elif absorption_months <= 24:
            assessment = "GOOD"
            recommendation = "Velocidade adequada dentro do benchmark TIV (24 meses)."
        elif absorption_months <= 36:
            assessment = "MODERATE"
            recommendation = (
                "Velocidade moderada. Considerar faseamento ou ajuste de preço."
            )
        else:
            assessment = "SLOW"
            recommendation = (
                "Velocidade abaixo do esperado. Reavaliar produto ou pricing."
            )

        return {
            "municipality": input_data.municipality,
            "project_metrics": {
                "total_units": input_data.project_units,
                "average_price": float(input_data.project_price_avg),
                "total_vgv": float(input_data.project_price_avg)
                * input_data.project_units,
            },
            "absorption_projection": {
                "monthly_sales_velocity": round(monthly_sales, 2),
                "projected_absorption_months": absorption_months,
                "annualized_vso": round(adjusted_vso * 12 * 100, 1),
                "assessment": assessment,
                "recommendation": recommendation,
            },
            "market_dynamics": {
                "qualified_demand": input_data.qualified_demand,
                "total_market_inventory": total_inventory,
                "demand_supply_ratio": round(demand_supply_ratio, 2),
                "ratio_assessment": (
                    "STRONG"
                    if demand_supply_ratio >= 4.0
                    else "ADEQUATE" if demand_supply_ratio >= 2.0 else "WEAK"
                ),
            },
            "vso_analysis": {
                "base_vso_monthly": round(input_data.market_vso_monthly * 100, 1),
                "adjusted_vso_monthly": round(adjusted_vso * 100, 1),
                "adjustment_factor": (
                    round(adjusted_vso / base_vso, 2) if base_vso > 0 else 1.0
                ),
            },
            "analysis_timestamp": datetime.now().isoformat(),
        }


# ==================== P9: VALIDATION ENGINE ====================


class P9ValidationInput(BaseModel):
    """Input for P9 Validation Gate."""

    municipality: str

    # From P6
    qualified_demand: int = Field(..., gt=0)

    # From P7
    active_inventory: int = Field(default=0, ge=0)
    competitors_count: int = Field(default=0, ge=0)

    # From P8
    projected_absorption_months: int = Field(default=24)

    # Project
    project_units: int = Field(..., gt=0)
    project_price_sqm: Decimal = Field(..., gt=0)
    market_price_sqm: Decimal = Field(..., gt=0)


class P9ValidationEngine:
    """
    P9 Strategic Validation (Gate 4:1) Engine.

    Final market validation before financial modeling.
    Implements the TIV 4:1 Demand:Supply ratio gate.
    """

    # Gate thresholds (from KB_CORE v6.0)
    THRESHOLDS = {
        "ratio_excellent": 6.0,
        "ratio_good": 4.0,
        "ratio_acceptable": 2.5,
        "ratio_minimum": 1.67,
        "absorption_max_months": 24,
        "price_variance_max": 0.15,  # 15% max deviation from market
    }

    def analyze(self, input_data: P9ValidationInput) -> dict:
        """
        Execute P9 Strategic Validation.
        """
        # Calculate 4:1 Ratio
        total_supply = input_data.project_units + input_data.active_inventory
        ratio_4_1 = (
            input_data.qualified_demand / total_supply if total_supply > 0 else 0
        )

        # Price competitiveness
        price_variance = (
            (
                (
                    float(input_data.project_price_sqm)
                    - float(input_data.market_price_sqm)
                )
                / float(input_data.market_price_sqm)
            )
            if float(input_data.market_price_sqm) > 0
            else 0
        )

        # Gate evaluations
        gates = []

        # Gate 1: 4:1 Ratio
        if ratio_4_1 >= self.THRESHOLDS["ratio_excellent"]:
            ratio_status = "PASS_EXCELLENT"
            ratio_passed = True
        elif ratio_4_1 >= self.THRESHOLDS["ratio_good"]:
            ratio_status = "PASS"
            ratio_passed = True
        elif ratio_4_1 >= self.THRESHOLDS["ratio_acceptable"]:
            ratio_status = "PASS_MARGINAL"
            ratio_passed = True
        elif ratio_4_1 >= self.THRESHOLDS["ratio_minimum"]:
            ratio_status = "CAUTION"
            ratio_passed = False
        else:
            ratio_status = "FAIL"
            ratio_passed = False

        gates.append(
            {
                "gate": "GATE_4_1_RATIO",
                "value": round(ratio_4_1, 2),
                "threshold": self.THRESHOLDS["ratio_good"],
                "status": ratio_status,
                "passed": ratio_passed,
            }
        )

        # Gate 2: Absorption Timeline
        absorption_passed = (
            input_data.projected_absorption_months
            <= self.THRESHOLDS["absorption_max_months"]
        )
        gates.append(
            {
                "gate": "GATE_ABSORPTION",
                "value": input_data.projected_absorption_months,
                "threshold": self.THRESHOLDS["absorption_max_months"],
                "status": "PASS" if absorption_passed else "FAIL",
                "passed": absorption_passed,
            }
        )

        # Gate 3: Price Competitiveness
        price_passed = abs(price_variance) <= self.THRESHOLDS["price_variance_max"]
        gates.append(
            {
                "gate": "GATE_PRICE_COMPETITIVENESS",
                "value": round(price_variance * 100, 1),
                "threshold": self.THRESHOLDS["price_variance_max"] * 100,
                "status": "PASS" if price_passed else "CAUTION",
                "passed": price_passed,
            }
        )

        # Overall validation
        critical_gates_passed = ratio_passed and absorption_passed
        all_gates_passed = all(g["passed"] for g in gates)

        if all_gates_passed:
            decision = "GO"
            is_validated = True
            recommendation = (
                "VALIDADO: Todos os gates de mercado aprovados. Prosseguir para P10."
            )
        elif critical_gates_passed:
            decision = "CAUTION"
            is_validated = True
            recommendation = "VALIDADO COM RESSALVAS: Gates críticos aprovados. Monitorar competitividade de preço."
        elif ratio_passed:
            decision = "HOLD"
            is_validated = False
            recommendation = (
                "AGUARDAR: Demanda favorável mas absorção lenta. Considerar faseamento."
            )
        else:
            decision = "NO_GO"
            is_validated = False
            recommendation = f"NÃO VALIDADO: Fator 4:1 insuficiente ({ratio_4_1:.2f}). Mercado saturado."

        # Audit Requirement Singularity v6.1.0: Log decisions to stdout
        print(
            f"[P9_VALIDATION] GATE DECISION: {decision} | Validated: {is_validated} | Ratio 4:1: {ratio_4_1:.2f}"
        )

        return {
            "municipality": input_data.municipality,
            "gate_result": {
                "decision": decision,
                "is_validated": is_validated,
                "recommendation": recommendation,
            },
            "key_ratio": {
                "gate_4_1_ratio": round(ratio_4_1, 2),
                "qualified_demand": input_data.qualified_demand,
                "total_supply": total_supply,
                "project_units": input_data.project_units,
                "active_inventory": input_data.active_inventory,
            },
            "gates_detail": gates,
            "gates_summary": {
                "total": len(gates),
                "passed": sum(1 for g in gates if g["passed"]),
                "failed": sum(1 for g in gates if not g["passed"]),
            },
            "market_position": {
                "price_variance_pct": round(price_variance * 100, 1),
                "price_position": (
                    "PREMIUM"
                    if price_variance > 0.05
                    else "COMPETITIVE" if price_variance > -0.05 else "AGGRESSIVE"
                ),
                "competitors_count": input_data.competitors_count,
            },
            "thresholds_reference": self.THRESHOLDS,
            "analysis_timestamp": datetime.now().isoformat(),
        }
