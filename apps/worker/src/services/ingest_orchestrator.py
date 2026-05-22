"""
VERTIV V7 — Ingestion Orchestrator
The spine that connects ZIP upload to final triage.

Pipeline:
  ZIP → Download → Extract text → LLM Extraction → Pydantic Validation
    → Polars Calculation (P1→P10 + CashFlow + RealOptions)
    → GoldenEvaluator (if legacy_simulation_id)
    → Triage → Update DB status
"""

import json
import logging
import os
import sys
import traceback
import zipfile
import io
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

from pydantic import ValidationError
from supabase import Client

logger = logging.getLogger("vertiv.worker.orchestrator")

# Resolve backend path for engine imports
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", ".."))
backend_path = os.path.join(root_dir, "apps", "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)


class IngestionOrchestrator:
    """Orchestrates the full Data Room ingestion pipeline."""

    def __init__(self, supabase_client: Client) -> None:
        self.db = supabase_client

    def _update_status(
        self, ingestion_id: str, status: str, **extra_fields: Any
    ) -> None:
        """Update ingestion record status in Supabase."""
        data: Dict[str, Any] = {"status": status}
        data.update(extra_fields)
        try:
            self.db.table("data_room_ingestions").update(data).eq(
                "id", ingestion_id
            ).execute()
            logger.info(f"[{ingestion_id[:8]}] Status → {status}")
        except Exception as e:
            logger.error(f"DB update failed for {ingestion_id}: {e}")

    def _download_zip(self, storage_url: str) -> bytes:
        """Download ZIP from Supabase Storage."""
        # storage_url format: "data-rooms/{user_id}/{ingestion_id}/{filename}"
        bucket_name = storage_url.split("/")[0]
        file_path = "/".join(storage_url.split("/")[1:])
        response = self.db.storage.from_(bucket_name).download(file_path)
        logger.info(f"Downloaded {len(response)} bytes from {storage_url}")
        return response

    def _extract_text_from_zip(self, zip_bytes: bytes) -> str:
        """Extract all readable text from a ZIP file."""
        texts: List[str] = []
        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                name_lower = info.filename.lower()
                # Read text-like files
                if name_lower.endswith((".txt", ".csv", ".json", ".md", ".xml")):
                    try:
                        content = z.read(info.filename).decode(
                            "utf-8", errors="replace"
                        )
                        texts.append(f"=== {info.filename} ===\n{content}\n")
                    except Exception as e:
                        logger.warning(f"Could not read {info.filename}: {e}")
                elif name_lower.endswith(".pdf"):
                    try:
                        import fitz  # PyMuPDF

                        pdf_bytes = z.read(info.filename)
                        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                        pdf_text = f"=== {info.filename} ===\n"
                        for page in doc:
                            pdf_text += page.get_text() + "\n"
                        texts.append(pdf_text)
                    except ImportError:
                        logger.error("PyMuPDF (fitz) is not installed.")
                    except Exception as e:
                        logger.warning(f"Could not read PDF {info.filename}: {e}")

        combined = "\n".join(texts)
        logger.info(f"Extracted {len(combined)} chars from ZIP ({len(texts)} files)")
        return combined

    def _run_polars_engines(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the Diamond Core: P1→P10, CashFlow, RealOptions."""
        from src.engine.cashflow import CashFlowEngine
        from src.engine.real_options import RealOptionsEngine
        from vertiv.biz import tropicalize

        def sf(v: Any) -> float:
            """Safe float conversion."""
            try:
                val = float(v) if v is not None else 0.0
                import math

                return 0.0 if (math.isnan(val) or math.isinf(val)) else val
            except (ValueError, TypeError):
                return 0.0

        # Extract key financial inputs from the flattened data
        land_cost = sf(
            extracted_data.get("asking_price", extracted_data.get("land_cost", 0))
        )
        area_sqm = sf(
            extracted_data.get("area_sqm", extracted_data.get("land_area_sqm", 5000))
        )
        total_units = int(sf(extracted_data.get("total_units", 200)))
        sales_price_avg = sf(
            extracted_data.get(
                "sales_price_avg", extracted_data.get("unit_price_avg", 344700)
            )
        )
        construction_cost_total = sf(
            extracted_data.get("construction_cost_total", land_cost * 3)
        )
        dev_months = int(sf(extracted_data.get("development_months", 36)))
        incc_rate = sf(extracted_data.get("incc_annual_rate", 0.05))
        ipca_rate = sf(extracted_data.get("ipca_annual_rate", 0.045))
        use_ret = bool(extracted_data.get("use_ret_taxation", True))
        permuta_pct = sf(extracted_data.get("permuta_physical_pct", 0))
        funding_model = str(extracted_data.get("funding_model", "SBPE"))

        # WACC with ESG adjustment
        base_wacc = tropicalize("WACC_ANNUAL", 0.145)
        greenium = sf(extracted_data.get("green_premium", 0.0))
        brown_discount = sf(extracted_data.get("brown_discount", 0.0))
        adjusted_wacc = base_wacc - greenium + brown_discount

        logger.info(
            f"Diamond Core inputs: units={total_units}, price={sales_price_avg:,.0f}, "
            f"cost={construction_cost_total:,.0f}, WACC={adjusted_wacc:.2%}"
        )

        # CashFlow Engine
        cf_engine = CashFlowEngine(months=dev_months + 24)
        cf_results = cf_engine.calculate_project_cashflow(
            units=total_units,
            avg_price=sales_price_avg,
            cost_total=construction_cost_total,
            start_sales_month=6,
            wacc_annual=adjusted_wacc,
            use_ret=use_ret,
            permuta_pct=permuta_pct,
            funding_model=funding_model,
            incc_annual=incc_rate,
            ipca_annual=ipca_rate,
        )
        metrics = cf_results["metrics"]
        cashflow_data = cf_results.get("dataframe", [])
        cashflow_series = [row.get("net_cash_flow", 0) for row in cashflow_data]

        dcf_npv = sf(metrics["npv"])
        irr_val = sf(metrics.get("irr_annual", metrics.get("irr", 0)))

        # Dynamic metrics
        from core.main import (
            calculate_roe,
            calculate_payback_months,
            calculate_max_exposure,
        )

        roe_val = calculate_roe(dcf_npv, land_cost)
        payback = calculate_payback_months(cashflow_series)
        max_exp = calculate_max_exposure(cashflow_series)

        # Real Options
        ro_value = 0.0
        volatility = sf(extracted_data.get("volatility", 0.25))
        risk_free = sf(extracted_data.get("risk_free_rate", 0.1175))
        time_permit = sf(extracted_data.get("time_to_permit_years", 1.5))
        if land_cost > 0:
            try:
                ro_value = sf(
                    RealOptionsEngine.calculate_land_option_value(
                        land_value_current=land_cost,
                        development_cost=construction_cost_total,
                        time_to_permit_years=time_permit,
                        volatility=volatility,
                        risk_free_rate=risk_free,
                    )
                )
            except Exception as e:
                logger.warning(f"RealOptions calc failed: {e}")

        final_npv = dcf_npv + ro_value
        is_viable = irr_val > (adjusted_wacc * 100)

        results = {
            "npv": round(dcf_npv, 2),
            "irr": round(irr_val, 4),
            "roe": round(roe_val, 4),
            "payback_months": payback,
            "exposure_max": round(max_exp, 2),
            "esg_adjusted_npv": round(final_npv, 2),
            "real_option_land_value": round(ro_value, 2),
            "is_viable": is_viable,
            "total_units": total_units,
            "sales_price_avg": sales_price_avg,
            "construction_cost_total": construction_cost_total,
            "wacc_used": round(adjusted_wacc, 4),
        }

        logger.info(
            f"Diamond Core output: VPL={dcf_npv:,.2f}, TIR={irr_val:.2f}%, "
            f"ROE={roe_val:.2%}, Payback={payback}mo, Viable={is_viable}"
        )
        return results

    def _run_golden_evaluation(
        self,
        extracted_data: Dict[str, Any],
        legacy_simulation_id: str,
    ) -> Tuple[float, Dict[str, Any]]:
        """Run GoldenEvaluator against historical V6 data."""
        from .validation.golden_evaluator import GoldenEvaluator

        # Fetch golden data
        response = (
            self.db.table("golden_simulations")
            .select("simulation_data")
            .eq("dataset_id", legacy_simulation_id)
            .execute()
        )

        if not response.data or len(response.data) == 0:
            logger.warning(f"No golden data for {legacy_simulation_id}")
            return 100.0, {"note": "No golden data available for comparison"}

        golden_data = response.data[0].get("simulation_data", {})
        evaluator = GoldenEvaluator()
        score, details = evaluator.evaluate_step_1_inputs(extracted_data, golden_data)

        logger.info(f"GoldenEvaluator score: {score:.1f}")
        return score, details

    async def process(
        self,
        ingestion_id: str,
        storage_url: str,
        legacy_simulation_id: Optional[str] = None,
        use_mock: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute the full ingestion pipeline.

        Args:
            ingestion_id: UUID of the data_room_ingestions row
            storage_url: Path in Supabase Storage
            legacy_simulation_id: Optional golden dataset_id for calibration
            use_mock: If True, use MockProvider instead of real LLM
        """
        try:
            self._update_status(ingestion_id, "INGESTING")

            # ── Step 1: Download ZIP ──
            logger.info(f"[{ingestion_id[:8]}] Step 1: Downloading ZIP")
            zip_bytes = self._download_zip(storage_url)

            # ── Step 2: Extract text from ZIP ──
            logger.info(f"[{ingestion_id[:8]}] Step 2: Extracting text")
            raw_text = self._extract_text_from_zip(zip_bytes)

            # ── Step 3: LLM Extraction ──
            logger.info(f"[{ingestion_id[:8]}] Step 3: LLM extraction")

            if use_mock:
                from ..providers.mock import MockLLMProvider

                provider = MockLLMProvider()
                schema_hints = {"dataset_id": legacy_simulation_id or "GD-PUB-001"}
                extracted_data = await provider.extract_structured_data(
                    raw_text.encode("utf-8"), schema_hints
                )
            else:
                from ..providers.router import create_default_router
                from ..schemas.v7_extraction import V7ExtractionSchema

                router = create_default_router()
                extraction_schema = V7ExtractionSchema.model_json_schema()
                extracted_data = await router.extract(
                    raw_text.encode("utf-8"), extraction_schema
                )

            validation_metrics: Dict[str, Any] = {}
            try:
                from ..schemas.v7_extraction import validate_v7_extraction

                validated_extraction, normalization_logs = validate_v7_extraction(
                    extracted_data
                )
                extracted_data = validated_extraction.to_engine_payload()
                if normalization_logs:
                    validation_metrics["normalization_logs"] = normalization_logs
            except (TypeError, ValueError, ValidationError) as validation_error:
                kill_reasons = [
                    "LLM extraction failed V7 schema validation",
                    str(validation_error),
                ]
                self._update_status(
                    ingestion_id,
                    "FAILED",
                    kill_reasons=kill_reasons,
                    validation_metrics={"schema_validation_error": str(validation_error)},
                )
                return {
                    "ingestion_id": ingestion_id,
                    "status": "FAILED",
                    "error": "LLM extraction failed V7 schema validation",
                }

            # ── Step 4: Polars Calculation (Diamond Core) ──
            logger.info(f"[{ingestion_id[:8]}] Step 4: Diamond Core calculation")
            polars_results = self._run_polars_engines(extracted_data)

            # ── Step 5: GoldenEvaluator (if calibration mode) ──
            accuracy_score = 100.0
            if legacy_simulation_id:
                logger.info(
                    f"[{ingestion_id[:8]}] Step 5: Golden evaluation vs {legacy_simulation_id}"
                )
                accuracy_score, validation_metrics = self._run_golden_evaluation(
                    extracted_data, legacy_simulation_id
                )
                if normalization_logs:
                    validation_metrics["normalization_logs"] = normalization_logs
                validation_metrics["accuracy_score"] = accuracy_score

            # ── Step 6: Triage ──
            logger.info(f"[{ingestion_id[:8]}] Step 6: Triage")
            from .validation.triage import (
                determine_operation_level,
            )

            kill_reasons: List[str] = []
            has_blocking = False

            # Check blocking booleans from P5
            if extracted_data.get("is_in_app"):
                kill_reasons.append("Terreno em APP (Área de Preservação Permanente)")
                has_blocking = True
            if extracted_data.get("has_contamination"):
                kill_reasons.append("Solo contaminado detectado")
                has_blocking = True
            if extracted_data.get(
                "has_adverse_possession_claims"
            ) or extracted_data.get("has_adverse_possession"):
                kill_reasons.append("Posse adversa registrada")
                has_blocking = True

            final_status = determine_operation_level(
                accuracy_score=accuracy_score,
                has_blocking_errors=has_blocking,
                kill_reasons=kill_reasons if kill_reasons else None,
                normalization_logs=normalization_logs if normalization_logs else None,
            )

            # ── Step 7: Update DB with full results ──
            logger.info(f"[{ingestion_id[:8]}] Step 7: Final update → {final_status}")
            self._update_status(
                ingestion_id,
                final_status,
                llm_extracted_payload=extracted_data,
                polars_calculations=polars_results,
                kill_reasons=kill_reasons if kill_reasons else None,
                accuracy_score=accuracy_score,
                validation_metrics=validation_metrics if validation_metrics else None,
            )

            result = {
                "ingestion_id": ingestion_id,
                "status": final_status,
                "accuracy_score": accuracy_score,
                "polars_summary": {
                    "npv": polars_results.get("npv"),
                    "irr": polars_results.get("irr"),
                    "is_viable": polars_results.get("is_viable"),
                },
            }
            logger.info(
                f"[{ingestion_id[:8]}] Pipeline complete: {final_status} (score={accuracy_score:.1f})"
            )
            return result

        except Exception as e:
            logger.error(
                f"[{ingestion_id[:8]}] Pipeline FAILED: {traceback.format_exc()}"
            )
            self._update_status(
                ingestion_id,
                "FAILED",
                kill_reasons=[f"Pipeline error: {str(e)}"],
            )
            return {
                "ingestion_id": ingestion_id,
                "status": "FAILED",
                "error": str(e),
            }
