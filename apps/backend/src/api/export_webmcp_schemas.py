"""
VERTIV V7 — WebMCP Schema Exporter
Pydantic → JSON Schema (Draft-07) for navigator.modelContext.registerTool()

This module introspects Pydantic models from the Diamond Core domain and
exports them as WebMCP-compatible tool definitions. Internal fields
(extraction_confidence, normalization_logs) are stripped from the output.

Usage:
    from src.api.export_webmcp_schemas import get_webmcp_tool_catalog
    catalog = get_webmcp_tool_catalog()
"""

from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel
import json
import logging

logger = logging.getLogger("vertiv.webmcp")

# ── Internal fields to strip from exported schemas ──────────────────────────
INTERNAL_FIELDS = frozenset(
    {
        "extraction_confidence",
        "normalization_logs",
    }
)

# Only expose tools that are backed by a real implementation today. The
# mutation tools below stay defined for future use, but are not published until
# their backend endpoints and persistence model exist.
SUPPORTED_TOOL_NAMES = frozenset(
    {
        "simulate_what_if",
        "highlight_pdf_evidence",
    }
)


def pydantic_to_webmcp_schema(
    model: Type[BaseModel],
    *,
    exclude_fields: Optional[frozenset] = None,
) -> Dict[str, Any]:
    """
    Convert a Pydantic model to a JSON Schema dict suitable for WebMCP registerTool().

    - Strips internal agentic fields (extraction_confidence, normalization_logs)
    - Converts Decimal fields to { type: "number" }
    - Preserves Field(description=...) metadata
    - Emits Draft-07 compatible schema
    """
    exclude = exclude_fields or INTERNAL_FIELDS

    # Generate the full JSON Schema from Pydantic
    raw_schema: Dict[str, Any] = model.model_json_schema(mode="serialization")

    # Strip internal fields from properties
    properties = raw_schema.get("properties", {})
    cleaned_properties: Dict[str, Any] = {}

    for field_name, field_schema in properties.items():
        if field_name in exclude:
            continue
        # Normalize Decimal → number (Pydantic may emit "string" for Decimal)
        cleaned_properties[field_name] = _normalize_field_schema(field_schema)

    # Rebuild required list without excluded fields
    raw_required = raw_schema.get("required", [])
    cleaned_required = [r for r in raw_required if r not in exclude]

    result: Dict[str, Any] = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": cleaned_properties,
    }

    if cleaned_required:
        result["required"] = cleaned_required

    # Carry over $defs if present (for nested models / enums)
    if "$defs" in raw_schema:
        result["$defs"] = raw_schema["$defs"]

    # Carry over title/description
    if "title" in raw_schema:
        result["title"] = raw_schema["title"]
    if "description" in raw_schema:
        result["description"] = raw_schema["description"]

    return result


