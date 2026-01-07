from typing import Optional, Dict, Any, List
from src.infrastructure.database import get_supabase_client
import json


class SimulationRepository:
    def __init__(self):
        self.table = "simulations"

    def create(self, simulation_id: str, project_data: Dict[str, Any]) -> None:
        """
        Creates a new simulation record with PENDING status.
        """
        client = get_supabase_client()
        row = {
            "id": simulation_id,
            "status": "PENDING",
            "project_data": project_data,  # Supabase JSONB column
            "result": None,
        }
        # Fire and forget or await? synchronos library used here.
        client.table(self.table).insert(row).execute()

    def get(self, simulation_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a simulation by ID.
        """
        client = get_supabase_client()
        response = (
            client.table(self.table).select("*").eq("id", simulation_id).execute()
        )
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None

    def update_result(
        self,
        simulation_id: str,
        status: str,
        result: Dict[str, Any] = None,
        error: str = None,
    ) -> None:
        """
        Updates the simulation status and result/error.
        """
        client = get_supabase_client()
        data = {"status": status}
        if result is not None:
            data["result"] = result
        if error is not None:
            data["error"] = (
                error  # Assuming 'error' column exists, if not, store in result?
            )
            # Let's assume standard schema: id, created_at, status, project_data, result (jsonb)
            # If error, we might put it in result or a separate column.
            # I'll put it in 'result' if error column doesn't exist, but arguably 'error' is better.
            # I will assume 'result' can hold the error structure for simplicity if schema is rigid,
            # but usually I'd prefer a separate column.
            # Given I don't know the schema, I will put error inside 'result' to be safe with a typical 'jsonb' payload.
            if error:
                data["result"] = {"error": error}

        client.table(self.table).update(data).eq("id", simulation_id).execute()

    def get_latest(self, limit: int = 1) -> List[Dict[str, Any]]:
        """
        Fetch the most recent simulations.
        """
        client = get_supabase_client()
        response = (
            client.table(self.table)
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data if response.data else []
