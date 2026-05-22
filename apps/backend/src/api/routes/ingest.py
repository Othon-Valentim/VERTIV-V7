"""
VERTIV V7 — Data Room Ingestion API
Endpoints for uploading data rooms and retrieving ingestion results.

POST /api/v7/ingest      → Upload ZIP, create ingestion record, trigger worker
GET  /api/v7/ingestion/{id} → Retrieve ingestion status and results
"""

import uuid
import hashlib
import json
import logging
import traceback
import io
import os
import zipfile
from datetime import datetime, timezone
from typing import Optional, Any, Literal

from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File,
    Form,
    Depends,
    BackgroundTasks,
    Request,
)
from pydantic import BaseModel

from src.infrastructure.auth import get_current_user, CurrentUser
from src.infrastructure.database import (
    get_supabase_client,
    get_supabase_client_for_user,
)
from src.domain.ingestion_actions import resolve_ingestion_action

logger = logging.getLogger("vertiv.api.ingest")
router = APIRouter()

MAX_UPLOAD_BYTES = int(os.getenv("MAX_DATA_ROOM_UPLOAD_BYTES", str(50 * 1024 * 1024)))
MAX_ZIP_ENTRIES = int(os.getenv("MAX_DATA_ROOM_ZIP_ENTRIES", "200"))
MAX_ZIP_UNCOMPRESSED_BYTES = int(
    os.getenv("MAX_DATA_ROOM_UNCOMPRESSED_BYTES", str(200 * 1024 * 1024))
)
MAX_ZIP_COMPRESSION_RATIO = float(os.getenv("MAX_DATA_ROOM_COMPRESSION_RATIO", "20"))
UPLOAD_READ_CHUNK_SIZE = 1024 * 1024


async def _read_upload_with_limit(file: UploadFile) -> bytes:
    chunks: list[bytes] = []
    total_size = 0

    while True:
        chunk = await file.read(UPLOAD_READ_CHUNK_SIZE)
        if not chunk:
            break

        total_size += len(chunk)
        if total_size > MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=413,
                detail="Arquivo excede o tamanho máximo permitido.",
            )

        chunks.append(chunk)

    return b"".join(chunks)


def _validate_zip_payload(file_bytes: bytes) -> None:
    """Reject oversized, malformed, or suspicious ZIP payloads before storage."""
    if len(file_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Arquivo excede o tamanho máximo permitido.",
        )

    if not zipfile.is_zipfile(io.BytesIO(file_bytes)):
        raise HTTPException(status_code=400, detail="Arquivo ZIP inválido.")

    try:
        with zipfile.ZipFile(io.BytesIO(file_bytes), "r") as archive:
            entries = [info for info in archive.infolist() if not info.is_dir()]
            if len(entries) > MAX_ZIP_ENTRIES:
                raise HTTPException(
                    status_code=413,
                    detail="ZIP contém arquivos demais para processamento seguro.",
                )

            uncompressed_total = sum(info.file_size for info in entries)
            compressed_total = sum(info.compress_size for info in entries)
            if uncompressed_total > MAX_ZIP_UNCOMPRESSED_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail="Conteúdo descompactado excede o limite permitido.",
                )

            if compressed_total == 0 and uncompressed_total > 0:
                raise HTTPException(status_code=400, detail="ZIP suspeito.")

            if compressed_total > 0:
                ratio = uncompressed_total / compressed_total
                if ratio > MAX_ZIP_COMPRESSION_RATIO:
                    raise HTTPException(
                        status_code=400,
                        detail="ZIP com taxa de compressão suspeita.",
                    )
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Arquivo ZIP inválido.")


def _safe_storage_filename(filename: str) -> str:
    safe_name = filename.replace("\\", "/").split("/")[-1].strip()
    return safe_name or "data-room.zip"


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class IngestResponse(BaseModel):
    ingestion_id: str
    status: str = "UPLOADING"
    message: str = "Data room accepted. Processing will begin shortly."


