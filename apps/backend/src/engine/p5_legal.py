"""
P5: Legal & Restrições - Legal Due Diligence Engine
VERTIV v6.0 Global Edition

Framework: Binary Gate (PASS/FAIL)
Comprehensive legal due diligence checklist for Brazilian real estate.

Reference: KB_CORE v6.0 Section 2.7
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from dataclasses import dataclass
from datetime import datetime


class RiskLevel(str, Enum):
    """Risk severity levels."""

    CRITICAL = "CRITICAL"  # Blocks project entirely
    HIGH = "HIGH"  # Requires resolution before proceed
    MEDIUM = "MEDIUM"  # Can be mitigated
    LOW = "LOW"  # Informational


class CheckCategory(str, Enum):
    """Legal check categories."""

    OWNERSHIP = "OWNERSHIP"  # Titularidade
    ENVIRONMENTAL = "ENVIRONMENTAL"  # Ambiental
    URBAN = "URBAN"  # Urbanístico
    FISCAL = "FISCAL"  # Fiscal/Tributário
    JUDICIAL = "JUDICIAL"  # Judicial
    REGULATORY = "REGULATORY"  # Regulatório


class LegalCheckResult(BaseModel):
    """Result of a single legal check."""

    id: str
    category: CheckCategory
    description: str
    is_passed: bool
    risk_level: RiskLevel
    finding: Optional[str] = None
    recommendation: Optional[str] = None
    blocking: bool = False  # If True, blocks GO decision


class P5LegalInput(BaseModel):
    """Input parameters for P5 Legal Analysis."""

    # Property Identification
    land_registration_number: str = Field(..., description="Matrícula do imóvel")
    municipality: str
    notary_office: str = Field(..., description="Cartório de registro")

    # Ownership Status
    has_clear_title: bool = True
    is_registered: bool = True
    has_pending_lawsuits: bool = False
    has_liens: bool = False  # Ônus (hipoteca, penhora)
    has_usufruct: bool = False
    condominium_fraction: Optional[float] = None  # For apartment land

    # Environmental
    is_in_app: bool = False  # Área de Preservação Permanente
    is_in_apa: bool = False  # Área de Proteção Ambiental
    is_in_reserve: bool = False  # Reserva Legal
    has_contamination: bool = False
    requires_environmental_study: bool = False
    has_environmental_license: Optional[bool] = None

    # Urban/Zoning
    complies_with_zoning: bool = True
    complies_with_master_plan: bool = True  # Plano Diretor
    has_building_restrictions: bool = False
    has_heritage_protection: bool = False  # Tombamento
    requires_eia_rima: bool = False  # Estudo de Impacto Ambiental

    # Fiscal
    has_iptu_debt: bool = False
    has_itr_debt: bool = False  # Imposto Territorial Rural
    has_tax_liens: bool = False
    tax_debt_amount: float = 0.0

    # Judicial
    pending_lawsuits_count: int = 0
    has_adverse_possession_claims: bool = False  # Usucapião
    has_expropriation_risk: bool = False  # Desapropriação
    has_neighborhood_disputes: bool = False

    # Documentation
    has_updated_registration: bool = True
    has_topographic_survey: bool = False
    has_georeferencing: bool = False  # Required for rural > 25ha


class P5LegalEngine:
    """
    P5 Legal Due Diligence Engine.

    Implements comprehensive legal analysis for Brazilian real estate,
    covering ownership, environmental, urban, fiscal, and judicial aspects.

    Gate: Binary PASS/FAIL - Any CRITICAL issue blocks project.
    """

    def check_ownership(self, input_data: P5LegalInput) -> List[LegalCheckResult]:
        """Category 1: Ownership (Titularidade) checks."""
        results = []

        # Clear Title
        results.append(
            LegalCheckResult(
                id="OWN-001",
                category=CheckCategory.OWNERSHIP,
                description="Título de propriedade limpo e regular",
                is_passed=input_data.has_clear_title,
                risk_level=(
                    RiskLevel.CRITICAL
                    if not input_data.has_clear_title
                    else RiskLevel.LOW
                ),
                finding=(
                    None
                    if input_data.has_clear_title
                    else "Título com irregularidades identificadas"
                ),
                recommendation=(
                    None
                    if input_data.has_clear_title
                    else "Regularizar título antes de prosseguir"
                ),
                blocking=not input_data.has_clear_title,
            )
        )

        # Registration Status
        results.append(
            LegalCheckResult(
                id="OWN-002",
                category=CheckCategory.OWNERSHIP,
                description="Imóvel registrado em cartório",
                is_passed=input_data.is_registered,
                risk_level=(
                    RiskLevel.CRITICAL
                    if not input_data.is_registered
                    else RiskLevel.LOW
                ),
                finding=None if input_data.is_registered else "Imóvel não registrado",
                recommendation=(
                    None
                    if input_data.is_registered
                    else "Providenciar registro imobiliário"
                ),
                blocking=not input_data.is_registered,
            )
        )

        # Liens (Ônus)
        results.append(
            LegalCheckResult(
                id="OWN-003",
                category=CheckCategory.OWNERSHIP,
                description="Ausência de ônus (hipoteca, penhora, etc.)",
                is_passed=not input_data.has_liens,
                risk_level=RiskLevel.HIGH if input_data.has_liens else RiskLevel.LOW,
                finding=(
                    "Ônus identificados na matrícula" if input_data.has_liens else None
                ),
                recommendation=(
                    "Negociar baixa dos ônus" if input_data.has_liens else None
                ),
                blocking=False,  # Can be resolved
            )
        )

        # Usufruct
        results.append(
            LegalCheckResult(
                id="OWN-004",
                category=CheckCategory.OWNERSHIP,
                description="Ausência de usufruto",
                is_passed=not input_data.has_usufruct,
                risk_level=RiskLevel.HIGH if input_data.has_usufruct else RiskLevel.LOW,
                finding="Usufruto registrado" if input_data.has_usufruct else None,
                recommendation=(
                    "Verificar extinção ou renúncia do usufruto"
                    if input_data.has_usufruct
                    else None
                ),
                blocking=False,
            )
        )

        return results

    def check_environmental(self, input_data: P5LegalInput) -> List[LegalCheckResult]:
        """Category 2: Environmental (Ambiental) checks."""
        results = []

        # APP Check
        results.append(
            LegalCheckResult(
                id="ENV-001",
                category=CheckCategory.ENVIRONMENTAL,
                description="Não incide em Área de Preservação Permanente (APP)",
                is_passed=not input_data.is_in_app,
                risk_level=(
                    RiskLevel.CRITICAL if input_data.is_in_app else RiskLevel.LOW
                ),
                finding=(
                    "Imóvel total ou parcialmente em APP"
                    if input_data.is_in_app
                    else None
                ),
                recommendation=(
                    "APP não edificável - avaliar área efetiva"
                    if input_data.is_in_app
                    else None
                ),
                blocking=input_data.is_in_app,  # Critical block
            )
        )

        # APA Check
        results.append(
            LegalCheckResult(
                id="ENV-002",
                category=CheckCategory.ENVIRONMENTAL,
                description="Verificação de Área de Proteção Ambiental (APA)",
                is_passed=not input_data.is_in_apa
                or True,  # APA allows some development
                risk_level=RiskLevel.MEDIUM if input_data.is_in_apa else RiskLevel.LOW,
                finding=(
                    "Imóvel em APA - restrições aplicáveis"
                    if input_data.is_in_apa
                    else None
                ),
                recommendation=(
                    "Verificar restrições específicas da APA"
                    if input_data.is_in_apa
                    else None
                ),
                blocking=False,
            )
        )

        # Contamination
        results.append(
            LegalCheckResult(
                id="ENV-003",
                category=CheckCategory.ENVIRONMENTAL,
                description="Ausência de contaminação do solo",
                is_passed=not input_data.has_contamination,
                risk_level=(
                    RiskLevel.CRITICAL
                    if input_data.has_contamination
                    else RiskLevel.LOW
                ),
                finding=(
                    "Solo contaminado identificado"
                    if input_data.has_contamination
                    else None
                ),
                recommendation=(
                    "Remediação obrigatória antes do desenvolvimento"
                    if input_data.has_contamination
                    else None
                ),
                blocking=input_data.has_contamination,
            )
        )

        # Environmental License
        if input_data.requires_environmental_study:
            results.append(
                LegalCheckResult(
                    id="ENV-004",
                    category=CheckCategory.ENVIRONMENTAL,
                    description="Licenciamento ambiental",
                    is_passed=input_data.has_environmental_license == True,
                    risk_level=(
                        RiskLevel.HIGH
                        if not input_data.has_environmental_license
                        else RiskLevel.LOW
                    ),
                    finding=(
                        "Licença ambiental pendente"
                        if not input_data.has_environmental_license
                        else None
                    ),
                    recommendation=(
                        "Iniciar processo de licenciamento"
                        if not input_data.has_environmental_license
                        else None
                    ),
                    blocking=False,  # Can be obtained
                )
            )

        return results

    def check_urban(self, input_data: P5LegalInput) -> List[LegalCheckResult]:
        """Category 3: Urban/Zoning (Urbanístico) checks."""
        results = []

        # Zoning Compliance
        results.append(
            LegalCheckResult(
                id="URB-001",
                category=CheckCategory.URBAN,
                description="Conformidade com zoneamento municipal",
                is_passed=input_data.complies_with_zoning,
                risk_level=(
                    RiskLevel.CRITICAL
                    if not input_data.complies_with_zoning
                    else RiskLevel.LOW
                ),
                finding=(
                    "Uso pretendido não permitido pelo zoneamento"
                    if not input_data.complies_with_zoning
                    else None
                ),
                recommendation=(
                    "Verificar possibilidade de mudança de uso ou outro produto"
                    if not input_data.complies_with_zoning
                    else None
                ),
                blocking=not input_data.complies_with_zoning,
            )
        )

        # Master Plan
        results.append(
            LegalCheckResult(
                id="URB-002",
                category=CheckCategory.URBAN,
                description="Conformidade com Plano Diretor",
                is_passed=input_data.complies_with_master_plan,
                risk_level=(
                    RiskLevel.HIGH
                    if not input_data.complies_with_master_plan
                    else RiskLevel.LOW
                ),
                finding=(
                    "Restrições do Plano Diretor aplicáveis"
                    if not input_data.complies_with_master_plan
                    else None
                ),
                recommendation=(
                    "Consultar prefeitura para orientações"
                    if not input_data.complies_with_master_plan
                    else None
                ),
                blocking=False,
            )
        )

        # Heritage Protection
        results.append(
            LegalCheckResult(
                id="URB-003",
                category=CheckCategory.URBAN,
                description="Ausência de tombamento patrimonial",
                is_passed=not input_data.has_heritage_protection,
                risk_level=(
                    RiskLevel.HIGH
                    if input_data.has_heritage_protection
                    else RiskLevel.LOW
                ),
                finding=(
                    "Imóvel ou entorno tombado"
                    if input_data.has_heritage_protection
                    else None
                ),
                recommendation=(
                    "Verificar restrições junto ao IPHAN/órgão estadual"
                    if input_data.has_heritage_protection
                    else None
                ),
                blocking=False,
            )
        )

        # EIA/RIMA
        if input_data.requires_eia_rima:
            results.append(
                LegalCheckResult(
                    id="URB-004",
                    category=CheckCategory.URBAN,
                    description="Estudo de Impacto Ambiental (EIA/RIMA)",
                    is_passed=False,  # Needs to be conducted
                    risk_level=RiskLevel.HIGH,
                    finding="Projeto requer EIA/RIMA",
                    recommendation="Contratar consultoria ambiental para elaboração do estudo",
                    blocking=False,
                )
            )

        return results

    def check_fiscal(self, input_data: P5LegalInput) -> List[LegalCheckResult]:
        """Category 4: Fiscal/Tax checks."""
        results = []

        # IPTU Debt
        results.append(
            LegalCheckResult(
                id="FIS-001",
                category=CheckCategory.FISCAL,
                description="Quitação de IPTU",
                is_passed=not input_data.has_iptu_debt,
                risk_level=(
                    RiskLevel.MEDIUM if input_data.has_iptu_debt else RiskLevel.LOW
                ),
                finding=(
                    f"Débito de IPTU identificado: R$ {input_data.tax_debt_amount:,.2f}"
                    if input_data.has_iptu_debt
                    else None
                ),
                recommendation=(
                    "Negociar quitação ou parcelamento"
                    if input_data.has_iptu_debt
                    else None
                ),
                blocking=False,
            )
        )

        # ITR Debt (Rural)
        results.append(
            LegalCheckResult(
                id="FIS-002",
                category=CheckCategory.FISCAL,
                description="Quitação de ITR (se rural)",
                is_passed=not input_data.has_itr_debt,
                risk_level=(
                    RiskLevel.MEDIUM if input_data.has_itr_debt else RiskLevel.LOW
                ),
                finding=(
                    "Débito de ITR identificado" if input_data.has_itr_debt else None
                ),
                recommendation=(
                    "Regularizar situação junto à Receita Federal"
                    if input_data.has_itr_debt
                    else None
                ),
                blocking=False,
            )
        )

        # Tax Liens
        results.append(
            LegalCheckResult(
                id="FIS-003",
                category=CheckCategory.FISCAL,
                description="Ausência de penhora fiscal",
                is_passed=not input_data.has_tax_liens,
                risk_level=(
                    RiskLevel.HIGH if input_data.has_tax_liens else RiskLevel.LOW
                ),
                finding=(
                    "Penhora fiscal sobre o imóvel"
                    if input_data.has_tax_liens
                    else None
                ),
                recommendation=(
                    "Resolver pendência antes da aquisição"
                    if input_data.has_tax_liens
                    else None
                ),
                blocking=False,
            )
        )

        return results

    def check_judicial(self, input_data: P5LegalInput) -> List[LegalCheckResult]:
        """Category 5: Judicial checks."""
        results = []

        # Pending Lawsuits
        results.append(
            LegalCheckResult(
                id="JUD-001",
                category=CheckCategory.JUDICIAL,
                description="Ausência de ações judiciais",
                is_passed=input_data.pending_lawsuits_count == 0,
                risk_level=(
                    RiskLevel.HIGH
                    if input_data.pending_lawsuits_count > 0
                    else RiskLevel.LOW
                ),
                finding=(
                    f"{input_data.pending_lawsuits_count} ação(ões) judicial(is) identificada(s)"
                    if input_data.pending_lawsuits_count > 0
                    else None
                ),
                recommendation=(
                    "Analisar natureza e risco das ações"
                    if input_data.pending_lawsuits_count > 0
                    else None
                ),
                blocking=input_data.pending_lawsuits_count
                > 2,  # Block if many lawsuits
            )
        )

        # Adverse Possession
        results.append(
            LegalCheckResult(
                id="JUD-002",
                category=CheckCategory.JUDICIAL,
                description="Ausência de reivindicação de usucapião",
                is_passed=not input_data.has_adverse_possession_claims,
                risk_level=(
                    RiskLevel.CRITICAL
                    if input_data.has_adverse_possession_claims
                    else RiskLevel.LOW
                ),
                finding=(
                    "Reivindicação de usucapião identificada"
                    if input_data.has_adverse_possession_claims
                    else None
                ),
                recommendation=(
                    "Avaliar juridicamente antes de prosseguir"
                    if input_data.has_adverse_possession_claims
                    else None
                ),
                blocking=input_data.has_adverse_possession_claims,
            )
        )

        # Expropriation Risk
        results.append(
            LegalCheckResult(
                id="JUD-003",
                category=CheckCategory.JUDICIAL,
                description="Ausência de risco de desapropriação",
                is_passed=not input_data.has_expropriation_risk,
                risk_level=(
                    RiskLevel.CRITICAL
                    if input_data.has_expropriation_risk
                    else RiskLevel.LOW
                ),
                finding=(
                    "Risco de desapropriação identificado"
                    if input_data.has_expropriation_risk
                    else None
                ),
                recommendation=(
                    "Verificar decretos de utilidade pública"
                    if input_data.has_expropriation_risk
                    else None
                ),
                blocking=input_data.has_expropriation_risk,
            )
        )

        return results

    def analyze(self, input_data: P5LegalInput) -> dict:
        """
        Execute full P5 Legal Due Diligence.

        Returns comprehensive analysis with all checks,
        blocking issues, and final gate decision.
        """
        # Run all checks
        ownership_checks = self.check_ownership(input_data)
        environmental_checks = self.check_environmental(input_data)
        urban_checks = self.check_urban(input_data)
        fiscal_checks = self.check_fiscal(input_data)
        judicial_checks = self.check_judicial(input_data)

        all_checks = (
            ownership_checks
            + environmental_checks
            + urban_checks
            + fiscal_checks
            + judicial_checks
        )

        # Aggregate results
        total_checks = len(all_checks)
        passed_checks = sum(1 for c in all_checks if c.is_passed)
        failed_checks = total_checks - passed_checks
        blocking_issues = [c for c in all_checks if c.blocking]

        # Calculate scores by category
        category_scores = {}
        for category in CheckCategory:
            cat_checks = [c for c in all_checks if c.category == category]
            if cat_checks:
                cat_passed = sum(1 for c in cat_checks if c.is_passed)
                category_scores[category.value] = {
                    "passed": cat_passed,
                    "total": len(cat_checks),
                    "score": round(cat_passed / len(cat_checks) * 100, 1),
                }

        # Final decision (Binary Gate)
        if blocking_issues:
            decision = "NO_GO"
            is_approved = False
            recommendation = f"BLOQUEADO: {len(blocking_issues)} impedimento(s) crítico(s) identificado(s)."
        elif failed_checks > 3:
            decision = "HOLD"
            is_approved = False
            recommendation = (
                f"AGUARDAR: {failed_checks} pendências a resolver antes de prosseguir."
            )
        elif failed_checks > 0:
            decision = "CAUTION"
            is_approved = True  # Can proceed with caution
            recommendation = f"PROSSEGUIR COM RESSALVAS: {failed_checks} item(ns) requer(em) atenção."
        else:
            decision = "GO"
            is_approved = True
            recommendation = "APROVADO: Due diligence legal concluída sem impedimentos."

        # Audit Requirement Singularity v6.1.0: Log decisions to stdout
        print(
            f"[P5_LEGAL] GATE DECISION: {decision} | Approved: {is_approved} | Blocking: {len(blocking_issues)}"
        )

        return {
            "property": {
                "registration_number": input_data.land_registration_number,
                "municipality": input_data.municipality,
                "notary_office": input_data.notary_office,
            },
            "gate_result": {
                "decision": decision,
                "is_approved": is_approved,
                "recommendation": recommendation,
            },
            "summary": {
                "total_checks": total_checks,
                "passed": passed_checks,
                "failed": failed_checks,
                "blocking_issues": len(blocking_issues),
                "compliance_score": round(passed_checks / total_checks * 100, 1),
            },
            "category_scores": category_scores,
            "blocking_issues": [
                {
                    "id": c.id,
                    "description": c.description,
                    "finding": c.finding,
                    "recommendation": c.recommendation,
                }
                for c in blocking_issues
            ],
            "all_checks": [
                {
                    "id": c.id,
                    "category": c.category.value,
                    "description": c.description,
                    "is_passed": c.is_passed,
                    "risk_level": c.risk_level.value,
                    "finding": c.finding,
                    "recommendation": c.recommendation,
                    "blocking": c.blocking,
                }
                for c in all_checks
            ],
            "checks_by_category": {
                "ownership": [c.model_dump() for c in ownership_checks],
                "environmental": [c.model_dump() for c in environmental_checks],
                "urban": [c.model_dump() for c in urban_checks],
                "fiscal": [c.model_dump() for c in fiscal_checks],
                "judicial": [c.model_dump() for c in judicial_checks],
            },
            "analysis_timestamp": datetime.now().isoformat(),
        }
