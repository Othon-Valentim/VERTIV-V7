import pytest

from src.domain.ingestion_actions import resolve_ingestion_action


@pytest.mark.parametrize("status", ["UPLOADING", "INGESTING"])
@pytest.mark.parametrize(
    "action",
    ["REQUEST_MANUAL_AUDIT", "COMPLETE_MANUAL_REVIEW", "CONFIRM_SENTENCE"],
)
def test_blocks_in_progress_statuses(status, action):
    decision = resolve_ingestion_action(action, status)

    assert decision.allowed is False
    assert decision.next_status == status


@pytest.mark.parametrize("status", ["FAILED", "KILLED"])
@pytest.mark.parametrize(
    "action",
    ["REQUEST_MANUAL_AUDIT", "COMPLETE_MANUAL_REVIEW", "CONFIRM_SENTENCE"],
)
def test_blocks_failed_and_killed(status, action):
    decision = resolve_ingestion_action(action, status)

    assert decision.allowed is False
    assert decision.next_status == status


def test_manual_audit_moves_autonomous_to_pending_human_audit():
    decision = resolve_ingestion_action(
        "REQUEST_MANUAL_AUDIT",
        "AUTONOMOUS_SENTENCED",
    )

    assert decision.allowed is True
    assert decision.action_status == "applied"
    assert decision.next_status == "PENDING_HUMAN_AUDIT"


@pytest.mark.parametrize("status", ["PENDING_HUMAN_AUDIT", "MANUAL_ASSISTED"])
def test_manual_audit_is_idempotent_when_already_manual(status):
    decision = resolve_ingestion_action("REQUEST_MANUAL_AUDIT", status)

    assert decision.allowed is True
    assert decision.action_status == "idempotent_noop"
    assert decision.next_status == status


@pytest.mark.parametrize("status", ["AUTONOMOUS_SENTENCED", "PENDING_HUMAN_AUDIT"])
def test_confirm_sentence_allowed_for_confirmable_statuses(status):
    decision = resolve_ingestion_action("CONFIRM_SENTENCE", status)

    assert decision.allowed is True
    assert decision.action_status == "applied"
    assert decision.next_status == status


def test_complete_manual_review_allowed_for_manual_assisted():
    decision = resolve_ingestion_action("COMPLETE_MANUAL_REVIEW", "MANUAL_ASSISTED")

    assert decision.allowed is True
    assert decision.action_status == "applied"
    assert decision.next_status == "MANUAL_ASSISTED"


def test_complete_manual_review_blocks_non_manual_assisted():
    decision = resolve_ingestion_action(
        "COMPLETE_MANUAL_REVIEW",
        "AUTONOMOUS_SENTENCED",
    )

    assert decision.allowed is False
    assert decision.next_status == "AUTONOMOUS_SENTENCED"


def test_complete_manual_review_is_noop_when_already_completed():
    decision = resolve_ingestion_action(
        "COMPLETE_MANUAL_REVIEW",
        "MANUAL_ASSISTED",
        manual_review_completed=True,
    )

    assert decision.allowed is True
    assert decision.action_status == "idempotent_noop"
    assert decision.next_status == "MANUAL_ASSISTED"


def test_confirm_sentence_blocks_manual_assisted_until_review_is_approved():
    decision = resolve_ingestion_action("CONFIRM_SENTENCE", "MANUAL_ASSISTED")

    assert decision.allowed is False
    assert decision.next_status == "MANUAL_ASSISTED"


def test_confirm_sentence_allows_manual_assisted_after_approved_review():
    decision = resolve_ingestion_action(
        "CONFIRM_SENTENCE",
        "MANUAL_ASSISTED",
        manual_review_completed=True,
        manual_review_verdict="APPROVE_WITH_NOTES",
    )

    assert decision.allowed is True
    assert decision.action_status == "applied"
    assert decision.next_status == "MANUAL_ASSISTED"


@pytest.mark.parametrize("verdict", ["REJECT", "REQUEST_REUPLOAD"])
def test_confirm_sentence_blocks_manual_assisted_after_non_approved_review(verdict):
    decision = resolve_ingestion_action(
        "CONFIRM_SENTENCE",
        "MANUAL_ASSISTED",
        manual_review_completed=True,
        manual_review_verdict=verdict,
    )

    assert decision.allowed is False
    assert decision.next_status == "MANUAL_ASSISTED"


def test_confirm_sentence_is_idempotent_when_already_confirmed():
    decision = resolve_ingestion_action(
        "CONFIRM_SENTENCE",
        "AUTONOMOUS_SENTENCED",
        already_confirmed=True,
    )

    assert decision.allowed is True
    assert decision.action_status == "idempotent_noop"
    assert decision.next_status == "AUTONOMOUS_SENTENCED"
