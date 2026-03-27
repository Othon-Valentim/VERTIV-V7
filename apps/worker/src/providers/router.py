"""
VERTIV V7 — Ingestion Router
Resilient multi-provider routing with automatic fallback.

Strategy:
1. ZIP < 150k tokens  → GPT-5.4 (primary, fast + precise)
2. ZIP 150k–900k      → Claude Opus 4.6 (1M context)
3. ZIP > 900k tokens  → Gemini 2.5 Pro (2M context, force)
4. Any failure        → cascade fallback through remaining providers
5. All fail           → raise critical exception
"""

import logging
from typing import Any, Dict, Optional

from apps.worker.src.providers.base import LLMProvider

logger = logging.getLogger("vertiv.providers.router")

# Rough estimate: 1 byte ≈ 0.25 tokens for mixed content (JSON + text)
BYTES_TO_TOKENS_RATIO = 0.25

# Context window thresholds (tokens)
GPT_MAX_TOKENS = 150_000       # Use GPT-5.4 below this
CLAUDE_MAX_TOKENS = 900_000    # Use Claude Opus below this
GEMINI_MAX_TOKENS = 2_000_000  # Gemini 2.5 Pro ceiling


class IngestionRouter:
    """Routes Data Room extraction to the optimal LLM provider."""

    def __init__(
        self,
        gpt: LLMProvider,
        claude: LLMProvider,
        gemini: LLMProvider,
    ) -> None:
        self.gpt = gpt        # Primary: GPT-5.4 (fast, precise, 200k)
        self.claude = claude  # Mid-tier: Claude Opus 4.6 (1M context)
        self.gemini = gemini  # Heavy: Gemini 2.5 Pro (2M context)
        self._last_provider_used: Optional[str] = None
        # Legacy compatibility
        self.primary = gpt
        self.fallback = claude

    @property
    def last_provider_used(self) -> Optional[str]:
        return self._last_provider_used

    def _estimate_tokens(self, content_bytes: int) -> int:
        """Estimate token count from byte size."""
        return int(content_bytes * BYTES_TO_TOKENS_RATIO)

    def _select_provider_by_size(self, content_bytes: int) -> LLMProvider:
        """
        Select optimal provider based on estimated token count.
        - < 150k tokens  → GPT-5.4 (primary)
        - 150k–900k      → Claude Opus 4.6 (1M context)
        - > 900k tokens  → Gemini 2.5 Pro (2M context)
        """
        estimated_tokens = self._estimate_tokens(content_bytes)
        if estimated_tokens > CLAUDE_MAX_TOKENS:
            logger.info(
                f"~{estimated_tokens:,} tokens > Claude limit → forcing Gemini 2.5 Pro."
            )
            return self.gemini
        elif estimated_tokens > GPT_MAX_TOKENS:
            logger.info(
                f"~{estimated_tokens:,} tokens > GPT limit → routing to Claude Opus."
            )
            return self.claude
        else:
            logger.info(
                f"~{estimated_tokens:,} tokens → routing to GPT-5.4 (primary)."
            )
            return self.gpt

    def _get_fallback_chain(self, primary: LLMProvider) -> list:
        """Return fallback providers in order, excluding the primary."""
        all_providers = [self.gpt, self.claude, self.gemini]
        return [p for p in all_providers if p.name != primary.name]

    async def extract(
        self,
        raw_content: bytes,
        extraction_schema: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Route extraction to the optimal provider with cascade fallback.

        Strategy:
        1. Select primary provider based on content size
        2. Try primary
        3. On failure, cascade through remaining providers in order
        4. If all fail, raise critical exception

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

        # Select primary provider by content size
        primary = self._select_provider_by_size(content_size)
        fallbacks = self._get_fallback_chain(primary)

        errors = {}

        # Try primary
        try:
            result = await self._try_provider(
                primary, raw_content, extraction_schema, fallback_allowed=True
            )
            return result
        except Exception as e:
            errors[primary.name] = str(e)
            logger.warning(f"Primary ({primary.name}) failed: {e}. Trying fallbacks...")

        # Cascade through fallbacks
        for fallback in fallbacks:
            try:
                logger.info(f"Attempting fallback: {fallback.name}")
                result = await self._try_provider(
                    fallback, raw_content, extraction_schema, fallback_allowed=False
                )
                return result
            except Exception as e:
                errors[fallback.name] = str(e)
                logger.warning(f"Fallback ({fallback.name}) failed: {e}.")

        # All providers failed
        error_summary = "\n".join(
            [f"  {name}: {err}" for name, err in errors.items()]
        )
        raise RuntimeError(
            f"CRITICAL: All LLM providers failed.\n{error_summary}"
        )

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
    USE_MOCK=0 → GPT-5.4 (primary) + Claude Opus (mid) + Gemini 2.5 Pro (heavy)

    Routing strategy by content size:
    - < 150k tokens  → GPT-5.4
    - 150k–900k      → Claude Opus 4.6
    - > 900k tokens  → Gemini 2.5 Pro
    All with cascade fallback if primary fails.
    """
    import os

    use_mock = os.getenv("USE_MOCK", "0") == "1"

    if use_mock:
        from apps.worker.src.providers.mock import MockLLMProvider

        logger.info(
            "🧪 USE_MOCK=1 → MockLLMProvider activated. "
            "Zero LLM tokens will be consumed."
        )
        mock = MockLLMProvider()
        return IngestionRouter(gpt=mock, claude=mock, gemini=mock)

    from apps.worker.src.providers.openai import OpenAIProvider
    from apps.worker.src.providers.claude import ClaudeProvider
    from apps.worker.src.providers.gemini import GeminiProvider

    logger.info(
        "🚀 Production mode → GPT-5.4 (primary) + "
        "Claude Opus 4.6 (mid) + Gemini 2.5 Pro (heavy)"
    )
    return IngestionRouter(
        gpt=OpenAIProvider(),
        claude=ClaudeProvider(),
        gemini=GeminiProvider(),
    )
