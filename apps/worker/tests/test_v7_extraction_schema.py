import pytest
from pydantic import ValidationError

from src.schemas.v7_extraction import V7ExtractionSchema, validate_v7_extraction


def test_aliases_and_defaults_are_normalized_for_diamond_core():
    schema, logs = validate_v7_extraction(
        {
            "land_cost": "1250000.50",
            "land_area_sqm": "4200",
            "total_units": "180",
            "unit_price_avg": "350000",
            "construction_cost_total": "41000000",
            "development_months": "30",
            "is_in_app": "false",
            "has_contamination": 0,
            "has_adverse_possession_claims": "no",
        }
    )

    payload = schema.to_engine_payload()

    assert payload["asking_price"] == 1250000.50
    assert payload["land_cost"] == 1250000.50
    assert payload["area_sqm"] == 4200
    assert payload["land_area_sqm"] == 4200
    assert payload["sales_price_avg"] == 350000
    assert payload["unit_price_avg"] == 350000
    assert payload["funding_model"] == "SBPE"
    assert payload["use_ret_taxation"] is True
    assert payload["is_in_app"] is False
    assert {
        "field": "asking_price",
        "severity": "INFO",
        "message": "Using alias land_cost for asking_price",
        "input_value": "1250000.50",
    } in logs
    assert {
        "field": "sales_price_avg",
        "severity": "INFO",
        "message": "Using alias unit_price_avg for sales_price_avg",
        "input_value": "350000",
    } in logs


def test_construction_cost_defaults_to_three_times_land_cost_when_missing():
    schema, logs = validate_v7_extraction(
        {
            "asking_price": 1000000,
            "area_sqm": 5000,
            "total_units": 100,
            "sales_price_avg": 300000,
        }
    )

    assert schema.to_engine_payload()["construction_cost_total"] == 3000000
    assert {
        "field": "construction_cost_total",
        "severity": "INFO",
        "message": "Defaulted construction_cost_total to asking_price * 3",
        "canonical_value": 3000000.0,
    } in logs


def test_minimal_critical_payload_logs_all_relevant_defaults():
    schema, logs = validate_v7_extraction(
        {
            "asking_price": 1000000,
            "sales_price_avg": 320000,
            "total_units": 120,
        }
    )

    assert schema.to_engine_payload()["asking_price"] == 1000000
    expected_logs = {
        ("land_cost", "INFO", "Defaulted land_cost from asking_price"),
        ("area_sqm", "INFO", "Defaulted area_sqm to 5000.0"),
        ("land_area_sqm", "INFO", "Defaulted land_area_sqm from area_sqm"),
        ("unit_price_avg", "INFO", "Defaulted unit_price_avg from sales_price_avg"),
        (
            "construction_cost_total",
            "INFO",
            "Defaulted construction_cost_total to asking_price * 3",
        ),
        ("development_months", "INFO", "Defaulted development_months to 36"),
        ("incc_annual_rate", "INFO", "Defaulted incc_annual_rate to 0.05"),
        ("ipca_annual_rate", "INFO", "Defaulted ipca_annual_rate to 0.045"),
        ("use_ret_taxation", "INFO", "Defaulted use_ret_taxation to True"),
        ("permuta_physical_pct", "INFO", "Defaulted permuta_physical_pct to 0.0"),
        ("funding_model", "INFO", "Defaulted funding_model to SBPE"),
        ("green_premium", "INFO", "Defaulted green_premium to 0.0"),
        ("brown_discount", "INFO", "Defaulted brown_discount to 0.0"),
        ("volatility", "INFO", "Defaulted volatility to 0.25"),
        ("risk_free_rate", "INFO", "Defaulted risk_free_rate to 0.1175"),
        ("time_to_permit_years", "INFO", "Defaulted time_to_permit_years to 1.5"),
        ("is_in_app", "INFO", "Defaulted is_in_app to False"),
        ("has_contamination", "INFO", "Defaulted has_contamination to False"),
        (
            "has_adverse_possession_claims",
            "INFO",
            "Defaulted has_adverse_possession_claims to False",
        ),
    }
    actual_logs = {(log["field"], log["severity"], log["message"]) for log in logs}

    assert expected_logs.issubset(actual_logs)


def test_empty_or_financially_incomplete_payload_fails_before_defaults():
    with pytest.raises(ValueError, match="Missing critical V7 extraction fields"):
        validate_v7_extraction({})

    with pytest.raises(ValueError, match="sales_price_avg or unit_price_avg"):
        validate_v7_extraction({"asking_price": 1000000, "total_units": 120})

    with pytest.raises(ValueError, match="total_units or area_sqm or land_area_sqm"):
        validate_v7_extraction({"asking_price": 1000000, "sales_price_avg": 320000})


def test_conflicting_canonical_and_alias_values_are_logged_as_warnings():
    _, logs = validate_v7_extraction(
        {
            "asking_price": 100,
            "land_cost": 200,
            "area_sqm": 300,
            "land_area_sqm": 400,
            "sales_price_avg": 500,
            "unit_price_avg": 600,
            "total_units": 10,
        }
    )

    assert {
        "field": "land_cost",
        "severity": "WARNING",
        "message": "Conflicting extraction values for asking_price and land_cost; using asking_price",
        "input_value": 200,
        "canonical_value": 100,
    } in logs
    assert {
        "field": "land_area_sqm",
        "severity": "WARNING",
        "message": "Conflicting extraction values for area_sqm and land_area_sqm; using area_sqm",
        "input_value": 400,
        "canonical_value": 300,
    } in logs
    assert {
        "field": "unit_price_avg",
        "severity": "WARNING",
        "message": "Conflicting extraction values for sales_price_avg and unit_price_avg; using sales_price_avg",
        "input_value": 600,
        "canonical_value": 500,
    } in logs


def test_equivalent_aliases_do_not_emit_default_logs():
    _, logs = validate_v7_extraction(
        {
            "land_cost": 1000000,
            "land_area_sqm": 4500,
            "unit_price_avg": 320000,
        }
    )

    messages = {log["message"] for log in logs}

    assert "Defaulted asking_price to 0.0" not in messages
    assert "Defaulted area_sqm to 5000.0" not in messages
    assert "Defaulted sales_price_avg to 344700.0" not in messages


def test_invalid_required_numeric_field_fails_without_recovery():
    with pytest.raises(ValidationError):
        V7ExtractionSchema.model_validate(
            {
                "asking_price": "not-a-number",
                "area_sqm": 5000,
                "total_units": 100,
                "sales_price_avg": 300000,
            }
        )
