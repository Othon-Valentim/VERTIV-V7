import os
import json
import httpx
from typing import Optional
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
from src.domain.schemas import SimulationRequest

# Environment variables
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "vertiv-v6")
location = os.getenv("GOOGLE_CLOUD_REGION", "southamerica-east1")
QUEUE_ID = os.getenv("CLOUD_TASKS_QUEUE", "financial-simulations")
WORKER_URL = os.getenv(
    "WORKER_URL", "http://localhost:8001/tasks/process-simulation"
)  # Default to local worker
ENV = os.getenv("ENV", "DEV")


class TaskDispatcher:
    """
    Abstracts the dispatch logic.
    In DEV: Calls Worker /process-simulation directly via HTTP.
    In PROD: Creates a Cloud Task targeting the Worker.
    """

    @staticmethod
    async def dispatch_simulation(payload: SimulationRequest) -> str:
        """
        Dispatches the simulation task. Returns the Task Name or ID.
        """
        payload_dict = payload.model_dump(mode="json")

        if ENV in ["DEV", "development"]:
            # Direct HTTP Call to Worker (Simulating Push Queue)
            print(f"[Queue] DEV MODE: Dispatching directly to {WORKER_URL}")
            async with httpx.AsyncClient() as client:
                try:
                    # Fire and forget (or wait for 1s to ensure it reached)
                    # For a true fire-and-forget in dev without blocking, we might want to just spawn a background task
                    # But for now, we await to ensure connectivity, but real Cloud Tasks is async.
                    # To mimic async, we could use asyncio.create_task, but let's just await response for MVP dev stability.
                    resp = await client.post(
                        WORKER_URL, json=payload_dict, timeout=30.0
                    )
                    resp.raise_for_status()
                    return f"local-task-{payload.simulation_id}"
                except Exception as e:
                    print(f"[Queue] ERROR: Could not dispatch to local worker: {e}")
                    raise e
        else:
            # Cloud Tasks (Production)
            client = tasks_v2.CloudTasksAsyncClient()
            parent = client.queue_path(PROJECT_ID, location, QUEUE_ID)

            task = {
                "http_request": {  # Specify the type of request.
                    "http_method": tasks_v2.HttpMethod.POST,
                    "url": WORKER_URL,  # The full URL of the entry point of the worker service
                    "headers": {"Content-type": "application/json"},
                    "body": json.dumps(payload_dict).encode(),
                }
            }

            response = await client.create_task(
                request={"parent": parent, "task": task}
            )
            return response.name
