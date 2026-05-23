from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from src.api.routes import ingest
from src.infrastructure.auth import CurrentUser


class FakeResponse:
    def __init__(self, data):
        self.data = data


class FakeQuery:
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name
        self.filters = []
        self.null_filters = []
        self.update_data = None
        self.insert_data = None
        self.limit_count = None

    def select(self, *_args):
        return self

    def update(self, data):
        self.update_data = data
        return self

    def insert(self, data):
        self.insert_data = data
        return self

    def eq(self, key, value):
        self.filters.append((key, value))
        return self

    def is_(self, key, value):
        self.null_filters.append((key, value))
        return self

    def limit(self, count):
        self.limit_count = count
        return self

    def execute(self):
        if self.insert_data is not None:
            return self._execute_insert()
        if self.update_data is not None:
            return self._execute_update()
        return self._execute_select()

    def _matches(self, row):
        for key, value in self.filters:
            if row.get(key) != value:
                return False
        for key, value in self.null_filters:
            if value == "null" and row.get(key) is not None:
                return False
        return True

    def _execute_select(self):
        rows = self.db.rows if self.table_name == "data_room_ingestions" else self.db.events
        if (
            self.table_name == "data_room_ingestion_events"
            and (
                self.db.hide_events_until_insert_conflict
                or self.db.hide_events_until_update_conflict
            )
        ):
            return FakeResponse([])
        data = [row.copy() for row in rows if self._matches(row)]
        if self.limit_count is not None:
            data = data[: self.limit_count]
        return FakeResponse(data)

    def _execute_update(self):
        if self.db.return_empty_update_once:
            self.db.return_empty_update_once = False
            self.db.hide_events_until_update_conflict = False
            if self.db.update_conflict_row_data:
                for row in self.db.rows:
                    if self._matches(row):
                        row.update(self.db.update_conflict_row_data)
            return FakeResponse([])

        updated = []
        for row in self.db.rows:
            if self._matches(row):
                row.update(self.update_data)
                updated.append(row.copy())
        return FakeResponse(updated)

    def _execute_insert(self):
        if (
            self.table_name == "data_room_ingestion_events"
            and self.db.raise_event_insert_conflict
        ):
            self.db.raise_event_insert_conflict = False
            self.db.hide_events_until_insert_conflict = False
            raise Exception("duplicate key value violates unique constraint")

        row = self.insert_data.copy()
        row["id"] = row.get("id") or f"event-{len(self.db.events) + 1}"
        self.db.events.append(row)
        return FakeResponse([row.copy()])


class FakeSupabase:
    def __init__(
        self,
        rows,
        events=None,
        raise_event_insert_conflict=False,
        hide_events_until_insert_conflict=False,
        return_empty_update_once=False,
        hide_events_until_update_conflict=False,
        update_conflict_row_data=None,
    ):
        self.rows = rows
        self.events = events or []
        self.raise_event_insert_conflict = raise_event_insert_conflict
        self.hide_events_until_insert_conflict = hide_events_until_insert_conflict
        self.return_empty_update_once = return_empty_update_once
        self.hide_events_until_update_conflict = hide_events_until_update_conflict
        self.update_conflict_row_data = update_conflict_row_data or {}

    def table(self, table_name):
        return FakeQuery(self, table_name)


def fake_request(idempotency_key="key-1"):
    return SimpleNamespace(
        headers={
            "idempotency-key": idempotency_key,
            "x-request-id": "req-1",
            "user-agent": "pytest",
        },
        client=SimpleNamespace(host="127.0.0.1"),
    )


@pytest.fixture
def user():
    return CurrentUser(id="00000000-0000-0000-0000-000000000001", email="u@test.dev")


@pytest.mark.asyncio
async def test_manual_audit_updates_status_and_writes_event(monkeypatch, user):
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "AUTONOMOUS_SENTENCED",
                "sentence_confirmed_at": None,
            }
        ]
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    response = await ingest.request_manual_audit(
        "ing-1",
        ingest.ManualAuditRequest(reason="review"),
        fake_request(),
        user,
    )

    assert response.current_status == "PENDING_HUMAN_AUDIT"
    assert response.action_status == "applied"
    assert db.rows[0]["status"] == "PENDING_HUMAN_AUDIT"
    assert db.events[0]["action"] == "REQUEST_MANUAL_AUDIT"


