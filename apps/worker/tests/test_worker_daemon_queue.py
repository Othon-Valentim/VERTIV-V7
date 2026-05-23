from datetime import datetime, timedelta, timezone

import pytest

import worker_daemon


class FakeResponse:
    def __init__(self, data):
        self.data = data


class FakeTable:
    def __init__(self, db, name):
        self.db = db
        self.name = name
        self._update = None
        self._filters = []
        self._order_field = None
        self._order_desc = False
        self._limit = None

    def select(self, _fields):
        return self

    def update(self, data):
        self._update = data
        return self

    def eq(self, field, value):
        self._filters.append((field, value))
        return self

    def order(self, field, desc=False):
        self._order_field = field
        self._order_desc = desc
        return self

    def limit(self, count):
        self._limit = count
        return self

    def execute(self):
        rows = self.db.tables[self.name]
        matched = [
            row
            for row in rows
            if all(row.get(field) == value for field, value in self._filters)
        ]

        if self._update is not None:
            updated = []
            for row in matched:
                row.update(self._update)
                updated.append(dict(row))
                self.db.updates.append(
                    {
                        "table": self.name,
                        "filters": list(self._filters),
                        "data": dict(self._update),
                    }
                )
            return FakeResponse(updated)

        if self._order_field:
            matched = sorted(
                matched,
                key=lambda row: row.get(self._order_field) or "",
                reverse=self._order_desc,
            )
        if self._limit is not None:
            matched = matched[: self._limit]
        return FakeResponse([dict(row) for row in matched])


class FakeSupabase:
    def __init__(self, rows):
        self.tables = {"data_room_ingestions": rows}
        self.updates = []

    def table(self, name):
        return FakeTable(self, name)


