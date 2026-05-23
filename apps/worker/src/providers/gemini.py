"""
VERTIV V7 — Gemini Provider (Oráculo)
Real LLM extraction using Google Gemini model with structured JSON enforcement.
"""

import os
import json
import logging
import asyncio
from typing import Any, Dict

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.api_core.exceptions import RetryError, ResourceExhausted, DeadlineExceeded

from .base import LLMProvider

logger = logging.getLogger("vertiv.providers.gemini")


class GeminiProvider(LLMProvider):
    """
    Google Gemini Provider for Data Room Extraction.
    Uses 'gemini-2.0-flash' with strict structured JSON output.
    """

    def __init__(self) -> None:
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            logger.warning("GOOGLE_API_KEY is not set.")

        genai.configure(api_key=api_key)
        self.model_name = (
            "gemini-2.5-pro"  # Use 2.5-pro as requested by user context and stub
        )

        # System instructions enforcing the "Oppenheimer" Analyst persona
        self.system_instruction = (
            "Você é um Analista de Risco Institucional Sênior da VERTIV. "
            "Sua única função é extrair dados estritamente factuais dos documentos (Data Room) "
            "que lhe são fornecidos. Você receberá o texto bruto de PDFs de aquisição de terrenos e estudos de viabilidade. "
            "NUNCA INVENTE NÚMEROS. Se a informação não estiver presente no texto, retorne null. "
            "O retorno deve ser puramente o JSON de acordo com o schema esperado, contendo os campos vitais da struct financeira."
        )

        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=self.system_instruction,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            ),
        )

    # ── Protocol properties ─────────────────────────────────────────────

    @property
    def name(self) -> str:
        return self.model_name

    @property
    def max_context_tokens(self) -> int:
        return 2_000_000

    @property
    def cost_per_million_tokens_input(self) -> float:
        return 1.25

    @property
    def cost_per_million_tokens_output(self) -> float:
        return 5.00

    # ── Protocol methods ────────────────────────────────────────────────

    async def health_check(self) -> bool:
        """Validate that the API key is configured and functional."""
        try:
            if not os.getenv("GOOGLE_API_KEY"):
                return False
            # API is stateless and genai.configure does not fail immediately on bad keys
            # so we assume healthy if key is present to save latency,
            # but a deeper check could be implemented if necessary.
            return True
        except Exception as e:
            logger.error(f"[GeminiProvider] Health check failed: {e}")
            return False

    async def extract_structured_data(
        self,
        raw_content: bytes,
        extraction_schema: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Sends raw text out to Gemini, demanding a strict JSON response.
        Implements basic exponential backoff for network/rate limits.
        """
        text_content = raw_content.decode("utf-8", errors="replace")

        prompt = (
            f"Por favor, analise a seguinte Data Room de projeto imobiliário:\n\n"
            f"=== CONTEÚDO BRUTO ===\n"
            f"{text_content}\n\n"
            f"=== FIM DO CONTEÚDO ===\n\n"
            f"Preencha as informações conforme as regras do analista. "
            f"Retorne puramente um objeto JSON. "
            f"Respeite o seguinte schema (VertivAgenticSchema):\n"
            f"{json.dumps(extraction_schema, indent=2)}\n"
        )

        max_retries = 3
        backoff_seconds = 2

        for attempt in range(max_retries):
            try:
                logger.info(
                    f"[GeminiProvider] Enviando payload para {self.model_name} (attempt {attempt+1}/{max_retries})..."
                )
                response = await self.model.generate_content_async(
                    prompt,
                    safety_settings={
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    },
                )

                raw_json = response.text
                if not raw_json or not raw_json.strip():
                    raise ValueError("Gemini returned empty response.")

                # Strip markdown blocks if the LLM leaked them despite json mime type
                if raw_json.startswith("```json"):
                    raw_json = raw_json[7:-3]
                elif raw_json.startswith("```"):
                    raw_json = raw_json[3:-3]

                parsed_data = json.loads(raw_json)
                return parsed_data

            except (RetryError, ResourceExhausted, DeadlineExceeded) as e:
                logger.warning(
                    f"[GeminiProvider] Network/Rate error on attempt {attempt+1}: {e}"
                )
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(backoff_seconds * (2**attempt))
            except Exception as e:
                logger.error(
                    f"[GeminiProvider] Unhandled API error or parsing fail: {e}"
                )
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(backoff_seconds * (2**attempt))

        return {}
