"""
VERTIV V7 — Operation Level Triage
Determines if an ingestion can be autonomous or needs human review.

Levels:
- AUTONOMOUS_SENTENCED: score >= 92, no blocking errors → full auto
- PENDING_HUMAN_AUDIT: score 85-92 → human reviews before commit
- MANUAL_ASSISTED: score < 85 or blocking errors → human drives
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("vertiv.validation.triage")


# Operation levels matching data_room_ingestions.status CHECK constraint
AUTONOMOUS_SENTENCED = "AUTONOMOUS_SENTENCED"
PENDING_HUMAN_AUDIT = "PENDING_HUMAN_AUDIT"
MANUAL_ASSISTED = "MANUAL_ASSISTED"
KILLED = "KILLED"

# Thresholds
THRESHOLD_AUTONOMOUS: float = 92.0
THRESHOLD_AUDIT: float = 85.0


def determine_operation_level(
    accuracy_score: float,
    has_blocking_errors: bool = False,
    kill_reasons: Optional[List[str]] = None,
    normalization_logs: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Determine the operation level for a Data Room ingestion.

    Args:
        accuracy_score: 0-100 score from GoldenEvaluator
        has_blocking_errors: True if P5 flagged critical legal issues
        kill_reasons: List of reasons the project should be killed
        normalization_logs: Self-healing corrections applied

    Returns:
        One of: AUTONOMOUS_SENTENCED, PENDING_HUMAN_AUDIT,
                MANUAL_ASSISTED, KILLED
    """
    # Kill gate: immediate rejection
    if kill_reasons and len(kill_reasons) > 0:
        logger.warning(f"KILL GATE triggered: {kill_reasons}")
        return KILLED

    # Blocking errors: force manual regardless of score
    if has_blocking_errors:
        logger.warning(
            f"Blocking errors detected (score={accuracy_score:.1f}). "
            f"Forcing MANUAL_ASSISTED."
        )
        return MANUAL_ASSISTED

    # Check for excessive self-healing corrections
    critical_corrections = 0
    if normalization_logs:
        critical_corrections = sum(
            1 for log in normalization_logs if log.get("severity") == "WARNING"
        )

    # If too many corrections, downgrade confidence
    if critical_corrections >= 3:
        logger.warning(
            f"Excessive self-healing ({critical_corrections} corrections). "
            f"Downgrading to PENDING_HUMAN_AUDIT."
        )
        return PENDING_HUMAN_AUDIT

    # Score-based triage
    if accuracy_score >= THRESHOLD_AUTONOMOUS:
        logger.info(f"AUTONOMOUS: score={accuracy_score:.1f} >= {THRESHOLD_AUTONOMOUS}")
        return AUTONOMOUS_SENTENCED

    elif accuracy_score >= THRESHOLD_AUDIT:
        logger.info(
            f"AUDIT: {THRESHOLD_AUDIT} <= score={accuracy_score:.1f} "
            f"< {THRESHOLD_AUTONOMOUS}"
        )
        return PENDING_HUMAN_AUDIT

    else:
        logger.info(f"MANUAL: score={accuracy_score:.1f} < {THRESHOLD_AUDIT}")
        return MANUAL_ASSISTED
