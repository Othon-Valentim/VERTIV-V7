"""
VERTIV V7 — Ingestion Router
Resilient provider routing with explicit production fallbacks.

Strategy:
1. If ZIP size > 1M tokens estimate → Force Gemini (only one with 2M context)
2. Try primary (Gemini, cheapest) first
3. If primary fails → use a configured real fallback only
4. If no real fallback exists → raise a clear production error
"""

import logging
from typing import Any, Dict, Optional

from .base import LLMProvider

logger = logging.getLogger("vertiv.providers.router")

# Rough estimate: 1 byte ≈ 0.25 tokens for mixed content (JSON + text)
BYTES_TO_TOKENS_RATIO = 0.25
CLAUDE_MAX_TOKENS = 1_000_000


class IngestionRouter:
    """Routes Data Room extraction to the optimal LLM provider."""

    def __init__(
        self,
        primary: LLMProvider,
        fallback: Optional[LLMProvider] = None,
    ) -> None:
        self.primary = primary
        self.fallback = fallback
        self._last_provider_used: Optional[str] = None

    @property
    def last_provider_used(self) -> Optional[str]:
        return self._last_provider_used

    def _estimate_tokens(self, content_bytes: int) -> int:
        """Estimate token count from byte size."""
        return int(content_bytes * BYTES_TO_TOKENS_RATIO)

    def _should_force_gemini(self, content_bytes: int) -> bool:
        """
        If content exceeds Claude's 1M token limit,
        force Gemini (2M context) — bypass Claude entirely.
        """
        estimated_tokens = self._estimate_tokens(content_bytes)
        if estimated_tokens > CLAUDE_MAX_TOKENS:
            logger.info(
                f"Content ~{estimated_tokens:,} tokens > Claude limit "
                f"({CLAUDE_MAX_TOKENS:,}). Forcing Gemini."
            )
            return True
        return False

    async def extract(
        self,
        raw_content: bytes,
        extraction_schema: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Route extraction to the optimal provider with fallback.

        Args:
            raw_content: Raw bytes from the ZIP Data Room
            extraction_schema: Pydantic-compatible schema dict

        Returns:
            Extracted structured data

        Raises:
            RuntimeError: If all providers fail
        """
        content_size = len(raw_content)
        estimated_tokens = self._estimate_tokens(content_size)

        logger.info(
            f"Routing extraction: {content_size:,} bytes, "
            f"~{estimated_tokens:,} tokens"
        )

        # Strategy 1: Force Gemini for large payloads
        if self._should_force_gemini(content_size):
            try:
                return await self._try_provider(
                    self.primary, raw_content, extraction_schema, fallback_allowed=False
                )
            except Exception as primary_error:
                raise RuntimeError(
                    f"Large payload requires gemini-compatible provider only. "
                    f"{self.primary.name} failed: {primary_error}"
                ) from primary_error

        # Strategy 2: Try primary (Gemini), fallback only to a real provider
        try:
            return await self._try_provider(
                self.primary, raw_content, extraction_schema, fallback_allowed=True
            )
        except Exception as primary_error:
            if self.fallback is None or getattr(self.fallback, "is_stub", False):
                raise RuntimeError(
                    "No production fallback provider configured for V7.0. "
                    f"Primary provider ({self.primary.name}) failed: {primary_error}"
                ) from primary_error

            logger.warning(
                f"Primary provider ({self.primary.name}) failed: {primary_error}. "
                f"Falling back to {self.fallback.name}."
            )
            try:
                return await self._try_provider(
                    self.fallback,
                    raw_content,
                    extraction_schema,
                    fallback_allowed=False,
                )
            except Exception as fallback_error:
                raise RuntimeError(
                    f"CRITICAL: All LLM providers failed.\n"
                    f"Primary ({self.primary.name}): {primary_error}\n"
                    f"Fallback ({self.fallback.name}): {fallback_error}"
                ) from fallback_error

    async def _try_provider(
        self,
        provider: LLMProvider,
        raw_content: bytes,
        extraction_schema: Dict[str, Any],
        fallback_allowed: bool = True,
    ) -> Dict[str, Any]:
        """Try a single provider with health check."""
        # Health check
        is_healthy = await provider.health_check()
        if not is_healthy:
            if fallback_allowed:
                raise ConnectionError(f"{provider.name} health check failed")
            else:
                raise RuntimeError(
                    f"{provider.name} health check failed and no fallback available"
                )

        # Extract
        logger.info(f"Extracting via {provider.name}...")
        result = await provider.extract_structured_data(raw_content, extraction_schema)
        self._last_provider_used = provider.name
        logger.info(f"Extraction complete via {provider.name}")
        return result


def create_default_router() -> IngestionRouter:
    """
    Create the default router with environment-driven provider selection.

    USE_MOCK=1 → MockLLMProvider (golden data, zero tokens, dry run)
    USE_MOCK=0 → Gemini only (Claude stub is excluded from production V7.0)
    """
    import os

    use_mock = os.getenv("USE_MOCK", "0") == "1"

    if use_mock:
        from .mock import MockLLMProvider

        logger.info(
            "🧪 USE_MOCK=1 → MockLLMProvider activated. "
            "Zero LLM tokens will be consumed."
        )
        mock = MockLLMProvider()
        return IngestionRouter(primary=mock, fallback=None)

    from .gemini import GeminiProvider

    logger.info("🚀 Production mode → Gemini only (Claude fallback disabled in V7.0)")
    return IngestionRouter(
        primary=GeminiProvider(),
        fallback=None,
    )