class IngestionDetail(BaseModel):
    id: str
    status: str
    raw_storage_url: Optional[str] = None
    llm_extracted_payload: Optional[dict] = None
    polars_calculations: Optional[dict] = None
    kill_reasons: Optional[list] = None
    legacy_simulation_id: Optional[str] = None
    accuracy_score: Optional[float] = None
    validation_metrics: Optional[dict] = None
    manual_audit_requested_at: Optional[str] = None
    manual_audit_requested_by: Optional[str] = None
    manual_review_completed_at: Optional[str] = None
    manual_review_completed_by: Optional[str] = None
    manual_review_verdict: Optional[str] = None
    manual_review_notes: Optional[str] = None
    manual_review_corrected_payload: Optional[dict] = None
    sentence_confirmed_at: Optional[str] = None
    sentence_confirmed_by: Optional[str] = None
    sentence_confirmation_notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ManualAuditRequest(BaseModel):
    reason: Optional[str] = None
    expected_status: Optional[str] = None
    idempotency_key: Optional[str] = None


class ConfirmSentenceRequest(BaseModel):
    accepted: bool = True
    notes: Optional[str] = None
    expected_status: Optional[str] = None
    decision_snapshot_hash: Optional[str] = None
    idempotency_key: Optional[str] = None


class CompleteManualReviewRequest(BaseModel):
    reviewer_verdict: Literal[
        "APPROVE_WITH_NOTES",
        "REJECT",
        "REQUEST_REUPLOAD",
    ]
    notes: Optional[str] = None
    corrected_payload: Optional[dict] = None
    expected_status: Optional[str] = None
    idempotency_key: Optional[str] = None


