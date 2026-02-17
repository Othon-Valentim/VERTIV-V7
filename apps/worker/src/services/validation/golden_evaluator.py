"""
VERTIV V7 — Golden Evaluator
2-Step Hybrid Validation: Input MAPE + Impact (VPL) MAPE.

Step 1: Field-level comparison (MAPE <= 5% for numerics, exact for booleans)
Step 2: Run both inputs through Polars engine, compare VPL (MAPE <= 2%)

Returns accuracy_score (0-100) + validation_metrics JSONB.
"""

import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from decimal import Decimal

logger = logging.getLogger("vertiv.validation.golden")


def _to_comparable(val: Any) -> Any:
    """Convert Enum objects to their value for safe comparison."""
    if isinstance(val, Enum):
        return val.value
    return val


class GoldenEvaluator:
    """
    Compares AI-extracted Data Room inputs against historical V6 golden data.

    Usage:
        evaluator = GoldenEvaluator()
        score, metrics = evaluator.evaluate(ai_extracted, golden_reference)
    """

    # Field-level thresholds
    NUMERIC_MAPE_THRESHOLD: float = 0.05  # 5% for individual fields
    VPL_MAPE_THRESHOLD: float = 0.02  # 2% for VPL impact

    # Weights for final score
    WEIGHT_INPUTS: float = 0.40
    WEIGHT_IMPACT: float = 0.60

    def evaluate(
        self,
        ai_extracted: Dict[str, Any],
        golden_reference: Dict[str, Any],
        ai_vpl: Optional[float] = None,
        golden_vpl: Optional[float] = None,
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Full 2-step evaluation.

        Args:
            ai_extracted: AI-extracted input fields
            golden_reference: Historical V6 reference fields
            ai_vpl: VPL calculated from AI inputs (if available)
            golden_vpl: VPL from golden dataset

        Returns:
            (accuracy_score, validation_metrics)
        """
        # Step 1: Input-level comparison
        step1_score, step1_details = self.evaluate_step_1_inputs(
            ai_extracted, golden_reference
        )

        # Step 2: Impact comparison (VPL)
        step2_score, step2_details = self.evaluate_step_2_impact(ai_vpl, golden_vpl)

        # Composite score
        if ai_vpl is not None and golden_vpl is not None:
            accuracy_score = (
                step1_score * self.WEIGHT_INPUTS + step2_score * self.WEIGHT_IMPACT
            )
        else:
            # If no VPL comparison possible, use only inputs
            accuracy_score = step1_score

        validation_metrics = {
            "accuracy_score": round(accuracy_score, 2),
            "step_1_inputs": {
                "score": round(step1_score, 2),
                "weight": self.WEIGHT_INPUTS,
                "details": step1_details,
            },
            "step_2_impact": {
                "score": round(step2_score, 2),
                "weight": self.WEIGHT_IMPACT,
                "details": step2_details,
            },
        }

        logger.info(
            f"Golden Evaluation: score={accuracy_score:.1f}, "
            f"step1={step1_score:.1f}, step2={step2_score:.1f}"
        )

        return round(accuracy_score, 2), validation_metrics

    def evaluate_step_1_inputs(
        self,
        ai_data: Dict[str, Any],
        golden_data: Dict[str, Any],
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Step 1: Field-by-field comparison.

        Numeric fields: MAPE (Mean Absolute Percentage Error)
        Boolean/enum fields: exact match
        """
        numeric_errors: List[Dict[str, Any]] = []
        exact_errors: List[Dict[str, Any]] = []
        total_fields = 0
        passed_fields = 0

        # Skip meta-fields
        skip_fields = {
            "extraction_confidence",
            "normalization_logs",
            "id",
            "created_at",
            "updated_at",
        }

        for key, golden_val in golden_data.items():
            if key in skip_fields:
                continue
            if key not in ai_data:
                continue

            total_fields += 1
            ai_val = _to_comparable(ai_data[key])
            golden_val = _to_comparable(golden_val)

            # CRITICAL: Check bool BEFORE int/float because
            # isinstance(True, int) == True in Python!
            if isinstance(golden_val, bool):
                # Boolean: exact match
                if bool(ai_val) == golden_val:
                    passed_fields += 1
                else:
                    exact_errors.append(
                        {
                            "field": key,
                            "golden": golden_val,
                            "ai": ai_val,
                        }
                    )

            elif isinstance(golden_val, (int, float, Decimal)):
                # Numeric comparison via MAPE
                golden_num = float(golden_val)
                try:
                    ai_num = float(ai_val)
                except (ValueError, TypeError):
                    numeric_errors.append(
                        {
                            "field": key,
                            "golden": golden_num,
                            "ai": ai_val,
                            "error": "TYPE_MISMATCH",
                        }
                    )
                    continue

                if golden_num == 0:
                    if ai_num == 0:
                        passed_fields += 1
                    else:
                        numeric_errors.append(
                            {
                                "field": key,
                                "golden": golden_num,
                                "ai": ai_num,
                                "mape": float("inf"),
                            }
                        )
                else:
                    mape = abs(ai_num - golden_num) / abs(golden_num)
                    if mape <= self.NUMERIC_MAPE_THRESHOLD:
                        passed_fields += 1
                    else:
                        numeric_errors.append(
                            {
                                "field": key,
                                "golden": golden_num,
                                "ai": ai_num,
                                "mape": round(mape, 4),
                            }
                        )

            elif isinstance(golden_val, str):
                # String/enum: case-insensitive, whitespace-tolerant
                if str(ai_val).strip().upper() == str(golden_val).strip().upper():
                    passed_fields += 1
                else:
                    exact_errors.append(
                        {
                            "field": key,
                            "golden": golden_val,
                            "ai": ai_val,
                        }
                    )

        score = (passed_fields / total_fields * 100) if total_fields > 0 else 0

        return score, {
            "total_fields": total_fields,
            "passed_fields": passed_fields,
            "numeric_errors": numeric_errors,
            "exact_errors": exact_errors,
        }

    def evaluate_step_2_impact(
        self,
        ai_vpl: Optional[float],
        golden_vpl: Optional[float],
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Step 2: VPL Impact Comparison.

        Even if individual fields differ, what matters is the final VPL.
        Threshold: MAPE <= 2%.
        """
        if ai_vpl is None or golden_vpl is None:
            return 0.0, {
                "status": "SKIPPED",
                "reason": "VPL values not provided for comparison",
            }

        if golden_vpl == 0:
            if ai_vpl == 0:
                return 100.0, {
                    "status": "PASS",
                    "vpl_mape": 0.0,
                    "golden_vpl": 0.0,
                    "ai_vpl": 0.0,
                }
            else:
                return 0.0, {
                    "status": "FAIL",
                    "vpl_mape": float("inf"),
                    "golden_vpl": 0.0,
                    "ai_vpl": ai_vpl,
                }

        vpl_mape = abs(ai_vpl - golden_vpl) / abs(golden_vpl)

        if vpl_mape <= self.VPL_MAPE_THRESHOLD:
            # Within 2%: perfect score
            score = 100.0
            status = "PASS"
        elif vpl_mape <= 0.05:
            # 2-5%: partial credit
            score = 100.0 * (1 - (vpl_mape - self.VPL_MAPE_THRESHOLD) / 0.03)
            status = "PARTIAL"
        else:
            # > 5%: fail
            score = max(0.0, 100.0 * (1 - vpl_mape))
            status = "FAIL"

        return round(score, 2), {
            "status": status,
            "vpl_mape": round(vpl_mape, 4),
            "golden_vpl": golden_vpl,
            "ai_vpl": ai_vpl,
            "threshold": self.VPL_MAPE_THRESHOLD,
        }
