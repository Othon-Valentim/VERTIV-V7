import pytest

from src.services.ingest_orchestrator import IngestionOrchestrator


class FakeProvider:
    def __init__(self, payload):
        self.payload = payload

    async def extract(self, raw_content, extraction_schema):
        return self.payload


class FakeTable:
    def __init__(self, db):
        self.db = db
        self.pending_update = None

    def update(self, data):
        self.pending_update = data
        return self

    def eq(self, _field, _value):
        return self

    def execute(self):
        self.db.updates.append(self.pending_update)
        return type("Response", (), {"data": []})()


class FakeDB:
    def __init__(self):
        self.updates = []

    def table(self, _name):
        return FakeTable(self)


def _patch_orchestrator_io(monkeypatch, orchestrator):
    monkeypatch.setattr(orchestrator, "_download_zip", lambda _storage_url: b"zip")
    monkeypatch.setattr(orchestrator, "_extract_text_from_zip", lambda _zip: "data room")
    monkeypatch.setattr(
        orchestrator,
        "_run_polars_engines",
        lambda payload: {
            "npv": 100,
            "irr": 12,
            "is_viable": True,
            "total_units": payload["total_units"],
            "sales_price_avg": payload["sales_price_avg"],
            "construction_cost_total": payload["construction_cost_total"],
        },
    )


@pytest.mark.asyncio
async def test_process_marks_failed_when_provider_payload_fails_v7_validation(
    monkeypatch,
):
    import src.providers.router as router_module

    db = FakeDB()
    orchestrator = IngestionOrchestrator(db)
    _patch_orchestrator_io(monkeypatch, orchestrator)
    monkeypatch.setattr(
        router_module,
        "create_default_router",
        lambda: FakeProvider({}),
    )

    result = await orchestrator.process(
        "ingestion-1",
        "data-rooms/user/ingestion/file.zip",
        use_mock=False,
    )

    assert result["status"] == "FAILED"
    failed_update = db.updates[-1]
    assert failed_update["status"] == "FAILED"
    assert failed_update["kill_reasons"][0] == "LLM extraction failed V7 schema validation"
    assert "Missing critical V7 extraction fields" in failed_update["kill_reasons"][1]


@pytest.mark.asyncio
async def test_process_preserves_structured_normalization_logs_in_validation_metrics(
    monkeypatch,
):
    import src.providers.router as router_module

    db = FakeDB()
    orchestrator = IngestionOrchestrator(db)
    _patch_orchestrator_io(monkeypatch, orchestrator)
    monkeypatch.setattr(
        router_module,
        "create_default_router",
        lambda: FakeProvider(
            {
                "asking_price": 100,
                "land_cost": 200,
                "sales_price_avg": 500,
                "unit_price_avg": 600,
                "total_units": 10,
            }
        ),
    )

    result = await orchestrator.process(
        "ingestion-2",
        "data-rooms/user/ingestion/file.zip",
        use_mock=False,
    )

    assert result["status"] in {"AUTONOMOUS_SENTENCED", "PENDING_HUMAN_AUDIT"}
    final_update = db.updates[-1]
    logs = final_update["validation_metrics"]["normalization_logs"]
    assert any(log["severity"] == "WARNING" for log in logs)
    assert {
        "field": "land_cost",
        "severity": "WARNING",
        "message": "Conflicting extraction values for asking_price and land_cost; using asking_price",
        "input_value": 200,
        "canonical_value": 100,
    } in logs