class IngestionActionResponse(BaseModel):
    ingestion_id: str
    action: str
    action_status: str
    previous_status: str
    current_status: str
    audit_event_id: Optional[str] = None
    manual_audit_requested_at: Optional[str] = None
    manual_review_completed_at: Optional[str] = None
    manual_review_completed_by: Optional[str] = None
    manual_review_verdict: Optional[str] = None
    sentence_confirmed_at: Optional[str] = None
    sentence_confirmed_by: Optional[str] = None
    updated_at: Optional[str] = None


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_value(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _idempotency_hash(request: Request, body_key: Optional[str]) -> Optional[str]:
    header_key = request.headers.get("idempotency-key")
    return _hash_value(header_key or body_key)


def _request_ip_hash(request: Request) -> Optional[str]:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    ip = forwarded_for.split(",")[0].strip() if forwarded_for else None
    if not ip and request.client:
        ip = request.client.host
    return _hash_value(ip)


def _redacted_payload(**values: Any) -> dict:
    return {key: value for key, value in values.items() if value not in (None, "")}


def _json_payload_summary(name: str, payload: Optional[dict]) -> dict:
    if payload is None:
        return {}

    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return {
        f"{name}_hash": hashlib.sha256(encoded).hexdigest(),
        f"{name}_keys": sorted(str(key) for key in payload.keys()),
        f"{name}_size_bytes": len(encoded),
    }


def _get_owned_ingestion(db, ingestion_id: str, user: CurrentUser) -> dict:
    response = (
        db.table("data_room_ingestions")
        .select("*")
        .eq("id", ingestion_id)
        .eq("user_id", user.id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Ingestion not found or access denied.",
        )

    return response.data[0]


def _find_idempotent_event(
    db,
    ingestion_id: str,
    action: str,
    idempotency_key_hash: Optional[str],
) -> Optional[dict]:
    if not idempotency_key_hash:
        return None

    response = (
        db.table("data_room_ingestion_events")
        .select("*")
        .eq("ingestion_id", ingestion_id)
        .eq("action", action)
        .eq("idempotency_key_hash", idempotency_key_hash)
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None


def _insert_action_event(
    db,
    *,
    ingestion_id: str,
    user: CurrentUser,
    action: str,
    action_status: str,
    previous_status: str,
    new_status: str,
    request: Request,
    idempotency_key_hash: Optional[str],
    payload_redacted: dict,
) -> tuple[Optional[str], bool]:
    event = {
        "ingestion_id": ingestion_id,
        "actor_user_id": user.id,
        "actor_email": user.email,
        "action": action,
        "action_status": action_status,
        "previous_status": previous_status,
        "new_status": new_status,
        "idempotency_key_hash": idempotency_key_hash,
        "request_id": request.headers.get("x-request-id"),
        "ip_hash": _request_ip_hash(request),
        "user_agent": request.headers.get("user-agent"),
        "payload_redacted": payload_redacted,
    }
    try:
        response = db.table("data_room_ingestion_events").insert(event).execute()
    except Exception:
        if idempotency_key_hash:
            existing_event = _find_idempotent_event(
                db,
                ingestion_id,
                action,
                idempotency_key_hash,
            )
            if existing_event:
                return existing_event.get("id"), True
        raise

    if response.data:
        return response.data[0].get("id"), False
    return None, False


def _build_action_response(
    *,
    row: dict,
    ingestion_id: str,
    action: str,
    action_status: str,
    previous_status: str,
    current_status: str,
    audit_event_id: Optional[str],
) -> IngestionActionResponse:
    return IngestionActionResponse(
        ingestion_id=ingestion_id,
        action=action,
        action_status=action_status,
        previous_status=previous_status,
        current_status=current_status,
        audit_event_id=audit_event_id,
        manual_audit_requested_at=row.get("manual_audit_requested_at"),
        manual_review_completed_at=row.get("manual_review_completed_at"),
        manual_review_completed_by=row.get("manual_review_completed_by"),
        manual_review_verdict=row.get("manual_review_verdict"),
        sentence_confirmed_at=row.get("sentence_confirmed_at"),
        sentence_confirmed_by=row.get("sentence_confirmed_by"),
        updated_at=row.get("updated_at"),
    )


def _build_idempotent_response_if_event_exists(
    db,
    *,
    ingestion_id: str,
    user: CurrentUser,
    action: str,
    idempotency_key_hash: Optional[str],
    previous_status: str,
) -> Optional[IngestionActionResponse]:
    existing_event = _find_idempotent_event(
        db,
        ingestion_id,
        action,
        idempotency_key_hash,
    )
    if not existing_event:
        return None

    fresh_row = _get_owned_ingestion(db, ingestion_id, user)
    return _build_action_response(
        row=fresh_row,
        ingestion_id=ingestion_id,
        action=action,
        action_status="idempotent_noop",
        previous_status=previous_status,
        current_status=fresh_row["status"],
        audit_event_id=existing_event.get("id"),
    )


# ---------------------------------------------------------------------------
# Worker trigger (REMOVED - HTTP DECAPITATED)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# POST /api/v7/ingest
# ---------------------------------------------------------------------------


@router.post("/ingest", response_model=IngestResponse, status_code=202)
async def ingest_data_room(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    legacy_simulation_id: Optional[str] = Form(None),
    user: CurrentUser = Depends(get_current_user),
):
    """
    Upload a Data Room ZIP for agentic processing.

    Flow:
    1. Validate file is .zip
    2. Upload to Supabase Storage bucket 'data-rooms'
    3. Create row in data_room_ingestions (status: UPLOADING)
    4. Trigger async worker processing
    5. Return ingestion_id (client redirects to /audit/{id})
    """
    # 1. Validate
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos .zip são aceitos.",
        )

    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > MAX_UPLOAD_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail="Arquivo excede o tamanho máximo permitido.",
                )
        except ValueError:
            raise HTTPException(status_code=400, detail="Content-Length inválido.")

    ingestion_id = str(uuid.uuid4())
    # Extract raw JWT for user-authenticated Supabase client (RLS compat)
    auth_header = request.headers.get("authorization", "")
    raw_jwt = auth_header.replace("Bearer ", "") if auth_header else ""
    db = get_supabase_client_for_user(raw_jwt) if raw_jwt else get_supabase_client()

    try:
        # 2. Upload to Supabase Storage
        file_bytes = await _read_upload_with_limit(file)
        _validate_zip_payload(file_bytes)

        storage_path = f"{user.id}/{ingestion_id}/{_safe_storage_filename(file.filename)}"

        storage_response = db.storage.from_("data-rooms").upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": "application/zip"},
        )

        storage_url = f"data-rooms/{storage_path}"
        logger.info(f"Uploaded {len(file_bytes)} bytes to {storage_url}")

        # 3. Create ingestion record
        row = {
            "id": ingestion_id,
            "user_id": user.id,
            "status": "UPLOADING",
            "raw_storage_url": storage_url,
            "legacy_simulation_id": (
                legacy_simulation_id if legacy_simulation_id else None
            ),
        }
        db.table("data_room_ingestions").insert(row).execute()
        logger.info(f"Created ingestion record: {ingestion_id}")

        # 4. Return to UI — The Tracer Bullet will pick up the UPLOADING row
        return IngestResponse(
            ingestion_id=ingestion_id,
            status="UPLOADING",
            message="Data room aceito. Aguardando processamento agêntico.",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ingestion failed: {traceback.format_exc()}")
        # Try to mark as FAILED if record was created
        try:
            db.table("data_room_ingestions").update({"status": "FAILED"}).eq(
                "id", ingestion_id
            ).execute()
        except Exception:
            pass
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao processar ingestão.",
        )


