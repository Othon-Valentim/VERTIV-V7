"""
VERTIV V7 extraction schema.

The LLM extracts facts from the Data Room. This schema normalizes those facts
into the flat payload consumed by the Diamond Core.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from pydantic import BaseModel, ConfigDict


class V7ExtractionSchema(BaseModel):
    """Validated V7 Data Room extraction payload."""

    model_config = ConfigDict(extra="allow")

    asking_price: float = 0.0
    land_cost: float | None = None
    area_sqm: float = 5000.0
    land_area_sqm: float | None = None
    total_units: int = 200
    sales_price_avg: float = 344700.0
    unit_price_avg: float | None = None
    construction_cost_total: float | None = None
    development_months: int = 36
    incc_annual_rate: float = 0.05
    ipca_annual_rate: float = 0.045
    use_ret_taxation: bool = True
    permuta_physical_pct: float = 0.0
    funding_model: str = "SBPE"
    green_premium: float = 0.0
    brown_discount: float = 0.0
    volatility: float = 0.25
    risk_free_rate: float = 0.1175
    time_to_permit_years: float = 1.5
    is_in_app: bool = False
    has_contamination: bool = False
    has_adverse_possession_claims: bool = False

    def to_engine_payload(self) -> Dict[str, Any]:
        """Return a flat dict compatible with IngestionOrchestrator._run_polars_engines."""
        payload: Dict[str, Any] = dict(self.model_extra or {})

        asking_price = self.asking_price
        area_sqm = self.area_sqm
        sales_price_avg = self.sales_price_avg
        construction_cost_total = (
            self.construction_cost_total
            if self.construction_cost_total is not None
            else asking_price * 3
        )

        payload.update(
            {
                "asking_price": asking_price,
                "land_cost": asking_price,
                "area_sqm": area_sqm,
                "land_area_sqm": area_sqm,
                "total_units": self.total_units,
                "sales_price_avg": sales_price_avg,
                "unit_price_avg": sales_price_avg,
                "construction_cost_total": construction_cost_total,
                "development_months": self.development_months,
                "incc_annual_rate": self.incc_annual_rate,
                "ipca_annual_rate": self.ipca_annual_rate,
                "use_ret_taxation": self.use_ret_taxation,
                "permuta_physical_pct": self.permuta_physical_pct,
                "funding_model": self.funding_model,
                "green_premium": self.green_premium,
                "brown_discount": self.brown_discount,
                "volatility": self.volatility,
                "risk_free_rate": self.risk_free_rate,
                "time_to_permit_years": self.time_to_permit_years,
                "is_in_app": self.is_in_app,
                "has_contamination": self.has_contamination,
                "has_adverse_possession_claims": self.has_adverse_possession_claims,
            }
        )
        return payload


def validate_v7_extraction(
    data: Dict[str, Any],
) -> Tuple[V7ExtractionSchema, List[Dict[str, Any]]]:
    """Validate provider output and return normalization logs."""
    if not isinstance(data, dict):
        raise TypeError("V7 extraction must be a JSON object")

    original = dict(data)
    normalized = dict(data)
    logs: List[Dict[str, Any]] = []

    _require_critical_fields(original)
    _log_alias_conflicts(
        original,
        primary="asking_price",
        alias="land_cost",
        logs=logs,
    )
    _log_alias_conflicts(
        original,
        primary="area_sqm",
        alias="land_area_sqm",
        logs=logs,
    )
    _log_alias_conflicts(
        original,
        primary="sales_price_avg",
        alias="unit_price_avg",
        logs=logs,
    )

    _copy_alias(
        normalized,
        primary="asking_price",
        alias="land_cost",
        logs=logs,
    )
    _copy_alias(
        normalized,
        primary="area_sqm",
        alias="land_area_sqm",
        logs=logs,
    )
    _copy_alias(
        normalized,
        primary="sales_price_avg",
        alias="unit_price_avg",
        logs=logs,
    )

    if (
        "construction_cost_total" not in normalized
        and normalized.get("asking_price") is not None
    ):
        try:
            normalized["construction_cost_total"] = float(normalized["asking_price"]) * 3
            _append_log_once(
                logs,
                {
                    "field": "construction_cost_total",
                    "severity": "INFO",
                    "message": "Defaulted construction_cost_total to asking_price * 3",
                    "canonical_value": normalized["construction_cost_total"],
                },
            )
        except (TypeError, ValueError):
            pass

    schema = V7ExtractionSchema.model_validate(normalized)
    _log_defaulted_fields(original, schema, logs)
    payload = schema.to_engine_payload()
    for key in (
        "asking_price",
        "area_sqm",
        "total_units",
        "sales_price_avg",
        "construction_cost_total",
        "development_months",
        "incc_annual_rate",
        "ipca_annual_rate",
        "use_ret_taxation",
        "is_in_app",
        "has_contamination",
        "has_adverse_possession_claims",
    ):
        if key in data and data[key] != payload[key]:
            logs.append(
                {
                    "field": key,
                    "severity": "INFO",
                    "message": f"Coerced {key} from {type(data[key]).__name__}",
                    "input_value": data[key],
                    "canonical_value": payload[key],
                }
            )

    return schema, logs


def _require_critical_fields(original: Dict[str, Any]) -> None:
    required_groups = (
        ("asking_price or land_cost", ("asking_price", "land_cost")),
        ("sales_price_avg or unit_price_avg", ("sales_price_avg", "unit_price_avg")),
        (
            "total_units or area_sqm or land_area_sqm",
            ("total_units", "area_sqm", "land_area_sqm"),
        ),
    )
    missing = [
        label
        for label, fields in required_groups
        if not any(_has_value(original, field) for field in fields)
    ]
    if missing:
        raise ValueError(
            "Missing critical V7 extraction fields: "
            + "; ".join(missing)
            + ". Required minimum: land price, average sales price, "
            + "and one operational dimension."
        )


def _log_alias_conflicts(
    original: Dict[str, Any],
    *,
    primary: str,
    alias: str,
    logs: List[Dict[str, Any]],
) -> None:
    if not (_has_value(original, primary) and _has_value(original, alias)):
        return
    if _values_equivalent(original[primary], original[alias]):
        return
    logs.append(
        {
            "field": alias,
            "severity": "WARNING",
            "message": (
                f"Conflicting extraction values for {primary} and {alias}; "
                f"using {primary}"
            ),
            "input_value": original[alias],
            "canonical_value": original[primary],
        }
    )


def _log_defaulted_fields(
    original: Dict[str, Any],
    schema: V7ExtractionSchema,
    logs: List[Dict[str, Any]],
) -> None:
    _log_alias_default(
        original,
        primary="asking_price",
        alias="land_cost",
        default_value=schema.asking_price,
        logs=logs,
    )
    _log_alias_default(
        original,
        primary="area_sqm",
        alias="land_area_sqm",
        default_value=schema.area_sqm,
        logs=logs,
    )
    _log_alias_default(
        original,
        primary="sales_price_avg",
        alias="unit_price_avg",
        default_value=schema.sales_price_avg,
        logs=logs,
    )

    if "construction_cost_total" not in original:
        _append_log_once(
            logs,
            {
                "field": "construction_cost_total",
                "severity": "INFO",
                "message": "Defaulted construction_cost_total to asking_price * 3",
                "canonical_value": schema.to_engine_payload()[
                    "construction_cost_total"
                ],
            },
        )

    for field_name in (
        "total_units",
        "development_months",
        "incc_annual_rate",
        "ipca_annual_rate",
        "use_ret_taxation",
        "permuta_physical_pct",
        "funding_model",
        "green_premium",
        "brown_discount",
        "volatility",
        "risk_free_rate",
        "time_to_permit_years",
        "is_in_app",
        "has_contamination",
        "has_adverse_possession_claims",
    ):
        if field_name not in original:
            logs.append(
                {
                    "field": field_name,
                    "severity": "INFO",
                    "message": (
                        f"Defaulted {field_name} to "
                        f"{_format_default_value(getattr(schema, field_name))}"
                    ),
                    "canonical_value": getattr(schema, field_name),
                }
            )


def _log_alias_default(
    original: Dict[str, Any],
    *,
    primary: str,
    alias: str,
    default_value: Any,
    logs: List[Dict[str, Any]],
) -> None:
    has_primary = primary in original and original.get(primary) is not None
    has_alias = alias in original and original.get(alias) is not None

    if not has_primary and not has_alias:
        logs.append(
            {
                "field": primary,
                "severity": "INFO",
                "message": (
                    f"Defaulted {primary} to {_format_default_value(default_value)}"
                ),
                "canonical_value": default_value,
            }
        )
        logs.append(
            {
                "field": alias,
                "severity": "INFO",
                "message": f"Defaulted {alias} from {primary}",
                "canonical_value": default_value,
            }
        )
    elif has_primary and not has_alias:
        logs.append(
            {
                "field": alias,
                "severity": "INFO",
                "message": f"Defaulted {alias} from {primary}",
                "canonical_value": original[primary],
            }
        )


def _format_default_value(value: Any) -> str:
    return str(value)


def _append_log_once(logs: List[Dict[str, Any]], entry: Dict[str, Any]) -> None:
    if not any(
        log.get("field") == entry.get("field")
        and log.get("message") == entry.get("message")
        for log in logs
    ):
        logs.append(entry)


def _has_value(data: Dict[str, Any], key: str) -> bool:
    return key in data and data.get(key) is not None


def _values_equivalent(left: Any, right: Any) -> bool:
    try:
        return float(left) == float(right)
    except (TypeError, ValueError):
        return left == right


def _copy_alias(
    data: Dict[str, Any],
    *,
    primary: str,
    alias: str,
    logs: List[Dict[str, Any]],
) -> None:
    if data.get(primary) is None and data.get(alias) is not None:
        data[primary] = data[alias]
        logs.append(
            {
                "field": primary,
                "severity": "INFO",
                "message": f"Using alias {alias} for {primary}",
                "input_value": data[alias],
            }
        )
