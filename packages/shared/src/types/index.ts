/**
 * VERTIV v6.0 Shared Types
 * Mirror of apps/backend/src/domain/schemas.py
 */

// --- Enums ---

export enum ESGCertification {
  LEED = "LEED",
  BREEAM = "BREEAM",
  AQUA = "AQUA",
  WELL = "WELL",
  EDGE = "EDGE",
  NONE = "NONE",
}

export enum MarketCyclePhase {
  RECOVERY = "RECUPERACAO",
  EXPANSION = "EXPANSAO",
  DECELERATION = "DESACELERACAO",
  RECESSION = "RECESSAO",
}

export enum ProductType {
  LOTEAMENTO_ABERTO = "LOTEAMENTO_ABERTO",
  CONDOMINIO_FECHADO = "CONDOMINIO_FECHADO",
  VERTICAL_RESIDENCIAL = "VERTICAL_RESIDENCIAL",
  VERTICAL_COMERCIAL = "VERTICAL_COMERCIAL",
  MISTO = "MISTO",
}

export enum GoNoGoDecision {
  GO = "GO",
  NO_GO = "NO_GO",
  CAUTION = "CAUTION",
  HOLD = "HOLD",
}

// --- Models ---

export interface ESGAttributes {
  certification: ESGCertification;
  green_premium: number; // float
  brown_discount: number; // float
  carbon_footprint_tonnes?: number; // Optional[float]
}

// P1: Garimpo
export interface P1GarimpoInput {
  location_municipality: string;
  location_neighborhood: string;
  area_sqm: number;
  asking_price: string; // Decimal passed as string to preserve precision
}

export interface P1GarimpoOutput {
  cycle_phase: MarketCyclePhase;
  score_attractiveness: number;
  decision: GoNoGoDecision;
}

// P2: Dinamica Economica
export interface P2EconomicDynamicsOutput {
  p2i_lead_score: number;
  is_favorable: boolean;
}

// P3: Area de Influencia
export interface P3InfluenceAreaInput {
  latitude: number;
  longitude: number;
  buffer_radius_km?: number;
  isochrone_minutes?: number;
}

export interface P3InfluenceAreaOutput {
  population_total: number;
  average_income_brl: string; // Decimal
  polygon_geojson: Record<string, any>; // Dict
}

// P4: Vocacao
export interface P4VocationOutput {
  score_zoning: number;
  score_centrality: number;
  score_density: number;
  total_score: number;
  recommended_product: ProductType;
}

// P5: Legal
export interface P5LegalOutput {
  impediments: string[];
  has_environmental_restrictions: boolean;
  is_approved: boolean;
}

// P6: Demanda
export interface P6DemandOutput {
  families_total: number;
  income_bracket_target_min: string; // Decimal
  income_bracket_target_max: string; // Decimal
  qualified_demand_units: number;
}

// P7: Oferta
export interface P7SupplyOutput {
  competitors_count: number;
  active_inventory_units: number;
  average_price_sqm: string; // Decimal
}

// P8: Absorcao
export interface P8AbsorptionOutput {
  monthly_sales_velocity_units: number;
  projected_absorption_months: number;
}

// P9: Convalidacao
export interface P9ValidationOutput {
  gate_4_1_ratio: number;
  is_validated: boolean;
}

// P10: Financial
export interface P10FinancialInput {
  total_units: number;
  sales_price_avg: string; // Decimal
  construction_cost_total: string; // Decimal
  land_cost: string; // Decimal
  development_months: number;
}

export interface P10FinancialOutput {
  npv: string; // Decimal
  irr: number;
  roe: number;
  payback_months: number;
  exposure_max: string; // Decimal
  esg_adjusted_npv: string; // Decimal
  real_option_land_value?: number;
}

// Real Options
export interface RealOptionsInput {
  land_value_current: number;
  development_cost_forcing: number;
  time_to_permit_years: number;
  volatility?: number;
  risk_free_rate?: number;
}

// --- Aggregate ---

export interface ProjectTIV {
  id: string;
  name: string;
  esg: ESGAttributes;
  real_options?: RealOptionsInput;
  p1?: P1GarimpoOutput;
  p4?: P4VocationOutput;
  p10?: P10FinancialOutput;
  financial_input?: P10FinancialInput;
}
