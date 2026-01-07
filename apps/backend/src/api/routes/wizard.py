"""
TIV Wizard API Routes
VERTIV v6.0 Global Edition

Complete 10-step methodology endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal

# Import engines
from src.engine.p2_economic import P2EconomicEngine
from src.engine.p4_vocation import (
    P4VocationEngine,
    P4VocationInput,
    ZoningType,
    InfrastructureLevel
)
from src.engine.p5_legal import P5LegalEngine, P5LegalInput
from src.engine.p6_p9_market import (
    P6DemandEngine,
    P6DemandInput,
    P7SupplyEngine,
    P7SupplyInput,
    P8AbsorptionEngine,
    P8AbsorptionInput,
    P9ValidationEngine,
    P9ValidationInput,
    IncomeSegment,
    CompetitorProject
)

router = APIRouter(prefix="/wizard", tags=["TIV Wizard"])


# ==================== P2: Economic Dynamics ====================

class P2Request(BaseModel):
    """P2 Analysis Request."""
    municipality: str
    municipality_population: int = Field(default=50000, gt=0)
    is_metropolitan: bool = False


@router.post("/p2/analyze")
async def analyze_p2_economic(request: P2Request):
    """
    P2: Dinâmica Econômica Analysis

    Calculates P2i-Lead score (0-50) based on:
    - Leading indicators: Employment, Credit, Confidence
    - Lagging indicators: IPCA, PIB, Selic
    - Contextual factors: Population, Metropolitan status

    Gate: P2i-Lead >= 28 for GO
    """
    engine = P2EconomicEngine()
    result = await engine.analyze(
        municipality=request.municipality,
        municipality_population=request.municipality_population,
        is_metropolitan=request.is_metropolitan
    )
    return result


# ==================== P4: Vocation Analysis ====================

class P4Request(BaseModel):
    """P4 Analysis Request."""
    municipality: str
    neighborhood: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Zoning
    zoning_type: str = "ZR2"  # ZR1, ZR2, ZR3, ZM, ZC, ZI, ZEIS, APA, APP
    max_height_floors: int = Field(default=4, ge=1, le=100)
    max_coverage_ratio: float = Field(default=0.6, ge=0.1, le=1.0)
    max_floor_area_ratio: float = Field(default=2.0, ge=0.1, le=10.0)

    # Centrality
    distance_city_center_km: float = Field(default=2.0, ge=0)
    distance_main_avenue_km: float = Field(default=0.5, ge=0)
    public_transport_available: bool = True
    distance_metro_station_km: Optional[float] = None

    # Infrastructure
    infrastructure_level: str = "COMPLETE"  # COMPLETE, PARTIAL, BASIC, NONE
    has_paved_access: bool = True
    has_water_network: bool = True
    has_sewage_network: bool = True
    has_electricity: bool = True
    has_gas_network: bool = False
    has_fiber_optic: bool = False

    # Land
    land_area_sqm: float = Field(default=5000, gt=0)
    land_price_per_sqm: float = Field(default=150.0, gt=0)
    target_segment: str = "MEDIO"


@router.post("/p4/analyze")
async def analyze_p4_vocation(request: P4Request):
    """
    P4: Vocação Imobiliária Analysis

    3-Pillar Attractiveness Matrix:
    - Pilar 1: Zoning & Potential (30%)
    - Pilar 2: Centrality & Accessibility (40%)
    - Pilar 3: Infrastructure (30%)

    Returns product recommendation and decision.
    """
    # Map string enums to actual enums
    try:
        zoning = ZoningType[request.zoning_type]
    except KeyError:
        zoning = ZoningType.ZR2

    try:
        infra_level = InfrastructureLevel[request.infrastructure_level]
    except KeyError:
        infra_level = InfrastructureLevel.COMPLETE

    input_data = P4VocationInput(
        municipality=request.municipality,
        neighborhood=request.neighborhood,
        latitude=request.latitude,
        longitude=request.longitude,
        zoning_type=zoning,
        max_height_floors=request.max_height_floors,
        max_coverage_ratio=request.max_coverage_ratio,
        max_floor_area_ratio=request.max_floor_area_ratio,
        distance_city_center_km=request.distance_city_center_km,
        distance_main_avenue_km=request.distance_main_avenue_km,
        public_transport_available=request.public_transport_available,
        distance_metro_station_km=request.distance_metro_station_km,
        infrastructure_level=infra_level,
        has_paved_access=request.has_paved_access,
        has_water_network=request.has_water_network,
        has_sewage_network=request.has_sewage_network,
        has_electricity=request.has_electricity,
        has_gas_network=request.has_gas_network,
        has_fiber_optic=request.has_fiber_optic,
        land_area_sqm=request.land_area_sqm,
        land_price_per_sqm=Decimal(str(request.land_price_per_sqm)),
        target_segment=request.target_segment
    )

    engine = P4VocationEngine()
    return engine.analyze(input_data)


# ==================== P5: Legal Due Diligence ====================

class P5Request(BaseModel):
    """P5 Analysis Request."""
    land_registration_number: str = Field(..., description="Matrícula do imóvel")
    municipality: str
    notary_office: str = Field(default="1º Ofício", description="Cartório de registro")

    # Ownership
    has_clear_title: bool = True
    is_registered: bool = True
    has_pending_lawsuits: bool = False
    has_liens: bool = False
    has_usufruct: bool = False

    # Environmental
    is_in_app: bool = False
    is_in_apa: bool = False
    is_in_reserve: bool = False
    has_contamination: bool = False
    requires_environmental_study: bool = False
    has_environmental_license: Optional[bool] = None

    # Urban
    complies_with_zoning: bool = True
    complies_with_master_plan: bool = True
    has_building_restrictions: bool = False
    has_heritage_protection: bool = False
    requires_eia_rima: bool = False

    # Fiscal
    has_iptu_debt: bool = False
    has_itr_debt: bool = False
    has_tax_liens: bool = False
    tax_debt_amount: float = 0.0

    # Judicial
    pending_lawsuits_count: int = 0
    has_adverse_possession_claims: bool = False
    has_expropriation_risk: bool = False
    has_neighborhood_disputes: bool = False

    # Documentation
    has_updated_registration: bool = True
    has_topographic_survey: bool = False
    has_georeferencing: bool = False


@router.post("/p5/analyze")
async def analyze_p5_legal(request: P5Request):
    """
    P5: Legal Due Diligence Analysis

    Binary Gate checking:
    - Ownership status
    - Environmental restrictions
    - Urban/Zoning compliance
    - Fiscal situation
    - Judicial issues

    Returns PASS/FAIL with detailed findings.
    """
    input_data = P5LegalInput(
        land_registration_number=request.land_registration_number,
        municipality=request.municipality,
        notary_office=request.notary_office,
        has_clear_title=request.has_clear_title,
        is_registered=request.is_registered,
        has_pending_lawsuits=request.has_pending_lawsuits,
        has_liens=request.has_liens,
        has_usufruct=request.has_usufruct,
        is_in_app=request.is_in_app,
        is_in_apa=request.is_in_apa,
        is_in_reserve=request.is_in_reserve,
        has_contamination=request.has_contamination,
        requires_environmental_study=request.requires_environmental_study,
        has_environmental_license=request.has_environmental_license,
        complies_with_zoning=request.complies_with_zoning,
        complies_with_master_plan=request.complies_with_master_plan,
        has_building_restrictions=request.has_building_restrictions,
        has_heritage_protection=request.has_heritage_protection,
        requires_eia_rima=request.requires_eia_rima,
        has_iptu_debt=request.has_iptu_debt,
        has_itr_debt=request.has_itr_debt,
        has_tax_liens=request.has_tax_liens,
        tax_debt_amount=request.tax_debt_amount,
        pending_lawsuits_count=request.pending_lawsuits_count,
        has_adverse_possession_claims=request.has_adverse_possession_claims,
        has_expropriation_risk=request.has_expropriation_risk,
        has_neighborhood_disputes=request.has_neighborhood_disputes,
        has_updated_registration=request.has_updated_registration,
        has_topographic_survey=request.has_topographic_survey,
        has_georeferencing=request.has_georeferencing
    )

    engine = P5LegalEngine()
    return engine.analyze(input_data)


# ==================== P6: Qualified Demand ====================

class P6Request(BaseModel):
    """P6 Analysis Request."""
    municipality: str
    influence_area_population: int = Field(default=50000, gt=0)
    average_household_income: float = Field(default=5000.0, gt=0)
    target_segment: str = "MEDIO"  # FAIXA_1, FAIXA_2, FAIXA_3, MEDIO, ALTO
    unit_price_min: float = Field(default=150000.0, gt=0)
    unit_price_max: float = Field(default=250000.0, gt=0)
    unit_type: str = "LOTE"


@router.post("/p6/analyze")
async def analyze_p6_demand(request: P6Request):
    """
    P6: Qualified Demand Analysis

    5-Stage Funnel:
    1. Total Families
    2. Income-Qualified
    3. Product-Fit
    4. Purchase Intent
    5. Effective Demand
    """
    try:
        segment = IncomeSegment[request.target_segment]
    except KeyError:
        segment = IncomeSegment.MEDIO

    input_data = P6DemandInput(
        municipality=request.municipality,
        influence_area_population=request.influence_area_population,
        average_household_income=Decimal(str(request.average_household_income)),
        target_segment=segment,
        unit_price_min=Decimal(str(request.unit_price_min)),
        unit_price_max=Decimal(str(request.unit_price_max)),
        unit_type=request.unit_type
    )

    engine = P6DemandEngine()
    return engine.analyze(input_data)


# ==================== P7: Supply Analysis ====================

class CompetitorInput(BaseModel):
    """Competitor project input."""
    name: str
    developer: str
    total_units: int
    units_sold: int
    units_available: int
    price_per_sqm: float
    launch_date: Optional[str] = None
    product_type: str = "LOTEAMENTO"


class P7Request(BaseModel):
    """P7 Analysis Request."""
    municipality: str
    influence_area_km: float = 5.0
    competitors: List[CompetitorInput] = []
    market_average_price_sqm: Optional[float] = None


@router.post("/p7/analyze")
async def analyze_p7_supply(request: P7Request):
    """
    P7: Supply & Market Analysis

    Analyzes:
    - Competitor inventory
    - Pricing benchmarks
    - Market saturation
    """
    competitors = [
        CompetitorProject(
            name=c.name,
            developer=c.developer,
            total_units=c.total_units,
            units_sold=c.units_sold,
            units_available=c.units_available,
            price_per_sqm=Decimal(str(c.price_per_sqm)),
            launch_date=c.launch_date,
            product_type=c.product_type
        )
        for c in request.competitors
    ]

    input_data = P7SupplyInput(
        municipality=request.municipality,
        influence_area_km=request.influence_area_km,
        competitors=competitors,
        market_average_price_sqm=Decimal(str(request.market_average_price_sqm)) if request.market_average_price_sqm else None
    )

    engine = P7SupplyEngine()
    return engine.analyze(input_data)


# ==================== P8: Absorption Analysis ====================

class P8Request(BaseModel):
    """P8 Analysis Request."""
    municipality: str
    project_units: int = Field(default=30, gt=0)
    project_price_avg: float = Field(default=180000.0, gt=0)
    qualified_demand: int = Field(default=200, gt=0)  # From P6
    active_inventory: int = Field(default=50, ge=0)  # From P7
    market_vso_monthly: float = Field(default=0.08, ge=0, le=1)


@router.post("/p8/analyze")
async def analyze_p8_absorption(request: P8Request):
    """
    P8: Sales Velocity (VSO) Analysis

    Calculates:
    - Monthly sales velocity
    - Absorption timeline
    - Demand/Supply ratio impact
    """
    input_data = P8AbsorptionInput(
        municipality=request.municipality,
        project_units=request.project_units,
        project_price_avg=Decimal(str(request.project_price_avg)),
        qualified_demand=request.qualified_demand,
        active_inventory=request.active_inventory,
        market_vso_monthly=request.market_vso_monthly
    )

    engine = P8AbsorptionEngine()
    return engine.analyze(input_data)


# ==================== P9: Strategic Validation ====================

class P9Request(BaseModel):
    """P9 Analysis Request."""
    municipality: str
    qualified_demand: int = Field(default=200, gt=0)
    active_inventory: int = Field(default=50, ge=0)
    competitors_count: int = Field(default=3, ge=0)
    projected_absorption_months: int = Field(default=24)
    project_units: int = Field(default=30, gt=0)
    project_price_sqm: float = Field(default=300.0, gt=0)
    market_price_sqm: float = Field(default=280.0, gt=0)


@router.post("/p9/analyze")
async def analyze_p9_validation(request: P9Request):
    """
    P9: Strategic Validation (Gate 4:1)

    Final market validation before P10:
    - 4:1 Demand:Supply ratio
    - Absorption timeline check
    - Price competitiveness
    """
    input_data = P9ValidationInput(
        municipality=request.municipality,
        qualified_demand=request.qualified_demand,
        active_inventory=request.active_inventory,
        competitors_count=request.competitors_count,
        projected_absorption_months=request.projected_absorption_months,
        project_units=request.project_units,
        project_price_sqm=Decimal(str(request.project_price_sqm)),
        market_price_sqm=Decimal(str(request.market_price_sqm))
    )

    engine = P9ValidationEngine()
    return engine.analyze(input_data)


# ==================== Wizard Session Management ====================

class WizardSessionCreate(BaseModel):
    """Create a new wizard session."""
    project_name: str
    municipality: str


class WizardStepSave(BaseModel):
    """Save step data to session."""
    session_id: str
    step: str  # p1, p2, p3, etc.
    data: dict


# In-memory session storage (would use Redis/DB in production)
_wizard_sessions = {}


@router.post("/session/create")
async def create_wizard_session(request: WizardSessionCreate):
    """Create a new wizard session."""
    import uuid
    session_id = str(uuid.uuid4())[:8].upper()

    _wizard_sessions[session_id] = {
        "id": session_id,
        "project_name": request.project_name,
        "municipality": request.municipality,
        "steps": {},
        "created_at": __import__("datetime").datetime.now().isoformat()
    }

    return {"session_id": session_id, "status": "created"}


@router.post("/session/save-step")
async def save_wizard_step(request: WizardStepSave):
    """Save step data to session."""
    if request.session_id not in _wizard_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    _wizard_sessions[request.session_id]["steps"][request.step] = request.data
    return {"status": "saved", "step": request.step}


@router.get("/session/{session_id}")
async def get_wizard_session(session_id: str):
    """Get wizard session data."""
    if session_id not in _wizard_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    return _wizard_sessions[session_id]
