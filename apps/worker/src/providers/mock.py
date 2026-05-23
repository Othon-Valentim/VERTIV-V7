"""
VERTIV V7 — Mock LLM Provider (Dry Run)
Returns golden dataset data directly — for E2E validation without real LLM tokens.

This provider bypasses actual LLM calls and returns pre-validated data
from benchmark_projects.json, allowing the full pipeline to run:
  UI → Worker → MockProvider → Polars → GoldenEvaluator → Triage

Gate 1 Quality Target: Score 100.0, VPL MAPE 0.00%

Activated via: USE_MOCK=1 (environment variable)
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, Optional

logger = logging.getLogger("vertiv.providers.mock")

# Realistic LLM thinking delay (seconds)
MOCK_THINKING_DELAY: float = 5.0


class MockLLMProvider:
    """
    Mock provider implementing the LLMProvider Protocol.

    Returns golden dataset data for testing the full E2E pipeline
    (Polars, GoldenEvaluator, Triage) without consuming LLM tokens.
    """

    def __init__(self) -> None:
        self._golden_data: Optional[list] = None

    # ── Protocol properties ─────────────────────────────────────────────

    @property
    def name(self) -> str:
        return "mock-golden-v7"

    @property
    def max_context_tokens(self) -> int:
        return 999_999_999  # Unlimited — it's a mock

    @property
    def cost_per_million_tokens_input(self) -> float:
        return 0.0  # Free — zero token consumption

    @property
    def cost_per_million_tokens_output(self) -> float:
        return 0.0  # Free — zero token consumption

    # ── Golden Data Loader ──────────────────────────────────────────────

    def _load_golden_data(self) -> list:
        """Load benchmark projects from golden dataset."""
        if self._golden_data is not None:
            return self._golden_data

        # Search for benchmark_projects.json relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(
                current_dir,
                "..",
                "..",
                "..",
                "..",
                "golden_dataset",
                "benchmark_projects.json",
            ),
            os.path.join(
                current_dir,
                "..",
                "..",
                "..",
                "..",
                "..",
                "golden_dataset",
                "benchmark_projects.json",
            ),
            # Absolute fallback for CI/CD
            os.path.join(os.getcwd(), "golden_dataset", "benchmark_projects.json"),
        ]

        for path in candidates:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                with open(abs_path, "r", encoding="utf-8") as f:
                    self._golden_data = json.load(f)
                logger.info(
                    f"[MockProvider] Loaded {len(self._golden_data)} golden "
                    f"projects from {abs_path}"
                )
                return self._golden_data

        raise FileNotFoundError(
            f"benchmark_projects.json not found. Searched: "
            f"{[os.path.abspath(c) for c in candidates]}"
        )

    # ── Protocol methods ────────────────────────────────────────────────

    async def health_check(self) -> bool:
        """Always healthy — it's a mock. Validates golden data is loadable."""
        try:
            self._load_golden_data()
            return True
        except FileNotFoundError:
            logger.error("[MockProvider] Health check FAILED — golden data not found")
            return False

    async def extract_structured_data(
        self,
        raw_content: bytes,
        extraction_schema: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Simulate LLM extraction with a realistic thinking delay.

        Returns golden data for the matching project (default: GD-PUB-001).
        The 5-second delay simulates real LLM processing time so the
        frontend polling and status updates work identically to production.
        """
        golden_projects = self._load_golden_data()

        # Try to match by dataset_id if provided in schema hints
        target_id: str = extraction_schema.get("dataset_id", "GD-PUB-001")

        logger.info(
            f"[MockProvider] Simulating LLM thinking for {target_id} "
            f"({MOCK_THINKING_DELAY}s delay)..."
        )

        # ── Simulate AI thinking time ───────────────────────────────────
        await asyncio.sleep(MOCK_THINKING_DELAY)

        # ── Find matching project ───────────────────────────────────────
        for project in golden_projects:
            if project.get("dataset_id") == target_id:
                logger.info(
                    f"[MockProvider] Returning golden data for {target_id} "
                    f"(project: {project.get('project_name', 'unknown')})"
                )
                return self._flatten_project(project)

        # Fallback: return GD-PUB-001 (Reserva do Horto / Cury SP)
        logger.warning(
            f"[MockProvider] No match for '{target_id}', "
            f"returning GD-PUB-001 as default"
        )
        return self._flatten_project(golden_projects[0])

    # ── Helpers ─────────────────────────────────────────────────────────

    def _flatten_project(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """
        Flatten nested project structure (p1, p2, p4, p5, p10, etc.)
        into a single dict suitable for engine inputs.

        This mirrors exactly what a real LLM would extract from a PDF,
        ensuring the Polars engine receives identical inputs.
        """
        flat: Dict[str, Any] = {
            "dataset_id": project.get("dataset_id"),
            "project_name": project.get("project_name"),
            "municipality": project.get("municipality"),
        }

        # Merge all pipeline sections
        for key in [
            "p1",
            "p2",
            "p3",
            "p4",
            "p5",
            "p6",
            "p7",
            "p8",
            "p10",
            "financial_input",
            "real_options",
            "esg",
        ]:
            section = project.get(key, {})
            if isinstance(section, dict):
                flat.update(section)

        return flat
