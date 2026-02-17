"""
VERTIV V7 — LLM Provider Protocol
Runtime-checkable protocol for multi-provider LLM routing.
"""

from typing import Any, Dict, Protocol, runtime_checkable


@runtime_checkable
class LLMProvider(Protocol):
    """Protocol for LLM providers used in Data Room ingestion."""

    @property
    def name(self) -> str:
        """Provider name for logging."""
        ...

    @property
    def max_context_tokens(self) -> int:
        """Maximum context window in tokens."""
        ...

    @property
    def cost_per_million_tokens_input(self) -> float:
        """Cost per million input tokens in USD."""
        ...

    @property
    def cost_per_million_tokens_output(self) -> float:
        """Cost per million output tokens in USD."""
        ...

    async def health_check(self) -> bool:
        """Check if the provider is available."""
        ...

    async def extract_structured_data(
        self,
        raw_content: bytes,
        extraction_schema: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Extract structured data from raw Data Room content.

        Args:
            raw_content: Raw bytes from the ZIP file
            extraction_schema: Pydantic-compatible schema dict

        Returns:
            Extracted and structured data as a dict
        """
        ...