def _normalize_field_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize individual field schemas for WebMCP compatibility.
    - Decimal (serialized as string by Pydantic) → number
    - anyOf with string/null for Decimal → number/null
    """
    if schema.get("type") == "string" and "decimal" in str(schema).lower():
        schema = {**schema, "type": "number"}

    # Handle anyOf patterns (Optional[Decimal] emits anyOf)
    if "anyOf" in schema:
        normalized_variants = []
        for variant in schema["anyOf"]:
            if variant.get("type") == "string" and "decimal" in str(variant).lower():
                normalized_variants.append({**variant, "type": "number"})
            else:
                normalized_variants.append(variant)
        schema = {**schema, "anyOf": normalized_variants}

    return schema


# ── Tool Catalog Definition ─────────────────────────────────────────────────


class WebMCPToolDef:
    """Definition of a single WebMCP tool for the catalog."""

    def __init__(
        self,
        name: str,
        description: str,
        input_model: Type[BaseModel],
        output_schema: Dict[str, Any],
        risk_level: str = "MEDIUM",
        request_user_interaction: bool = False,
    ) -> None:
        self.name = name
        self.description = description
        self.input_model = input_model
        self.output_schema = output_schema
        self.risk_level = risk_level
        self.request_user_interaction = request_user_interaction

    def to_dict(self) -> Dict[str, Any]:
        """Export as a WebMCP-compatible tool definition dict."""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": pydantic_to_webmcp_schema(self.input_model),
            "outputSchema": self.output_schema,
            "riskLevel": self.risk_level,
            "requestUserInteraction": self.request_user_interaction,
        }


# ── Input Models for WebMCP-specific tools ──────────────────────────────────


class SimulateWhatIfInput(BaseModel):
    """Recalculates VPL/TIR based on new premises WITHOUT saving to the database."""

    project_id: str
    total_units: Optional[int] = None
    sales_price_avg: Optional[float] = None
    construction_cost_total: Optional[float] = None
    land_cost: Optional[float] = None
    development_months: Optional[int] = None
    incc_annual_rate: Optional[float] = None
    ipca_annual_rate: Optional[float] = None
    wacc: Optional[float] = None


class HighlightPdfEvidenceInput(BaseModel):
    """Scrolls and focuses the PDF viewer on specific evidence."""

    page: int
    exact_text: str


class RegisterKillReasonInput(BaseModel):
    """Registers a fatal risk evidence in the proprietary cemetery."""

    category: str  # LEGAL, ENVIRONMENTAL, FINANCIAL, PHYSICAL
    citation: str
    source_document: Optional[str] = None
    page_number: Optional[int] = None


class OverrideLegalFlagInput(BaseModel):
    """Alters the status of legal liabilities on the property registration."""

    has_contamination: Optional[bool] = None
    has_liens: Optional[bool] = None
    has_adverse_possession: Optional[bool] = None
    justification: str


class ApproveCapitalSentenceInput(BaseModel):
    """Seals the viability and releases funds for the real estate operation."""

    project_id: str


# ── Catalog Builder ─────────────────────────────────────────────────────────


def _build_tool_catalog() -> List[WebMCPToolDef]:
    """Build the VERTIV WebMCP tool catalog."""
    return [
        WebMCPToolDef(
            name="simulate_what_if",
            description=(
                "Recalculates VPL/TIR based on new premises without saving to the "
                "database. Use this to run what-if scenarios on financial projections. "
                "The Polars engine on the backend performs all math — never calculate locally."
            ),
            input_model=SimulateWhatIfInput,
            output_schema={
                "type": "object",
                "properties": {
                    "new_vpl": {
                        "type": "number",
                        "description": "Recalculated NPV in BRL",
                    },
                    "new_irr": {
                        "type": "number",
                        "description": "Recalculated IRR as decimal",
                    },
                    "new_roe": {
                        "type": "number",
                        "description": "Recalculated ROE as decimal",
                    },
                    "payback_months": {"type": "integer"},
                    "exposure_max": {"type": "number"},
                },
            },
            risk_level="MEDIUM",
            request_user_interaction=False,
        ),
        WebMCPToolDef(
            name="highlight_pdf_evidence",
            description=(
                "Scrolls and focuses the PDF viewer on the problematic clause. "
                "Provide the page number and the exact text to highlight."
            ),
            input_model=HighlightPdfEvidenceInput,
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                },
            },
            risk_level="LOW",
            request_user_interaction=False,
        ),
        WebMCPToolDef(
            name="register_kill_reason",
            description=(
                "Registers a fatal risk evidence in the proprietary NO-GO cemetery. "
                "The agent MUST provide the exact clause_text and page_number from the "
                "document. This feeds the VERTIV proprietary moat at zero cost."
            ),
            input_model=RegisterKillReasonInput,
            output_schema={
                "type": "object",
                "properties": {
                    "saved_id": {"type": "string", "format": "uuid"},
                },
            },
            risk_level="HIGH",
            request_user_interaction=True,
        ),
        WebMCPToolDef(
            name="override_legal_flag",
            description=(
                "Alters the status of legal liabilities on the property registration "
                "(Matrícula). REQUIRES human confirmation via browser popup."
            ),
            input_model=OverrideLegalFlagInput,
            output_schema={
                "type": "object",
                "properties": {
                    "updated": {"type": "boolean"},
                },
            },
            risk_level="HIGH",
            request_user_interaction=True,
        ),
        WebMCPToolDef(
            name="approve_capital_sentence",
            description=(
                "Seals the viability study and releases funds for the real estate operation. "
                "This is a FATAL action — the AI compiles the final report but the browser "
                "FREEZES the agent and requires a physical mouse click from the human operator. "
                "NEVER attempt to bypass this confirmation."
            ),
            input_model=ApproveCapitalSentenceInput,
            output_schema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["GO"]},
                },
            },
            risk_level="FATAL",
            request_user_interaction=True,
        ),
    ]


def get_webmcp_tool_catalog() -> List[Dict[str, Any]]:
    """
    Returns the complete WebMCP tool catalog as a list of dicts
    ready for JSON serialization and navigator.modelContext.registerTool().
    """
    catalog = [
        tool
        for tool in _build_tool_catalog()
        if tool.name in SUPPORTED_TOOL_NAMES
    ]
    result = [tool.to_dict() for tool in catalog]
    logger.info(f"WebMCP catalog exported: {len(result)} tools")
    return result


def get_webmcp_tool_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single tool definition by name."""
    catalog = _build_tool_catalog()
    for tool in catalog:
        if tool.name == name:
            return tool.to_dict()
    return None


# ── CLI Entry Point (for manual inspection) ─────────────────────────────────

if __name__ == "__main__":
    import sys

    catalog = get_webmcp_tool_catalog()
    output = json.dumps(catalog, indent=2, ensure_ascii=False)
    print(output)

    if "--write" in sys.argv:
        out_path = "webmcp_schemas.json"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n✅ Written to {out_path}")