class FakeOrchestrator:
    def __init__(self, result=None, error=None):
        self.result = result or {"status": "AUTONOMOUS_SENTENCED"}
        self.error = error
        self.calls = []

    async def process(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return self.result


def _row(**overrides):
    data = {
        "id": "ingestion-1",
        "status": "UPLOADING",
        "raw_storage_url": "data-rooms/user/ingestion/file.zip",
        "legacy_simulation_id": None,
        "attempt_count": 0,
        "created_at": "2026-05-22T00:00:00+00:00",
    }
    data.update(overrides)
    return data


def test_worker_config_reads_env_at_runtime(monkeypatch):
    monkeypatch.setenv("WORKER_POLL_INTERVAL_SECONDS", "11")
    monkeypatch.setenv("WORKER_FAILED_COOLDOWN_SECONDS", "13")
    monkeypatch.setenv("MAX_WORKER_ATTEMPTS", "7")
    monkeypatch.setenv("WORKER_STALE_MINUTES", "19")

    config = worker_daemon._get_worker_config()

    assert config == {
        "poll_interval_seconds": 11,
        "failed_cooldown_seconds": 13,
        "max_worker_attempts": 7,
        "worker_stale_minutes": 19,
    }


def test_worker_config_preserves_defaults(monkeypatch):
    monkeypatch.delenv("WORKER_POLL_INTERVAL_SECONDS", raising=False)
    monkeypatch.delenv("WORKER_FAILED_COOLDOWN_SECONDS", raising=False)
    monkeypatch.delenv("MAX_WORKER_ATTEMPTS", raising=False)
    monkeypatch.delenv("WORKER_STALE_MINUTES", raising=False)

    config = worker_daemon._get_worker_config()

    assert config == {
        "poll_interval_seconds": 3,
        "failed_cooldown_seconds": 5,
        "max_worker_attempts": 2,
        "worker_stale_minutes": 30,
    }


def test_two_workers_do_not_claim_same_uploading_row():
    db = FakeSupabase([_row()])

    first_claim = worker_daemon._claim_next_ingestion(
        db,
        worker_id="worker-a",
        max_attempts=2,
    )
    second_claim = worker_daemon._claim_next_ingestion(
        db,
        worker_id="worker-b",
        max_attempts=2,
    )

    assert first_claim["id"] == "ingestion-1"
    assert second_claim is None
    assert db.tables["data_room_ingestions"][0]["status"] == "INGESTING"
    assert db.tables["data_room_ingestions"][0]["worker_id"] == "worker-a"


def test_claim_increments_attempts_and_records_processing_start():
    db = FakeSupabase([_row(attempt_count=1)])

    claimed = worker_daemon._claim_next_ingestion(
        db,
        worker_id="worker-a",
        max_attempts=3,
    )

    assert claimed["attempt_count"] == 2
    assert claimed["processing_started_at"]
    assert claimed["processing_finished_at"] is None
    assert claimed["last_error"] is None


def test_max_worker_attempts_is_respected_and_row_is_not_processed():
    db = FakeSupabase([_row(attempt_count=2)])

    claimed = worker_daemon._claim_next_ingestion(
        db,
        worker_id="worker-a",
        max_attempts=2,
    )

    row = db.tables["data_room_ingestions"][0]
    assert claimed is None
    assert row["status"] == "FAILED"
    assert row["last_error"] == "Max worker attempts reached (2) before claim"
    assert row["kill_reasons"] == [
        "Worker error: Max worker attempts reached (2) before claim"
    ]


def test_failed_rows_are_not_reprocessed_automatically():
    db = FakeSupabase([_row(status="FAILED", attempt_count=1)])

    claimed = worker_daemon._claim_next_ingestion(
        db,
        worker_id="worker-a",
        max_attempts=2,
    )

    assert claimed is None
    assert db.tables["data_room_ingestions"][0]["status"] == "FAILED"


@pytest.mark.asyncio
async def test_success_records_processing_finished_at(monkeypatch):
    monkeypatch.setenv("USE_MOCK", "1")
    row = _row(status="INGESTING", attempt_count=1)
    db = FakeSupabase([row])
    orchestrator = FakeOrchestrator({"status": "AUTONOMOUS_SENTENCED"})

    result = await worker_daemon._process_claimed_ingestion(
        db,
        row,
        orchestrator=orchestrator,
    )

    assert result["status"] == "AUTONOMOUS_SENTENCED"
    assert row["status"] == "AUTONOMOUS_SENTENCED"
    assert row["processing_finished_at"]
    assert orchestrator.calls[0]["ingestion_id"] == "ingestion-1"


@pytest.mark.asyncio
async def test_failure_records_failed_last_error_and_kill_reasons(monkeypatch):
    monkeypatch.setenv("USE_MOCK", "1")
    row = _row(status="INGESTING", attempt_count=1)
    db = FakeSupabase([row])
    orchestrator = FakeOrchestrator(
        {"status": "FAILED", "error": "Schema validation failed"}
    )

    result = await worker_daemon._process_claimed_ingestion(
        db,
        row,
        orchestrator=orchestrator,
    )

    assert result["status"] == "FAILED"
    assert row["status"] == "FAILED"
    assert row["processing_finished_at"]
    assert row["last_error"] == "Schema validation failed"
    assert row["kill_reasons"] == ["Pipeline error: Schema validation failed"]


def test_stale_ingesting_rows_can_be_requeued_internally():
    now = datetime(2026, 5, 22, 12, 0, tzinfo=timezone.utc)
    stale_started = (now - timedelta(minutes=45)).isoformat()
    fresh_started = (now - timedelta(minutes=5)).isoformat()
    stale = _row(
        id="stale",
        status="INGESTING",
        processing_started_at=stale_started,
        worker_id="worker-a",
    )
    fresh = _row(
        id="fresh",
        status="INGESTING",
        processing_started_at=fresh_started,
        worker_id="worker-b",
    )
    db = FakeSupabase([stale, fresh])

    requeued = worker_daemon.requeue_stale_ingestions(
        db,
        stale_minutes=30,
        now=now,
    )

    assert requeued == 1
    assert stale["status"] == "UPLOADING"
    assert stale["worker_id"] is None
    assert fresh["status"] == "INGESTING"
