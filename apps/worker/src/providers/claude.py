"""
VERTIV V7 — Claude Provider placeholder.

Claude is intentionally not part of the V7.0 production fallback path until a
real Anthropic SDK implementation is added and covered by tests.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger("vertiv.providers.claude")


class ClaudeProvider:
    """Non-production placeholder for future Anthropic extraction."""

    is_stub = True

    @property
    def name(self) -> str:
        return "claude-4.6-sonnet"

    @property
    def max_context_tokens(self) -> int:
        return 1_000_000  # 1M tokens

    @property
    def cost_per_million_tokens_input(self) -> float:
        return 5.00  # USD per million input tokens

    @property
    def cost_per_million_tokens_output(self) -> float:
        return 25.00  # USD per million output tokens

    async def health_check(self) -> bool:
        """Claude is not production-ready in V7.0."""
        logger.info("ClaudeProvider is disabled for V7.0 production routing.")
        return False

    async def extract_structured_data(
        self,
        raw_content: bytes,
        extraction_schema: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Extract structured data using Claude 4.6 Sonnet.

        Uses tool_use mode with Pydantic schema enforcement.
        """
        logger.info(
            f"Claude extraction: {len(raw_content)} bytes, "
            f"schema keys: {list(extraction_schema.keys())}"
        )

        raise RuntimeError(
            "ClaudeProvider is a non-production placeholder in V7.0. "
            "Configure Gemini for USE_MOCK=0 or implement Anthropic SDK support."
        )