@pytest.mark.asyncio
async def test_manual_audit_replay_ignores_stale_expected_status(monkeypatch, user):
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "AUTONOMOUS_SENTENCED",
                "sentence_confirmed_at": None,
            }
        ]
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    first = await ingest.request_manual_audit(
        "ing-1",
        ingest.ManualAuditRequest(
            reason="review",
            expected_status="AUTONOMOUS_SENTENCED",
        ),
        fake_request("same-key"),
        user,
    )
    second = await ingest.request_manual_audit(
        "ing-1",
        ingest.ManualAuditRequest(
            reason="review",
            expected_status="AUTONOMOUS_SENTENCED",
        ),
        fake_request("same-key"),
        user,
    )

    assert first.action_status == "applied"
    assert second.action_status == "idempotent_noop"
    assert second.current_status == "PENDING_HUMAN_AUDIT"
    assert len(db.events) == 1


@pytest.mark.asyncio
async def test_manual_audit_insert_conflict_returns_existing_event(monkeypatch, user):
    existing_event = {
        "id": "event-existing",
        "ingestion_id": "ing-1",
        "action": "REQUEST_MANUAL_AUDIT",
        "idempotency_key_hash": ingest._hash_value("race-key"),
    }
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "AUTONOMOUS_SENTENCED",
                "sentence_confirmed_at": None,
            }
        ],
        events=[existing_event],
        raise_event_insert_conflict=True,
        hide_events_until_insert_conflict=True,
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    response = await ingest.request_manual_audit(
        "ing-1",
        ingest.ManualAuditRequest(
            reason="review",
            expected_status="AUTONOMOUS_SENTENCED",
        ),
        fake_request("race-key"),
        user,
    )

    assert response.action_status == "idempotent_noop"
    assert response.audit_event_id == "event-existing"
    assert response.current_status == "PENDING_HUMAN_AUDIT"
    assert len(db.events) == 1


@pytest.mark.asyncio
async def test_manual_audit_update_conflict_returns_existing_event(monkeypatch, user):
    existing_event = {
        "id": "event-existing",
        "ingestion_id": "ing-1",
        "action": "REQUEST_MANUAL_AUDIT",
        "idempotency_key_hash": ingest._hash_value("update-race-key"),
    }
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "AUTONOMOUS_SENTENCED",
                "sentence_confirmed_at": None,
            }
        ],
        events=[existing_event],
        return_empty_update_once=True,
        hide_events_until_update_conflict=True,
        update_conflict_row_data={"status": "PENDING_HUMAN_AUDIT"},
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    response = await ingest.request_manual_audit(
        "ing-1",
        ingest.ManualAuditRequest(
            reason="review",
            expected_status="AUTONOMOUS_SENTENCED",
        ),
        fake_request("update-race-key"),
        user,
    )

    assert response.action_status == "idempotent_noop"
    assert response.audit_event_id == "event-existing"
    assert response.current_status == "PENDING_HUMAN_AUDIT"
    assert len(db.events) == 1


@pytest.mark.asyncio
async def test_confirm_sentence_sets_confirmation_metadata(monkeypatch, user):
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "AUTONOMOUS_SENTENCED",
                "sentence_confirmed_at": None,
                "polars_calculations": {"npv": 1},
            }
        ]
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    response = await ingest.confirm_sentence(
        "ing-1",
        ingest.ConfirmSentenceRequest(accepted=True, notes="ok"),
        fake_request(),
        user,
    )

    assert response.current_status == "AUTONOMOUS_SENTENCED"
    assert response.action_status == "applied"
    assert db.rows[0]["sentence_confirmed_by"] == user.id
    assert db.events[0]["action"] == "CONFIRM_SENTENCE"


