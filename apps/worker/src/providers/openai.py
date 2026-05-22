"""
VERTIV V7 — OpenAI Provider (GPT-5.4)
Primary extraction engine. Fast, precise, cost-effective for standard payloads.
"""

import os
import json
import logging
import asyncio
from typing import Any, Dict

from apps.worker.src.providers.base import LLMProvider

logger = logging.getLogger("vertiv.providers.openai")

SYSTEM_INSTRUCTION = (
    "Você é um Analista de Risco Institucional Sênior da VERTIV. "
    "Sua única função é extrair dados estritamente factuais dos documentos (Data Room) "
    "que lhe são fornecidos. Você receberá o texto bruto de PDFs de aquisição de terrenos "
    "e estudos de viabilidade. "
    "NUNCA INVENTE NÚMEROS. Se a informação não estiver presente no texto, retorne null. "
    "O retorno deve ser puramente o JSON de acordo com o schema esperado, "
    "contendo os campos vitais da struct financeira."
)


class OpenAIProvider(LLMProvider):
    """
    OpenAI GPT-5.4 Provider for Data Room Extraction.
    Primary provider — optimal for payloads up to 150k tokens.
    Uses structured JSON output mode for deterministic parsing.
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-5.4")
        if not self.api_key:
            logger.warning("[OpenAIProvider] OPENAI_API_KEY is not set.")

    # ── Protocol properties ─────────────────────────────────────────────

    @property
    def name(self) -> str:
        return self.model_name

    @property
    def max_context_tokens(self) -> int:
        return 200_000

    @property
    def cost_per_million_tokens_input(self) -> float:
        return 2.50  # USD per million input tokens

    @property
    def cost_per_million_tokens_output(self) -> float:
        return 10.00  # USD per million output tokens

    # ── Protocol methods ────────────────────────────────────────────────

    async def health_check(self) -> bool:
        """Validate API key presence."""
        try:
            return bool(self.api_key)
        except Exception as e:
            logger.error(f"[OpenAIProvider] Health check failed: {e}")
            return False

    async def extract_structured_data(
        self,
        raw_content: bytes,
        extraction_schema: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Extract structured data via GPT-5.4 with JSON mode enforcement.
        Implements exponential backoff for rate limits.
        """
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ImportError(
                "openai package not installed. Run: pip install openai"
            )

        client = AsyncOpenAI(api_key=self.api_key)
        text_content = raw_content.decode("utf-8", errors="replace")

        prompt = (
            f"Analise a seguinte Data Room de projeto imobiliário:\n\n"
            f"=== CONTEÚDO BRUTO ===\n"
            f"{text_content}\n\n"
            f"=== FIM DO CONTEÚDO ===\n\n"
            f"Extraia as informações conforme as regras do analista sênior VERTIV. "
            f"Retorne puramente um objeto JSON válido.\n"
            f"Schema esperado (VertivAgenticSchema):\n"
            f"{json.dumps(extraction_schema, indent=2)}\n"
        )

        max_retries = 3
        backoff_seconds = 2

        for attempt in range(max_retries):
            try:
                logger.info(
                    f"[OpenAIProvider] Enviando para {self.model_name} "
                    f"(attempt {attempt+1}/{max_retries})..."
                )

                response = await client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": SYSTEM_INSTRUCTION},
                        {"role": "user", "content": prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0,  # Deterministic — critical for financial extraction
                    max_tokens=8192,
                )

                raw_json = response.choices[0].message.content
                if not raw_json or not raw_json.strip():
                    raise ValueError("[OpenAIProvider] Empty response received.")

                parsed_data = json.loads(raw_json)
                logger.info(f"[OpenAIProvider] Extraction complete via {self.model_name}.")
                return parsed_data

            except Exception as e:
                logger.warning(
                    f"[OpenAIProvider] Error on attempt {attempt+1}: {e}"
                )
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(backoff_seconds * (2 ** attempt))

        return {}
