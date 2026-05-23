import asyncio
from datetime import datetime, timedelta, timezone
import logging
import os
import sys
import socket
import traceback
from typing import Any, Dict, Optional

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv() -> bool:
        return False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker_daemon")

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from supabase import create_client
from src.services.ingest_orchestrator import IngestionOrchestrator


def _env_int(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None or raw_value == "":
        return default
    try:
        return int(raw_value)
    except ValueError:
        logger.warning("Invalid integer for %s=%r. Using default %s.", name, raw_value, default)
        return default


def _get_worker_config() -> Dict[str, int]:
    return {
        "poll_interval_seconds": _env_int("WORKER_POLL_INTERVAL_SECONDS", 3),
        "failed_cooldown_seconds": _env_int("WORKER_FAILED_COOLDOWN_SECONDS", 5),
        "max_worker_attempts": _env_int("MAX_WORKER_ATTEMPTS", 2),
        "worker_stale_minutes": _env_int("WORKER_STALE_MINUTES", 30),
    }


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso_timestamp(value: Optional[datetime] = None) -> str:
    return (value or _utc_now()).isoformat()


def _get_worker_id() -> str:
    configured = os.getenv("WORKER_ID")
    if configured:
        return configured
    return f"{socket.gethostname()}:{os.getpid()}"


def _short_error(error: Any, limit: int = 2000) -> str:
    text = str(error)
    return text if len(text) <= limit else text[: limit - 3] + "..."


def _create_supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url:
        raise RuntimeError("SUPABASE_URL must be set for the worker daemon.")
    if not key:
        raise RuntimeError(
            "SUPABASE_SERVICE_ROLE_KEY must be set for the worker daemon."
        )

    return create_client(url, key)


def _claim_next_ingestion(
    supabase,
    worker_id: Optional[str] = None,
    max_attempts: Optional[int] = None,
):
    worker_id = worker_id or _get_worker_id()
    max_attempts = (
        _get_worker_config()["max_worker_attempts"]
        if max_attempts is None
        else max_attempts
    )
    response = (
        supabase.table("data_room_ingestions")
        .select("*")
        .eq("status", "UPLOADING")
        .order("created_at", desc=False)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    row = response.data[0]
    ingestion_id = row["id"]
    current_attempts = int(row.get("attempt_count") or 0)
    if current_attempts >= max_attempts:
        logger.warning(
            "Queue row %s exceeded max worker attempts (%s).",
            ingestion_id,
            max_attempts,
        )
        _mark_ingestion_failed(
            supabase,
            ingestion_id,
            f"Max worker attempts reached ({max_attempts}) before claim",
        )
        return None

    claim_data = {
        "status": "INGESTING",
        "processing_started_at": _iso_timestamp(),
        "processing_finished_at": None,
        "worker_id": worker_id,
        "attempt_count": current_attempts + 1,
        "last_error": None,
    }
    claimed = (
        supabase.table("data_room_ingestions")
        .update(claim_data)
        .eq("id", ingestion_id)
        .eq("status", "UPLOADING")
        .execute()
    )

    if not claimed.data:
        logger.info("Queue row %s was claimed by another worker.", ingestion_id)
        return None

    return claimed.data[0]


def _mark_ingestion_finished(supabase, ingestion_id: str, final_status: str) -> None:
    supabase.table("data_room_ingestions").update(
        {
            "status": final_status,
            "processing_finished_at": _iso_timestamp(),
        }
    ).eq("id", ingestion_id).execute()


def _mark_ingestion_failed(
    supabase,
    ingestion_id: str,
    error: Any,
    prefix: str = "Worker error",
    kill_reasons: Optional[list[str]] = None,
) -> None:
    message = _short_error(error)
    supabase.table("data_room_ingestions").update(
        {
            "status": "FAILED",
            "processing_finished_at": _iso_timestamp(),
            "last_error": message,
            "kill_reasons": kill_reasons or [f"{prefix}: {message}"],
        }
    ).eq("id", ingestion_id).execute()


def requeue_stale_ingestions(
    supabase,
    stale_minutes: Optional[int] = None,
    now: Optional[datetime] = None,
) -> int:
    """Internal recovery helper for INGESTING rows abandoned by a worker."""
    stale_minutes = (
        _get_worker_config()["worker_stale_minutes"]
        if stale_minutes is None
        else stale_minutes
    )
    cutoff = (now or _utc_now()) - timedelta(minutes=stale_minutes)
    response = (
        supabase.table("data_room_ingestions")
        .select("id,attempt_count,processing_started_at")
        .eq("status", "INGESTING")
        .execute()
    )

    requeued = 0
    for row in response.data or []:
        started_at = row.get("processing_started_at")
        if not started_at:
            continue
        try:
            started = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
        except (TypeError, ValueError):
            continue
        if started > cutoff:
            continue

        updated = (
            supabase.table("data_room_ingestions")
            .update(
                {
                    "status": "UPLOADING",
                    "processing_started_at": None,
                    "processing_finished_at": None,
                    "worker_id": None,
                    "last_error": "Requeued stale INGESTING row for worker retry",
                }
            )
            .eq("id", row["id"])
            .eq("status", "INGESTING")
            .execute()
        )
        if updated.data:
            requeued += 1
    return requeued


async def _process_claimed_ingestion(
    supabase,
    row: Dict[str, Any],
    orchestrator: Optional[IngestionOrchestrator] = None,
) -> Dict[str, Any]:
    ingestion_id = row["id"]
    storage_url = row["raw_storage_url"]
    legacy_sim_id = row.get("legacy_simulation_id")

    orchestrator = orchestrator or IngestionOrchestrator(supabase)
    is_mock = os.getenv("USE_MOCK", "1") == "1"

    if is_mock:
        logger.info("[DAEMON] USE_MOCK=1. Using mock extraction.")
    else:
        logger.warning("[DAEMON] USE_MOCK=0. Real LLM extraction is enabled.")

    try:
        result = await orchestrator.process(
            ingestion_id=ingestion_id,
            storage_url=storage_url,
            legacy_simulation_id=legacy_sim_id,
            use_mock=is_mock,
        )
    except Exception as error:
        _mark_ingestion_failed(
            supabase,
            ingestion_id,
            error,
            prefix="Pipeline exception",
        )
        raise

    final_status = result.get("status", "UNKNOWN")
    if final_status == "FAILED":
        _mark_ingestion_failed(
            supabase,
            ingestion_id,
            result.get("error") or "Worker pipeline returned FAILED",
            prefix="Pipeline error",
            kill_reasons=result.get("kill_reasons"),
        )
    else:
        _mark_ingestion_finished(supabase, ingestion_id, final_status)

    return result


async def run_daemon():
    load_dotenv()
    logger.info("[DAEMON] Starting VERTIV V7 ingestion worker.")
    supabase = _create_supabase_client()
    logger.info("[DAEMON] Connected to Supabase. Polling queue.")
    pid = None
    worker_id = _get_worker_id()
    config = _get_worker_config()
    logger.info("[DAEMON] Worker id: %s.", worker_id)

    while True:
        try:
            row = _claim_next_ingestion(supabase, worker_id=worker_id)

            if row:
                pid = row["id"]
                logger.info("[DAEMON] Claimed ingestion %s.", pid)

                result = await _process_claimed_ingestion(supabase, row)

                final_status = result.get("status", "UNKNOWN")
                logger.info("[DAEMON] Ingestion %s finished as %s.", pid, final_status)
                pid = None

            await asyncio.sleep(config["poll_interval_seconds"])

        except asyncio.CancelledError:
            logger.info("[DAEMON] Shutdown requested.")
            break
        except Exception as e:
            logger.error(
                "[DAEMON] Unhandled daemon error:\n%s", traceback.format_exc()
            )
            if pid:
                logger.warning("[DAEMON] Marking ingestion %s as FAILED.", pid)
                try:
                    _mark_ingestion_failed(
                        supabase,
                        pid,
                        e,
                        prefix="Daemon fatal error",
                    )
                except Exception as inner_e:
                    logger.error(
                        "[DAEMON] Failed to mark ingestion %s as FAILED: %s",
                        pid,
                        inner_e,
                    )
                finally:
                    pid = None
            await asyncio.sleep(config["failed_cooldown_seconds"])


if __name__ == "__main__":
    try:
        asyncio.run(run_daemon())
    except KeyboardInterrupt:
        print("\n[DAEMON] Interrupted.")