@pytest.mark.asyncio
async def test_complete_manual_review_sets_metadata_and_writes_event(monkeypatch, user):
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "MANUAL_ASSISTED",
                "manual_review_completed_at": None,
                "sentence_confirmed_at": None,
                "polars_calculations": {"npv": 1},
            }
        ]
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    response = await ingest.complete_manual_review(
        "ing-1",
        ingest.CompleteManualReviewRequest(
            reviewer_verdict="APPROVE_WITH_NOTES",
            notes="approved with corrected area",
            corrected_payload={"area_sqm": 1200},
        ),
        fake_request(),
        user,
    )

    assert response.current_status == "MANUAL_ASSISTED"
    assert response.action_status == "applied"
    assert response.manual_review_completed_by == user.id
    assert response.manual_review_verdict == "APPROVE_WITH_NOTES"
    assert db.rows[0]["manual_review_completed_by"] == user.id
    assert db.rows[0]["manual_review_verdict"] == "APPROVE_WITH_NOTES"
    assert db.rows[0]["manual_review_corrected_payload"] == {"area_sqm": 1200}
    assert db.events[0]["action"] == "COMPLETE_MANUAL_REVIEW"
    assert "corrected_payload" not in db.events[0]["payload_redacted"]
    assert db.events[0]["payload_redacted"]["corrected_payload_keys"] == ["area_sqm"]
    assert "corrected_payload_hash" in db.events[0]["payload_redacted"]
    assert "corrected_payload_size_bytes" in db.events[0]["payload_redacted"]


@pytest.mark.asyncio
async def test_complete_manual_review_replay_returns_noop(monkeypatch, user):
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "MANUAL_ASSISTED",
                "manual_review_completed_at": None,
                "sentence_confirmed_at": None,
                "polars_calculations": {"npv": 1},
            }
        ]
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    first = await ingest.complete_manual_review(
        "ing-1",
        ingest.CompleteManualReviewRequest(
            reviewer_verdict="APPROVE_WITH_NOTES",
            notes="approved",
            expected_status="MANUAL_ASSISTED",
        ),
        fake_request("same-review-key"),
        user,
    )
    second = await ingest.complete_manual_review(
        "ing-1",
        ingest.CompleteManualReviewRequest(
            reviewer_verdict="APPROVE_WITH_NOTES",
            notes="approved",
            expected_status="MANUAL_ASSISTED",
        ),
        fake_request("same-review-key"),
        user,
    )

    assert first.action_status == "applied"
    assert second.action_status == "idempotent_noop"
    assert second.manual_review_verdict == "APPROVE_WITH_NOTES"
    assert len(db.events) == 1


@pytest.mark.asyncio
async def test_complete_manual_review_insert_conflict_returns_existing_event(
    monkeypatch,
    user,
):
    existing_event = {
        "id": "event-existing",
        "ingestion_id": "ing-1",
        "action": "COMPLETE_MANUAL_REVIEW",
        "idempotency_key_hash": ingest._hash_value("race-review-key"),
    }
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "MANUAL_ASSISTED",
                "manual_review_completed_at": None,
                "sentence_confirmed_at": None,
                "polars_calculations": {"npv": 1},
            }
        ],
        events=[existing_event],
        raise_event_insert_conflict=True,
        hide_events_until_insert_conflict=True,
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    response = await ingest.complete_manual_review(
        "ing-1",
        ingest.CompleteManualReviewRequest(
            reviewer_verdict="APPROVE_WITH_NOTES",
            notes="approved",
            expected_status="MANUAL_ASSISTED",
        ),
        fake_request("race-review-key"),
        user,
    )

    assert response.action_status == "idempotent_noop"
    assert response.audit_event_id == "event-existing"
    assert response.manual_review_verdict == "APPROVE_WITH_NOTES"
    assert len(db.events) == 1


