from dataclasses import dataclass
from typing import Literal


IngestionAction = Literal[
    "REQUEST_MANUAL_AUDIT",
    "COMPLETE_MANUAL_REVIEW",
    "CONFIRM_SENTENCE",
]

UPLOADING = "UPLOADING"
INGESTING = "INGESTING"
AUTONOMOUS_SENTENCED = "AUTONOMOUS_SENTENCED"
PENDING_HUMAN_AUDIT = "PENDING_HUMAN_AUDIT"
MANUAL_ASSISTED = "MANUAL_ASSISTED"
KILLED = "KILLED"
FAILED = "FAILED"

IN_PROGRESS_STATUSES = {UPLOADING, INGESTING}
BLOCKED_TERMINAL_STATUSES = {KILLED, FAILED}
CONFIRMABLE_STATUSES = {AUTONOMOUS_SENTENCED, PENDING_HUMAN_AUDIT}
MANUAL_REVIEW_APPROVED_VERDICT = "APPROVE_WITH_NOTES"


@dataclass(frozen=True)
class IngestionActionDecision:
    allowed: bool
    action_status: Literal["applied", "idempotent_noop"]
    next_status: str
    reason: str


def resolve_ingestion_action(
    action: IngestionAction,
    current_status: str,
    *,
    already_confirmed: bool = False,
    manual_review_completed: bool = False,
    manual_review_verdict: str | None = None,
) -> IngestionActionDecision:
    if current_status in IN_PROGRESS_STATUSES:
        return IngestionActionDecision(
            allowed=False,
            action_status="applied",
            next_status=current_status,
            reason="Ingestao ainda em processamento.",
        )

    if current_status in BLOCKED_TERMINAL_STATUSES:
        return IngestionActionDecision(
            allowed=False,
            action_status="applied",
            next_status=current_status,
            reason="Status terminal nao permite acao humana.",
        )

    if action == "REQUEST_MANUAL_AUDIT":
        if current_status == AUTONOMOUS_SENTENCED:
            return IngestionActionDecision(
                allowed=True,
                action_status="applied",
                next_status=PENDING_HUMAN_AUDIT,
                reason="Auditoria manual solicitada.",
            )

        if current_status in {PENDING_HUMAN_AUDIT, MANUAL_ASSISTED}:
            return IngestionActionDecision(
                allowed=True,
                action_status="idempotent_noop",
                next_status=current_status,
                reason="Ingestao ja esta em fluxo de auditoria manual.",
            )

        return IngestionActionDecision(
            allowed=False,
            action_status="applied",
            next_status=current_status,
            reason="Status nao permite solicitar auditoria manual.",
        )

    if action == "COMPLETE_MANUAL_REVIEW":
        if current_status != MANUAL_ASSISTED:
            return IngestionActionDecision(
                allowed=False,
                action_status="applied",
                next_status=current_status,
                reason="Status nao permite concluir revisao manual.",
            )

        if manual_review_completed:
            return IngestionActionDecision(
                allowed=True,
                action_status="idempotent_noop",
                next_status=current_status,
                reason="Revisao manual ja concluida.",
            )

        return IngestionActionDecision(
            allowed=True,
            action_status="applied",
            next_status=current_status,
            reason="Revisao manual concluida.",
        )

    if action == "CONFIRM_SENTENCE":
        if already_confirmed:
            return IngestionActionDecision(
                allowed=True,
                action_status="idempotent_noop",
                next_status=current_status,
                reason="Sentenca ja confirmada.",
            )

        if current_status in CONFIRMABLE_STATUSES:
            return IngestionActionDecision(
                allowed=True,
                action_status="applied",
                next_status=current_status,
                reason="Sentenca confirmada.",
            )

        if current_status == MANUAL_ASSISTED:
            if (
                manual_review_completed
                and manual_review_verdict == MANUAL_REVIEW_APPROVED_VERDICT
            ):
                return IngestionActionDecision(
                    allowed=True,
                    action_status="applied",
                    next_status=current_status,
                    reason="Sentenca confirmada apos revisao manual.",
                )

            return IngestionActionDecision(
                allowed=False,
                action_status="applied",
                next_status=current_status,
                reason="Revisao manual aprovada e obrigatoria para confirmar sentenca.",
            )

        return IngestionActionDecision(
            allowed=False,
            action_status="applied",
            next_status=current_status,
            reason="Status nao permite confirmar sentenca.",
        )

    return IngestionActionDecision(
        allowed=False,
        action_status="applied",
        next_status=current_status,
        reason="Acao desconhecida.",
    )
