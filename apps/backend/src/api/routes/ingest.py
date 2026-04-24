"""
VERTIV V7 — Data Room Ingestion API
Endpoints for uploading data rooms and retrieving ingestion results.

POST /api/v7/ingest      → Upload ZIP, create ingestion record, trigger worker
GET  /api/v7/ingestion/{id} → Retrieve ingestion status and results
"""

import uuid
import logging
import traceback
import io
import os
import zipfile
from typing import Optional

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
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


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