@pytest.mark.asyncio
async def test_complete_manual_review_update_conflict_returns_existing_event(
    monkeypatch,
    user,
):
    existing_event = {
        "id": "event-existing",
        "ingestion_id": "ing-1",
        "action": "COMPLETE_MANUAL_REVIEW",
        "idempotency_key_hash": ingest._hash_value("update-review-key"),
    }
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "MANUAL_ASSISTED",
                "manual_review_completed_at": None,
                "sentence_confirmed_at": None,
                "polars_calculations": {"npv": 1},
            }
        ],
        events=[existing_event],
        return_empty_update_once=True,
        hide_events_until_update_conflict=True,
        update_conflict_row_data={
            "manual_review_completed_at": "2026-05-22T00:00:00+00:00",
            "manual_review_completed_by": user.id,
            "manual_review_verdict": "APPROVE_WITH_NOTES",
            "manual_review_notes": "approved",
        },
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    response = await ingest.complete_manual_review(
        "ing-1",
        ingest.CompleteManualReviewRequest(
            reviewer_verdict="APPROVE_WITH_NOTES",
            notes="approved",
            expected_status="MANUAL_ASSISTED",
        ),
        fake_request("update-review-key"),
        user,
    )

    assert response.action_status == "idempotent_noop"
    assert response.audit_event_id == "event-existing"
    assert response.manual_review_verdict == "APPROVE_WITH_NOTES"
    assert len(db.events) == 1


@pytest.mark.asyncio
async def test_complete_manual_review_blocks_non_manual_assisted(monkeypatch, user):
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "AUTONOMOUS_SENTENCED",
                "manual_review_completed_at": None,
            }
        ]
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    with pytest.raises(HTTPException) as exc:
        await ingest.complete_manual_review(
            "ing-1",
            ingest.CompleteManualReviewRequest(reviewer_verdict="APPROVE_WITH_NOTES"),
            fake_request(),
            user,
        )

    assert exc.value.status_code == 409
    assert db.events == []


@pytest.mark.asyncio
async def test_confirm_sentence_allows_approved_manual_review(monkeypatch, user):
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "MANUAL_ASSISTED",
                "manual_review_completed_at": "2026-05-22T00:00:00+00:00",
                "manual_review_verdict": "APPROVE_WITH_NOTES",
                "sentence_confirmed_at": None,
                "polars_calculations": {"npv": 1},
            }
        ]
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    response = await ingest.confirm_sentence(
        "ing-1",
        ingest.ConfirmSentenceRequest(accepted=True, notes="ok"),
        fake_request(),
        user,
    )

    assert response.current_status == "MANUAL_ASSISTED"
    assert response.action_status == "applied"
    assert db.rows[0]["sentence_confirmed_by"] == user.id
    assert db.events[0]["action"] == "CONFIRM_SENTENCE"


@pytest.mark.asyncio
@pytest.mark.parametrize("verdict", ["REJECT", "REQUEST_REUPLOAD"])
async def test_confirm_sentence_blocks_non_approved_manual_review(
    monkeypatch,
    user,
    verdict,
):
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "MANUAL_ASSISTED",
                "manual_review_completed_at": "2026-05-22T00:00:00+00:00",
                "manual_review_verdict": verdict,
                "sentence_confirmed_at": None,
                "polars_calculations": {"npv": 1},
            }
        ]
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    with pytest.raises(HTTPException) as exc:
        await ingest.confirm_sentence(
            "ing-1",
            ingest.ConfirmSentenceRequest(accepted=True),
            fake_request(),
            user,
        )

    assert exc.value.status_code == 409
    assert db.events == []


@pytest.mark.asyncio
async def test_confirm_sentence_blocks_failed(monkeypatch, user):
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "FAILED",
                "sentence_confirmed_at": None,
                "polars_calculations": {"npv": 1},
            }
        ]
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    with pytest.raises(HTTPException) as exc:
        await ingest.confirm_sentence(
            "ing-1",
            ingest.ConfirmSentenceRequest(accepted=True),
            fake_request(),
            user,
        )

    assert exc.value.status_code == 409
    assert db.events == []


