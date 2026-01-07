"""
P4: Vocação Imobiliária - Real Estate Vocation Engine
VERTIV v6.0 Global Edition

Framework: Matriz de Atratividade 3 Pilares
- Pilar 1: Zoneamento & Potencial (30%)
- Pilar 2: Centralidade & Acessibilidade (40%)
- Pilar 3: Densidade & Infraestrutura (30%)

Reference: KB_CORE v6.0 Section 2.6 + Harvard ULI Framework
"""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from decimal import Decimal


class ZoningType(str, Enum):
    """Brazilian zoning classifications."""
    ZR1 = "ZR1"  # Residencial Unifamiliar
    ZR2 = "ZR2"  # Residencial Multifamiliar Baixa
    ZR3 = "ZR3"  # Residencial Multifamiliar Alta
    ZM = "ZM"    # Zona Mista
    ZC = "ZC"    # Zona Comercial
    ZI = "ZI"    # Zona Industrial
    ZEIS = "ZEIS"  # Zona Especial Interesse Social
    APA = "APA"  # Área de Proteção Ambiental
    APP = "APP"  # Área de Preservação Permanente


class InfrastructureLevel(str, Enum):
    """Infrastructure availability levels."""
    COMPLETE = "COMPLETE"  # All utilities available
    PARTIAL = "PARTIAL"    # Some utilities missing
    BASIC = "BASIC"        # Only water/electricity
    NONE = "NONE"          # Greenfield


class ProductType(str, Enum):
    """Recommended product types based on analysis."""
    LOTEAMENTO_ABERTO = "LOTEAMENTO_ABERTO"
    CONDOMINIO_FECHADO = "CONDOMINIO_FECHADO"
    VERTICAL_RESIDENCIAL = "VERTICAL_RESIDENCIAL"
    VERTICAL_COMERCIAL = "VERTICAL_COMERCIAL"
    MISTO = "MISTO"
    SENIOR_HOUSING = "SENIOR_HOUSING"
    STUDENT_HOUSING = "STUDENT_HOUSING"


class P4VocationInput(BaseModel):
    """Input parameters for P4 Vocation Analysis."""
    # Location
    municipality: str
    neighborhood: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Zoning
    zoning_type: ZoningType
    max_height_floors: int = Field(default=4, ge=1, le=100)
    max_coverage_ratio: float = Field(default=0.6, ge=0.1, le=1.0)  # Taxa de ocupação
    max_floor_area_ratio: float = Field(default=2.0, ge=0.1, le=10.0)  # Coeficiente aproveitamento

    # Centrality
    distance_city_center_km: float = Field(ge=0)
    distance_main_avenue_km: float = Field(ge=0)
    public_transport_available: bool = True
    distance_metro_station_km: Optional[float] = None

    # Infrastructure
    infrastructure_level: InfrastructureLevel = InfrastructureLevel.COMPLETE
    has_paved_access: bool = True
    has_water_network: bool = True
    has_sewage_network: bool = True
    has_electricity: bool = True
    has_gas_network: bool = False
    has_fiber_optic: bool = False

    # Context
    land_area_sqm: float = Field(gt=0)
    land_price_per_sqm: Decimal = Field(gt=0)
    target_segment: str = "MEDIO"  # ECONOMICO, MEDIO, ALTO


