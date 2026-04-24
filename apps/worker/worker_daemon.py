import asyncio
import logging
import os
import sys
import traceback

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


POLL_INTERVAL_SECONDS = int(os.getenv("WORKER_POLL_INTERVAL_SECONDS", "3"))
FAILED_COOLDOWN_SECONDS = int(os.getenv("WORKER_FAILED_COOLDOWN_SECONDS", "5"))


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


def _claim_next_ingestion(supabase):
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
    claimed = (
        supabase.table("data_room_ingestions")
        .update({"status": "INGESTING"})
        .eq("id", ingestion_id)
        .eq("status", "UPLOADING")
        .execute()
    )

    if not claimed.data:
        logger.info("Queue row %s was claimed by another worker.", ingestion_id)
        return None

    return row


async def run_daemon():
    load_dotenv()
    logger.info("[DAEMON] Starting VERTIV V7 ingestion worker.")
    supabase = _create_supabase_client()
    logger.info("[DAEMON] Connected to Supabase. Polling queue.")
    pid = None

    while True:
        try:
            row = _claim_next_ingestion(supabase)

            if row:
                pid = row["id"]
                storage_url = row["raw_storage_url"]
                legacy_sim_id = row.get("legacy_simulation_id")
                logger.info("[DAEMON] Claimed ingestion %s.", pid)

                orchestrator = IngestionOrchestrator(supabase)
                is_mock = os.getenv("USE_MOCK", "1") == "1"

                if is_mock:
                    logger.info("[DAEMON] USE_MOCK=1. Using mock extraction.")
                else:
                    logger.warning(
                        "[DAEMON] USE_MOCK=0. Real LLM extraction is enabled."
                    )

                result = await orchestrator.process(
                    ingestion_id=pid,
                    storage_url=storage_url,
                    legacy_simulation_id=legacy_sim_id,
                    use_mock=is_mock,
                )

                final_status = result.get("status", "UNKNOWN")
                logger.info("[DAEMON] Ingestion %s finished as %s.", pid, final_status)
                pid = None

            await asyncio.sleep(POLL_INTERVAL_SECONDS)

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
                    supabase.table("data_room_ingestions").update(
                        {
                            "status": "FAILED",
                            "kill_reasons": [f"Daemon Fatal Error: {str(e)}"],
                        }
                    ).eq("id", pid).execute()
                except Exception as inner_e:
                    logger.error(
                        "[DAEMON] Failed to mark ingestion %s as FAILED: %s",
                        pid,
                        inner_e,
                    )
                finally:
                    pid = None
            await asyncio.sleep(FAILED_COOLDOWN_SECONDS)


if __name__ == "__main__":
    try:
        asyncio.run(run_daemon())
    except KeyboardInterrupt:
        print("\n[DAEMON] Interrupted.")