@pytest.mark.asyncio
async def test_replayed_idempotency_key_returns_noop(monkeypatch, user):
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "AUTONOMOUS_SENTENCED",
                "sentence_confirmed_at": None,
                "polars_calculations": {"npv": 1},
            }
        ]
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    first = await ingest.confirm_sentence(
        "ing-1",
        ingest.ConfirmSentenceRequest(accepted=True),
        fake_request("same-key"),
        user,
    )
    second = await ingest.confirm_sentence(
        "ing-1",
        ingest.ConfirmSentenceRequest(accepted=True),
        fake_request("same-key"),
        user,
    )

    assert first.action_status == "applied"
    assert second.action_status == "idempotent_noop"
    assert len(db.events) == 1


@pytest.mark.asyncio
async def test_confirm_sentence_replay_ignores_stale_expected_status(monkeypatch, user):
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "AUTONOMOUS_SENTENCED",
                "sentence_confirmed_at": None,
                "polars_calculations": {"npv": 1},
            }
        ]
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    first = await ingest.confirm_sentence(
        "ing-1",
        ingest.ConfirmSentenceRequest(
            accepted=True,
            expected_status="AUTONOMOUS_SENTENCED",
        ),
        fake_request("same-confirm-key"),
        user,
    )
    db.rows[0]["status"] = "MANUAL_ASSISTED"
    second = await ingest.confirm_sentence(
        "ing-1",
        ingest.ConfirmSentenceRequest(
            accepted=True,
            expected_status="AUTONOMOUS_SENTENCED",
        ),
        fake_request("same-confirm-key"),
        user,
    )

    assert first.action_status == "applied"
    assert second.action_status == "idempotent_noop"
    assert second.current_status == "MANUAL_ASSISTED"
    assert len(db.events) == 1


@pytest.mark.asyncio
async def test_confirm_sentence_insert_conflict_returns_existing_event(monkeypatch, user):
    existing_event = {
        "id": "event-existing",
        "ingestion_id": "ing-1",
        "action": "CONFIRM_SENTENCE",
        "idempotency_key_hash": ingest._hash_value("race-confirm-key"),
    }
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "AUTONOMOUS_SENTENCED",
                "sentence_confirmed_at": None,
                "polars_calculations": {"npv": 1},
            }
        ],
        events=[existing_event],
        raise_event_insert_conflict=True,
        hide_events_until_insert_conflict=True,
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    response = await ingest.confirm_sentence(
        "ing-1",
        ingest.ConfirmSentenceRequest(
            accepted=True,
            expected_status="AUTONOMOUS_SENTENCED",
        ),
        fake_request("race-confirm-key"),
        user,
    )

    assert response.action_status == "idempotent_noop"
    assert response.audit_event_id == "event-existing"
    assert response.current_status == "AUTONOMOUS_SENTENCED"
    assert len(db.events) == 1


@pytest.mark.asyncio
async def test_confirm_sentence_update_conflict_returns_existing_event(monkeypatch, user):
    existing_event = {
        "id": "event-existing",
        "ingestion_id": "ing-1",
        "action": "CONFIRM_SENTENCE",
        "idempotency_key_hash": ingest._hash_value("update-confirm-key"),
    }
    db = FakeSupabase(
        [
            {
                "id": "ing-1",
                "user_id": user.id,
                "status": "AUTONOMOUS_SENTENCED",
                "sentence_confirmed_at": None,
                "polars_calculations": {"npv": 1},
            }
        ],
        events=[existing_event],
        return_empty_update_once=True,
        hide_events_until_update_conflict=True,
        update_conflict_row_data={
            "sentence_confirmed_at": "2026-05-22T00:00:00+00:00",
            "sentence_confirmed_by": user.id,
        },
    )
    monkeypatch.setattr(ingest, "get_supabase_client", lambda: db)

    response = await ingest.confirm_sentence(
        "ing-1",
        ingest.ConfirmSentenceRequest(
            accepted=True,
            expected_status="AUTONOMOUS_SENTENCED",
        ),
        fake_request("update-confirm-key"),
        user,
    )

    assert response.action_status == "idempotent_noop"
    assert response.audit_event_id == "event-existing"
    assert response.current_status == "AUTONOMOUS_SENTENCED"
    assert len(db.events) == 1