class P4VocationEngine:
    """
    P4 Real Estate Vocation Analysis Engine.

    Implements the 3-Pillar Attractiveness Matrix from TIV Methodology
    with Harvard ULI best practices integration.
    """

    # Product recommendation rules based on zoning and density
    PRODUCT_MATRIX = {
        ZoningType.ZR1: [ProductType.LOTEAMENTO_ABERTO, ProductType.CONDOMINIO_FECHADO],
        ZoningType.ZR2: [ProductType.CONDOMINIO_FECHADO, ProductType.VERTICAL_RESIDENCIAL],
        ZoningType.ZR3: [ProductType.VERTICAL_RESIDENCIAL, ProductType.MISTO],
        ZoningType.ZM: [ProductType.MISTO, ProductType.VERTICAL_RESIDENCIAL, ProductType.VERTICAL_COMERCIAL],
        ZoningType.ZC: [ProductType.VERTICAL_COMERCIAL, ProductType.MISTO],
        ZoningType.ZI: [],  # Not suitable for residential
        ZoningType.ZEIS: [ProductType.VERTICAL_RESIDENCIAL],  # Social housing only
        ZoningType.APA: [ProductType.LOTEAMENTO_ABERTO],  # Low density only
        ZoningType.APP: [],  # Not buildable
    }

    def calculate_zoning_score(self, input_data: P4VocationInput) -> dict:
        """
        Pilar 1: Zoneamento & Potencial Construtivo (30% weight)

        Evaluates:
        - Zoning compatibility (0-4)
        - Building potential (0-3)
        - Regulatory flexibility (0-3)
        """
        # Zoning Compatibility (0-4)
        if input_data.zoning_type in [ZoningType.APP, ZoningType.ZI]:
            zoning_compat = 0.0
        elif input_data.zoning_type == ZoningType.APA:
            zoning_compat = 2.0
        elif input_data.zoning_type == ZoningType.ZEIS:
            zoning_compat = 3.0
        else:
            zoning_compat = 4.0

        # Building Potential (0-3) based on FAR
        if input_data.max_floor_area_ratio >= 4.0:
            building_potential = 3.0
        elif input_data.max_floor_area_ratio >= 2.0:
            building_potential = 2.5
        elif input_data.max_floor_area_ratio >= 1.0:
            building_potential = 2.0
        else:
            building_potential = 1.0

        # Regulatory Flexibility (0-3) based on height and coverage
        flexibility = 0.0
        if input_data.max_height_floors >= 10:
            flexibility += 1.5
        elif input_data.max_height_floors >= 4:
            flexibility += 1.0

        if input_data.max_coverage_ratio >= 0.5:
            flexibility += 1.5
        elif input_data.max_coverage_ratio >= 0.3:
            flexibility += 1.0

        total = zoning_compat + building_potential + flexibility
        normalized = min(10.0, total)

        return {
            "score": round(normalized, 2),
            "max": 10,
            "weight": 0.30,
            "components": {
                "zoning_compatibility": round(zoning_compat, 2),
                "building_potential": round(building_potential, 2),
                "regulatory_flexibility": round(flexibility, 2)
            },
            "zoning_type": input_data.zoning_type.value,
            "max_far": input_data.max_floor_area_ratio,
            "max_height": input_data.max_height_floors
        }

    def calculate_centrality_score(self, input_data: P4VocationInput) -> dict:
        """
        Pilar 2: Centralidade & Acessibilidade (40% weight)

        Evaluates:
        - Distance to center (0-4)
        - Main axis proximity (0-3)
        - Public transport (0-3)
        """
        # Distance to City Center (0-4)
        if input_data.distance_city_center_km <= 1.0:
            center_score = 4.0
        elif input_data.distance_city_center_km <= 3.0:
            center_score = 3.0
        elif input_data.distance_city_center_km <= 5.0:
            center_score = 2.0
        elif input_data.distance_city_center_km <= 10.0:
            center_score = 1.0
        else:
            center_score = 0.5

        # Main Avenue Proximity (0-3)
        if input_data.distance_main_avenue_km <= 0.3:
            avenue_score = 3.0
        elif input_data.distance_main_avenue_km <= 0.8:
            avenue_score = 2.0
        elif input_data.distance_main_avenue_km <= 1.5:
            avenue_score = 1.0
        else:
            avenue_score = 0.5

        # Public Transport (0-3)
        transport_score = 0.0
        if input_data.public_transport_available:
            transport_score += 1.5
        if input_data.distance_metro_station_km is not None:
            if input_data.distance_metro_station_km <= 0.5:
                transport_score += 1.5
            elif input_data.distance_metro_station_km <= 1.0:
                transport_score += 1.0
            elif input_data.distance_metro_station_km <= 2.0:
                transport_score += 0.5

        total = center_score + avenue_score + transport_score
        normalized = min(10.0, total)

        return {
            "score": round(normalized, 2),
            "max": 10,
            "weight": 0.40,
            "components": {
                "distance_to_center": round(center_score, 2),
                "main_avenue_proximity": round(avenue_score, 2),
                "public_transport": round(transport_score, 2)
            },
            "distance_center_km": input_data.distance_city_center_km,
            "has_metro": input_data.distance_metro_station_km is not None
        }

    def calculate_infrastructure_score(self, input_data: P4VocationInput) -> dict:
        """
        Pilar 3: Densidade & Infraestrutura (30% weight)

        Evaluates:
        - Basic utilities (0-4)
        - Enhanced utilities (0-3)
        - Access quality (0-3)
        """
        # Basic Utilities (0-4)
        basic_score = 0.0
        if input_data.has_water_network:
            basic_score += 1.0
        if input_data.has_electricity:
            basic_score += 1.0
        if input_data.has_sewage_network:
            basic_score += 1.0
        if input_data.has_paved_access:
            basic_score += 1.0

        # Enhanced Utilities (0-3)
        enhanced_score = 0.0
        if input_data.has_gas_network:
            enhanced_score += 1.0
        if input_data.has_fiber_optic:
            enhanced_score += 1.0
        if input_data.infrastructure_level == InfrastructureLevel.COMPLETE:
            enhanced_score += 1.0

        # Access Quality (0-3) - based on infrastructure level
        if input_data.infrastructure_level == InfrastructureLevel.COMPLETE:
            access_score = 3.0
        elif input_data.infrastructure_level == InfrastructureLevel.PARTIAL:
            access_score = 2.0
        elif input_data.infrastructure_level == InfrastructureLevel.BASIC:
            access_score = 1.0
        else:
            access_score = 0.0

        total = basic_score + enhanced_score + access_score
        normalized = min(10.0, total)

        return {
            "score": round(normalized, 2),
            "max": 10,
            "weight": 0.30,
            "components": {
                "basic_utilities": round(basic_score, 2),
                "enhanced_utilities": round(enhanced_score, 2),
                "access_quality": round(access_score, 2)
            },
            "infrastructure_level": input_data.infrastructure_level.value,
            "utilities_available": {
                "water": input_data.has_water_network,
                "electricity": input_data.has_electricity,
                "sewage": input_data.has_sewage_network,
                "gas": input_data.has_gas_network,
                "fiber": input_data.has_fiber_optic
            }
        }

    def recommend_product(
        self,
        input_data: P4VocationInput,
        total_score: float
    ) -> dict:
        """
        Recommend optimal product type based on analysis.

        Uses Harvard ULI matrix for product-market fit.
        """
        # Get allowed products for zoning
        allowed_products = self.PRODUCT_MATRIX.get(input_data.zoning_type, [])

        if not allowed_products:
            return {
                "primary": None,
                "alternatives": [],
                "reason": f"Zoneamento {input_data.zoning_type.value} não permite desenvolvimento residencial.",
                "confidence": 0.0
            }

        # Score adjustments based on context
        recommendations = []

        for product in allowed_products:
            base_score = total_score

            # Adjust for land size
            if product == ProductType.LOTEAMENTO_ABERTO:
                if input_data.land_area_sqm >= 10000:
                    base_score += 1.0
                else:
                    base_score -= 1.0

            elif product == ProductType.VERTICAL_RESIDENCIAL:
                if input_data.max_height_floors >= 8:
                    base_score += 1.0
                if input_data.distance_city_center_km <= 3:
                    base_score += 0.5

            elif product == ProductType.CONDOMINIO_FECHADO:
                if 2000 <= input_data.land_area_sqm <= 20000:
                    base_score += 0.5

            elif product == ProductType.MISTO:
                if input_data.zoning_type == ZoningType.ZM:
                    base_score += 1.0

            recommendations.append({
                "product": product.value,
                "adjusted_score": round(base_score, 2)
            })

        # Sort by adjusted score
        recommendations.sort(key=lambda x: x["adjusted_score"], reverse=True)

        primary = recommendations[0] if recommendations else None
        alternatives = recommendations[1:3] if len(recommendations) > 1 else []

        # Calculate confidence
        if primary:
            confidence = min(1.0, primary["adjusted_score"] / 10.0)
        else:
            confidence = 0.0

        return {
            "primary": primary["product"] if primary else None,
            "primary_score": primary["adjusted_score"] if primary else 0,
            "alternatives": [alt["product"] for alt in alternatives],
            "confidence": round(confidence, 2),
            "all_options": recommendations
        }

    def analyze(self, input_data: P4VocationInput) -> dict:
        """
        Execute full P4 Vocation Analysis.

        Returns comprehensive analysis with 3-pillar scores,
        product recommendation, and decision.
        """
        # Calculate pillar scores
        zoning_result = self.calculate_zoning_score(input_data)
        centrality_result = self.calculate_centrality_score(input_data)
        infrastructure_result = self.calculate_infrastructure_score(input_data)

        # Weighted total (0-10 scale)
        total_score = (
            zoning_result["score"] * zoning_result["weight"] +
            centrality_result["score"] * centrality_result["weight"] +
            infrastructure_result["score"] * infrastructure_result["weight"]
        )

        # Normalize to 0-100 scale for consistency
        score_100 = total_score * 10

        # Product recommendation
        product_rec = self.recommend_product(input_data, total_score)

        # Decision logic
        if product_rec["primary"] is None:
            decision = "NO_GO"
            recommendation = "Zoneamento incompatível com desenvolvimento imobiliário."
        elif total_score >= 7.5:
            decision = "GO"
            recommendation = f"Excelente vocação para {product_rec['primary']}. Alta atratividade."
        elif total_score >= 6.0:
            decision = "GO"
            recommendation = f"Boa vocação para {product_rec['primary']}. Prosseguir com análise."
        elif total_score >= 4.5:
            decision = "CAUTION"
            recommendation = f"Vocação moderada para {product_rec['primary']}. Avaliar mitigações."
        else:
            decision = "HOLD"
            recommendation = "Baixa atratividade. Considerar outras oportunidades."

        return {
            "location": {
                "municipality": input_data.municipality,
                "neighborhood": input_data.neighborhood
            },
            "total_score": round(total_score, 2),
            "score_100": round(score_100, 2),
            "max_score": 10,
            "decision": decision,
            "recommendation": recommendation,
            "pillars": {
                "pilar_1_zoning": zoning_result,
                "pilar_2_centrality": centrality_result,
                "pilar_3_infrastructure": infrastructure_result
            },
            "product_recommendation": product_rec,
            "input_summary": {
                "land_area_sqm": input_data.land_area_sqm,
                "land_price_per_sqm": float(input_data.land_price_per_sqm),
                "zoning": input_data.zoning_type.value,
                "target_segment": input_data.target_segment
            }
        }
