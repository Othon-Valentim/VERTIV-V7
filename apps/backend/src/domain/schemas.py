from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, condecimal, constr
from decimal import Decimal


# --- RICS ESG Framework ---
class ESGCertification(str, Enum):
    LEED = "LEED"
    BREEAM = "BREEAM"
    AQUA = "AQUA"
    WELL = "WELL"
    EDGE = "EDGE"
    NONE = "NONE"


class ESGAttributes(BaseModel):
    certification: ESGCertification = ESGCertification.NONE
    green_premium: float = Field(
        default=0.0,
        description="Projected value increase due to ESG (RICS Adjusted NPV)",
    )
    brown_discount: float = Field(
        default=0.0, description="Projected value decrease due to lack of ESG"
    )
    carbon_footprint_tonnes: Optional[float] = None


# --- TIV Methodology Enums ---
class MarketCyclePhase(str, Enum):
    RECOVERY = "RECUPERACAO"
    EXPANSION = "EXPANSAO"
    DECELERATION = "DESACELERACAO"
    RECESSION = "RECESSAO"


class ProductType(str, Enum):
    LOTEAMENTO_ABERTO = "LOTEAMENTO_ABERTO"
    CONDOMINIO_FECHADO = "CONDOMINIO_FECHADO"
    VERTICAL_RESIDENCIAL = "VERTICAL_RESIDENCIAL"
    VERTICAL_COMERCIAL = "VERTICAL_COMERCIAL"
    MISTO = "MISTO"


class GoNoGoDecision(str, Enum):
    GO = "GO"
    NO_GO = "NO_GO"
    CAUTION = "CAUTION"
    HOLD = "HOLD"


# --- Step Models ---


# P1: Garimpo
class P1GarimpoInput(BaseModel):
    location_municipality: str
    location_neighborhood: str
    area_sqm: float = Field(..., gt=0)
    asking_price: Decimal = Field(..., gt=0)


class P1GarimpoOutput(BaseModel):
    cycle_phase: MarketCyclePhase
    score_attractiveness: float = Field(..., ge=0, le=100)
    decision: GoNoGoDecision


# P2: Dinamica Economica
class P2EconomicDynamicsOutput(BaseModel):
    p2i_lead_score: float = Field(..., ge=0, le=50)
    is_favorable: bool


# P3: Area de Influencia
class P3InfluenceAreaInput(BaseModel):
    latitude: float
    longitude: float
    buffer_radius_km: Optional[float] = None
    isochrone_minutes: Optional[float] = None


class P3InfluenceAreaOutput(BaseModel):
    population_total: int
    average_income_brl: Decimal
    polygon_geojson: dict


# P4: Vocacao
class P4VocationOutput(BaseModel):
    score_zoning: float = Field(..., ge=0, le=10)  # 30%
    score_centrality: float = Field(..., ge=0, le=10)  # 40%
    score_density: float = Field(..., ge=0, le=10)  # 30%
    total_score: float
    recommended_product: ProductType


# P5: Legal
class P5LegalOutput(BaseModel):
    impediments: List[str]
    has_environmental_restrictions: bool
    is_approved: bool  # Gate Binario


# P6: Demanda
class P6DemandOutput(BaseModel):
    families_total: int
    income_bracket_target_min: Decimal
    income_bracket_target_max: Decimal
    qualified_demand_units: int


# P7: Oferta
class P7SupplyOutput(BaseModel):
    competitors_count: int
    active_inventory_units: int
    average_price_sqm: Decimal


# P8: Absorcao
class P8AbsorptionOutput(BaseModel):
    monthly_sales_velocity_units: float
    projected_absorption_months: int


# P9: Convalidacao
class P9ValidationOutput(BaseModel):
    gate_4_1_ratio: float  # 4:1 Ratio
    is_validated: bool


# P10: Financial (The Diamond Core)
class P10FinancialInput(BaseModel):
    total_units: int
    sales_price_avg: Decimal
    construction_cost_total: Decimal
    land_cost: Decimal
    development_months: int

    # Tropicalization Additions
    use_ret_taxation: bool = Field(
        default=True, description="Apply 4% RET on Gross Revenue"
    )
    funding_model: str = Field(
        default="SBPE", description="SBPE (Traditional) vs ASSOCIATIVO (MCMV/Caixa)"
    )
    permuta_physical_pct: float = Field(
        default=0.0, description="Percentage of units given to land owner"
    )
    incc_annual_rate: float = Field(
        default=0.06, description="Inflation index for Construction costs"
    )
    ipca_annual_rate: float = Field(
        default=0.045, description="Inflation index for Sales/Revenue"
    )


class P10FinancialOutput(BaseModel):
    npv: Decimal
    irr: float
    roe: float
    payback_months: int
    exposure_max: Decimal
    esg_adjusted_npv: Decimal  # RICS
    real_option_land_value: Optional[float] = Field(
        default=0.0, description="Black-Scholes Value"
    )


# --- Real Options (Land Banking) ---
class RealOptionsInput(BaseModel):
    land_value_current: float
    development_cost_forcing: float  # Strike Price (K)
    time_to_permit_years: float
    volatility: float = 0.20
    risk_free_rate: float = 0.11  # Selic


# --- Aggregates ---
class ProjectTIV(BaseModel):
    id: str
    name: str
    municipality: str = Field(default="Belo Horizonte", description="City of the project")
    esg: ESGAttributes = ESGAttributes()
    real_options: Optional[RealOptionsInput] = None
    p1: Optional[P1GarimpoOutput] = None

    # IT-11 Compliance (Fire Safety)
    is_mixed_use: bool = False
    separate_access_cores: bool = True  # Default safe assumption, but must be checked
    fire_load_category: str = "Residencial"
    efficiency: float = Field(
        default=0.85, description="Project efficiency (Sellable / Total Area)"
    )

    p4: Optional[P4VocationOutput] = None
    p10: Optional[P10FinancialOutput] = None
    financial_input: Optional[P10FinancialInput] = None


# --- Async Architecture Schemas ---
class SimulationStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class SimulationRequest(BaseModel):
    simulation_id: str
    project: ProjectTIV
    webhook_url: Optional[str] = None
    narrative_status: Optional[str] = Field(
        default="Sincronizando Motores...", description="Step-by-step progress message"
    )


class SimulationResponse(BaseModel):
    simulation_id: str
    status: SimulationStatus
    result: Optional[P10FinancialOutput] = None
    error: Optional[str] = None