# ---------------------------------------------------------------------------
# GET /api/v7/ingestion/{id}
# ---------------------------------------------------------------------------


@router.get("/ingestion/{ingestion_id}", response_model=IngestionDetail)
async def get_ingestion(
    ingestion_id: str,
    user: CurrentUser = Depends(get_current_user),
):
    """
    Retrieve the full status and results of a data room ingestion.
    RLS ensures users can only see their own ingestions.
    """
    db = get_supabase_client()

    try:
        response = (
            db.table("data_room_ingestions")
            .select("*")
            .eq("id", ingestion_id)
            .eq("user_id", user.id)
            .execute()
        )

        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=404,
                detail="Ingestion not found or access denied.",
            )

        row = response.data[0]
        return IngestionDetail(
            id=row["id"],
            status=row["status"],
            raw_storage_url=row.get("raw_storage_url"),
            llm_extracted_payload=row.get("llm_extracted_payload"),
            polars_calculations=row.get("polars_calculations"),
            kill_reasons=row.get("kill_reasons"),
            legacy_simulation_id=row.get("legacy_simulation_id"),
            accuracy_score=row.get("accuracy_score"),
            validation_metrics=row.get("validation_metrics"),
            manual_audit_requested_at=row.get("manual_audit_requested_at"),
            manual_audit_requested_by=row.get("manual_audit_requested_by"),
            manual_review_completed_at=row.get("manual_review_completed_at"),
            manual_review_completed_by=row.get("manual_review_completed_by"),
            manual_review_verdict=row.get("manual_review_verdict"),
            manual_review_notes=row.get("manual_review_notes"),
            manual_review_corrected_payload=row.get("manual_review_corrected_payload"),
            sentence_confirmed_at=row.get("sentence_confirmed_at"),
            sentence_confirmed_by=row.get("sentence_confirmed_by"),
            sentence_confirmation_notes=row.get("sentence_confirmation_notes"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get ingestion failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar ingestão: {str(e)}",
        )


# ---------------------------------------------------------------------------
# POST /api/v7/ingestion/{id}/manual-audit
# ---------------------------------------------------------------------------


@router.post(
    "/ingestion/{ingestion_id}/manual-audit",
    response_model=IngestionActionResponse,
)
async def request_manual_audit(
    ingestion_id: str,
    payload: ManualAuditRequest,
    request: Request,
    user: CurrentUser = Depends(get_current_user),
):
    db = get_supabase_client()
    action = "REQUEST_MANUAL_AUDIT"
    idempotency_key_hash = _idempotency_hash(request, payload.idempotency_key)

    try:
        row = _get_owned_ingestion(db, ingestion_id, user)
        previous_status = row["status"]

        existing_event = _find_idempotent_event(
            db, ingestion_id, action, idempotency_key_hash
        )
        if existing_event:
            fresh_row = _get_owned_ingestion(db, ingestion_id, user)
            return _build_action_response(
                row=fresh_row,
                ingestion_id=ingestion_id,
                action=action,
                action_status="idempotent_noop",
                previous_status=previous_status,
                current_status=fresh_row["status"],
                audit_event_id=existing_event.get("id"),
            )

        if payload.expected_status and payload.expected_status != previous_status:
            raise HTTPException(
                status_code=409,
                detail="Status atual diverge do esperado.",
            )

        decision = resolve_ingestion_action(action, previous_status)
        if not decision.allowed:
            raise HTTPException(status_code=409, detail=decision.reason)

        updated_row = row
        if decision.action_status == "applied":
            update_data = {
                "status": decision.next_status,
                "manual_audit_requested_at": _utc_now_iso(),
                "manual_audit_requested_by": user.id,
            }
            update_response = (
                db.table("data_room_ingestions")
                .update(update_data)
                .eq("id", ingestion_id)
                .eq("user_id", user.id)
                .eq("status", previous_status)
                .execute()
            )

            if not update_response.data:
                idempotent_response = _build_idempotent_response_if_event_exists(
                    db,
                    ingestion_id=ingestion_id,
                    user=user,
                    action=action,
                    idempotency_key_hash=idempotency_key_hash,
                    previous_status=previous_status,
                )
                if idempotent_response:
                    return idempotent_response

                raise HTTPException(
                    status_code=409,
                    detail="Status mudou antes da acao ser aplicada.",
                )
            updated_row = update_response.data[0]

        event_id, event_replayed = _insert_action_event(
            db,
            ingestion_id=ingestion_id,
            user=user,
            action=action,
            action_status=decision.action_status,
            previous_status=previous_status,
            new_status=decision.next_status,
            request=request,
            idempotency_key_hash=idempotency_key_hash,
            payload_redacted=_redacted_payload(reason=payload.reason),
        )
        if event_replayed:
            updated_row = _get_owned_ingestion(db, ingestion_id, user)

        return _build_action_response(
            row=updated_row,
            ingestion_id=ingestion_id,
            action=action,
            action_status=(
                "idempotent_noop" if event_replayed else decision.action_status
            ),
            previous_status=previous_status,
            current_status=updated_row["status"],
            audit_event_id=event_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Manual audit action failed: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao solicitar auditoria manual: {str(e)}",
        )


# ---------------------------------------------------------------------------
# POST /api/v7/ingestion/{id}/complete-manual-review
# ---------------------------------------------------------------------------


@router.post(
    "/ingestion/{ingestion_id}/complete-manual-review",
    response_model=IngestionActionResponse,
)
async def complete_manual_review(
    ingestion_id: str,
    payload: CompleteManualReviewRequest,
    request: Request,
    user: CurrentUser = Depends(get_current_user),
):
    db = get_supabase_client()
    action = "COMPLETE_MANUAL_REVIEW"
    idempotency_key_hash = _idempotency_hash(request, payload.idempotency_key)

    try:
        row = _get_owned_ingestion(db, ingestion_id, user)
        previous_status = row["status"]

        existing_event = _find_idempotent_event(
            db, ingestion_id, action, idempotency_key_hash
        )
        if existing_event:
            fresh_row = _get_owned_ingestion(db, ingestion_id, user)
            return _build_action_response(
                row=fresh_row,
                ingestion_id=ingestion_id,
                action=action,
                action_status="idempotent_noop",
                previous_status=previous_status,
                current_status=fresh_row["status"],
                audit_event_id=existing_event.get("id"),
            )

        if payload.expected_status and payload.expected_status != previous_status:
            raise HTTPException(
                status_code=409,
                detail="Status atual diverge do esperado.",
            )

        decision = resolve_ingestion_action(
            action,
            previous_status,
            manual_review_completed=bool(row.get("manual_review_completed_at")),
        )
        if not decision.allowed:
            raise HTTPException(status_code=409, detail=decision.reason)

        updated_row = row
        if decision.action_status == "applied":
            update_data = {
                "manual_review_completed_at": _utc_now_iso(),
                "manual_review_completed_by": user.id,
                "manual_review_verdict": payload.reviewer_verdict,
                "manual_review_notes": payload.notes,
                "manual_review_corrected_payload": payload.corrected_payload,
            }
            update_response = (
                db.table("data_room_ingestions")
                .update(update_data)
                .eq("id", ingestion_id)
                .eq("user_id", user.id)
                .eq("status", previous_status)
                .is_("manual_review_completed_at", "null")
                .execute()
            )

            if not update_response.data:
                idempotent_response = _build_idempotent_response_if_event_exists(
                    db,
                    ingestion_id=ingestion_id,
                    user=user,
                    action=action,
                    idempotency_key_hash=idempotency_key_hash,
                    previous_status=previous_status,
                )
                if idempotent_response:
                    return idempotent_response

                raise HTTPException(
                    status_code=409,
                    detail="Revisao manual ja concluida ou status alterado.",
                )
            updated_row = update_response.data[0]

        event_id, event_replayed = _insert_action_event(
            db,
            ingestion_id=ingestion_id,
            user=user,
            action=action,
            action_status=decision.action_status,
            previous_status=previous_status,
            new_status=decision.next_status,
            request=request,
            idempotency_key_hash=idempotency_key_hash,
            payload_redacted=_redacted_payload(
                reviewer_verdict=payload.reviewer_verdict,
                notes=payload.notes,
                **_json_payload_summary(
                    "corrected_payload",
                    payload.corrected_payload,
                ),
            ),
        )
        if event_replayed:
            updated_row = _get_owned_ingestion(db, ingestion_id, user)

        return _build_action_response(
            row=updated_row,
            ingestion_id=ingestion_id,
            action=action,
            action_status=(
                "idempotent_noop" if event_replayed else decision.action_status
            ),
            previous_status=previous_status,
            current_status=updated_row["status"],
            audit_event_id=event_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Complete manual review action failed: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao concluir revisao manual: {str(e)}",
        )


# ---------------------------------------------------------------------------
# POST /api/v7/ingestion/{id}/confirm-sentence
# ---------------------------------------------------------------------------


@router.post(
    "/ingestion/{ingestion_id}/confirm-sentence",
    response_model=IngestionActionResponse,
)
async def confirm_sentence(
    ingestion_id: str,
    payload: ConfirmSentenceRequest,
    request: Request,
    user: CurrentUser = Depends(get_current_user),
):
    if not payload.accepted:
        raise HTTPException(status_code=422, detail="accepted deve ser true.")

    db = get_supabase_client()
    action = "CONFIRM_SENTENCE"
    idempotency_key_hash = _idempotency_hash(request, payload.idempotency_key)

    try:
        row = _get_owned_ingestion(db, ingestion_id, user)
        previous_status = row["status"]

        existing_event = _find_idempotent_event(
            db, ingestion_id, action, idempotency_key_hash
        )
        if existing_event:
            fresh_row = _get_owned_ingestion(db, ingestion_id, user)
            return _build_action_response(
                row=fresh_row,
                ingestion_id=ingestion_id,
                action=action,
                action_status="idempotent_noop",
                previous_status=previous_status,
                current_status=fresh_row["status"],
                audit_event_id=existing_event.get("id"),
            )

        if payload.expected_status and payload.expected_status != previous_status:
            raise HTTPException(
                status_code=409,
                detail="Status atual diverge do esperado.",
            )

        already_confirmed = bool(row.get("sentence_confirmed_at"))
        decision = resolve_ingestion_action(
            action,
            previous_status,
            already_confirmed=already_confirmed,
            manual_review_completed=bool(row.get("manual_review_completed_at")),
            manual_review_verdict=row.get("manual_review_verdict"),
        )
        if not decision.allowed:
            raise HTTPException(status_code=409, detail=decision.reason)

        if decision.action_status == "applied" and not row.get("polars_calculations"):
            raise HTTPException(
                status_code=409,
                detail="Sentenca nao pode ser confirmada sem calculos Polars.",
            )

        updated_row = row
        if decision.action_status == "applied":
            update_data = {
                "sentence_confirmed_at": _utc_now_iso(),
                "sentence_confirmed_by": user.id,
                "sentence_confirmation_notes": payload.notes,
            }
            update_response = (
                db.table("data_room_ingestions")
                .update(update_data)
                .eq("id", ingestion_id)
                .eq("user_id", user.id)
                .eq("status", previous_status)
                .is_("sentence_confirmed_at", "null")
                .execute()
            )

            if not update_response.data:
                idempotent_response = _build_idempotent_response_if_event_exists(
                    db,
                    ingestion_id=ingestion_id,
                    user=user,
                    action=action,
                    idempotency_key_hash=idempotency_key_hash,
                    previous_status=previous_status,
                )
                if idempotent_response:
                    return idempotent_response

                raise HTTPException(
                    status_code=409,
                    detail="Sentenca ja confirmada ou status alterado.",
                )
            updated_row = update_response.data[0]

        event_id, event_replayed = _insert_action_event(
            db,
            ingestion_id=ingestion_id,
            user=user,
            action=action,
            action_status=decision.action_status,
            previous_status=previous_status,
            new_status=decision.next_status,
            request=request,
            idempotency_key_hash=idempotency_key_hash,
            payload_redacted=_redacted_payload(
                notes=payload.notes,
                decision_snapshot_hash=payload.decision_snapshot_hash,
            ),
        )
        if event_replayed:
            updated_row = _get_owned_ingestion(db, ingestion_id, user)

        return _build_action_response(
            row=updated_row,
            ingestion_id=ingestion_id,
            action=action,
            action_status=(
                "idempotent_noop" if event_replayed else decision.action_status
            ),
            previous_status=previous_status,
            current_status=updated_row["status"],
            audit_event_id=event_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Confirm sentence action failed: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao confirmar sentenca: {str(e)}",
        )
