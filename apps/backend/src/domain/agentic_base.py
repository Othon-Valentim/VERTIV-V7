"""
VERTIV V7 — Agentic Base Schema
Self-Healing Pydantic Armor (Vacina Antigravity)

All engine inputs inherit from VertivAgenticSchema.
The @model_validator intercepts LLM hallucinated percentages
and auto-corrects them before they reach the Polars engine.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, model_validator
import logging

logger = logging.getLogger("vertiv.agentic")

# Confidence levels for extraction tracking
CONFIDENCE_EXTRACTED = "EXTRACTED"
CONFIDENCE_DEFAULTED = "DEFAULTED"
CONFIDENCE_COERCED = "COERCED"

# Self-healing thresholds: if value exceeds these, it was likely
# provided as a percentage (e.g., 6.0 instead of 0.06)
HEALING_RULES: Dict[str, float] = {
    "incc_annual_rate": 0.15,
    "ipca_annual_rate": 0.12,
    "permuta_physical_pct": 1.0,
    "volatility": 2.0,
    "risk_free_rate": 0.25,
    "market_vso_monthly": 1.0,
    "green_premium": 1.0,
    "brown_discount": 1.0,
}


class VertivAgenticSchema(BaseModel):
    """
    Base schema for all V7 agentic engine inputs.

    Features:
    - extraction_confidence: tracks how each field was obtained
    - normalization_logs: audit trail of self-healing corrections
    - @model_validator: auto-heals hallucinated percentages
    """

    extraction_confidence: Dict[str, str] = {}
    normalization_logs: List[Dict[str, Any]] = []

    @model_validator(mode="before")
    @classmethod
    def vacina_antigravity(cls, data: Any) -> Any:
        """
        Self-Healing Mathematical Vaccine.

        If the LLM returns percentages as whole numbers (e.g., 6.0 for 6%),
        this validator auto-divides by 100 and logs the correction.
        """
        if isinstance(data, dict):
            logs = data.get("normalization_logs", [])
            confidence = data.get("extraction_confidence", {})

            for field_name, threshold in HEALING_RULES.items():
                if field_name in data and data[field_name] is not None:
                    val = data[field_name]
                    try:
                        val = float(val)
                    except (ValueError, TypeError):
                        continue

                    if val > threshold:
                        corrected = val / 100.0
                        logs.append(
                            {
                                "field": field_name,
                                "original": val,
                                "corrected": corrected,
                                "rule": f"Value {val} > threshold {threshold}, divided by 100",
                                "severity": "WARNING",
                            }
                        )
                        confidence[field_name] = CONFIDENCE_COERCED
                        data[field_name] = corrected
                        logger.warning(
                            f"VACINA ANTIGRAVITY: {field_name} = {val} → {corrected} "
                            f"(threshold: {threshold})"
                        )

            data["normalization_logs"] = logs
            data["extraction_confidence"] = confidence

        return data

    class Config:
        extra = "allow"  # Allow extra fields from LLM extraction
