from typing import Optional, Dict, Any, List
from src.infrastructure.database import get_supabase_client
import json
from datetime import datetime
import uuid


class SimulationRepository:
    def __init__(self):
        self.table = "simulations"

    def create(self, simulation_id: str, project_data: Dict[str, Any], user_id: str) -> None:
        """
        Creates a new simulation record with PENDING status.
        """
        client = get_supabase_client()
        row = {
            "id": simulation_id,
            "status": "PENDING",
            "project_data": project_data,  # Supabase JSONB column
            "user_id": user_id,            # Required for RLS
            "result": None,
        }
        client.table(self.table).insert(row).execute()

    def get(
        self, simulation_id: str, user_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves a simulation by ID, optionally scoped to a user.
        """
        client = get_supabase_client()
        query = client.table(self.table).select("*").eq("id", simulation_id)
        if user_id:
            query = query.eq("user_id", user_id)

        response = query.execute()
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

    def get_latest(self, user_id: str, limit: int = 1) -> List[Dict[str, Any]]:
        """
        Fetch the most recent simulations for a specific user.
        """
        client = get_supabase_client()
        response = (
            client.table(self.table)
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data if response.data else []


class WizardSessionRepository:
    """
    Repositório para persistência de sessões do Wizard TIV.

    Substitui o dicionário in-memory por armazenamento no Supabase,
    garantindo que sessões não sejam perdidas em restarts do servidor.

    Tabela necessária no Supabase:
    CREATE TABLE wizard_sessions (
        id TEXT PRIMARY KEY,
        user_id UUID NOT NULL REFERENCES auth.users(id),
        project_name TEXT NOT NULL,
        municipality TEXT,
        steps JSONB DEFAULT '{}',
        current_step TEXT DEFAULT 'p1',
        status TEXT DEFAULT 'active',
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );

    -- RLS Policy
    ALTER TABLE wizard_sessions ENABLE ROW LEVEL SECURITY;
    CREATE POLICY "Users can manage their own sessions"
        ON wizard_sessions FOR ALL
        USING (auth.uid() = user_id);
    """

    def __init__(self):
        self.table = "wizard_sessions"

    def create(
        self,
        user_id: str,
        project_name: str,
        municipality: str = ""
    ) -> Dict[str, Any]:
        """
        Cria uma nova sessão do wizard.

        Returns:
            Dict com session_id e dados da sessão
        """
        session_id = str(uuid.uuid4())[:8].upper()

        client = get_supabase_client()
        row = {
            "id": session_id,
            "user_id": user_id,
            "project_name": project_name,
            "municipality": municipality,
            "steps": {},
            "current_step": "p1",
            "status": "active",
        }

        try:
            client.table(self.table).insert(row).execute()
            return {
                "session_id": session_id,
                "status": "created",
                **row
            }
        except Exception as e:
            # Fallback: se tabela não existir, usar in-memory
            print(f"[WIZARD] DB insert failed, using in-memory: {e}")
            return {
                "session_id": session_id,
                "status": "created_in_memory",
                "warning": "Database table not found. Session will be lost on restart.",
                **row
            }

    def get(self, session_id: str, user_id: str = None) -> Optional[Dict[str, Any]]:
        """
        Busca uma sessão pelo ID.
        """
        client = get_supabase_client()

        try:
            query = client.table(self.table).select("*").eq("id", session_id)
            if user_id:
                query = query.eq("user_id", user_id)

            response = query.execute()

            if response.data and len(response.data) > 0:
                return response.data[0]
        except Exception as e:
            print(f"[WIZARD] DB get failed: {e}")

        return None

    def save_step(
        self,
        session_id: str,
        step: str,
        data: Dict[str, Any],
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Salva os dados de uma etapa específica.
        """
        client = get_supabase_client()

        try:
            # Buscar sessão atual
            session = self.get(session_id, user_id)
            if not session:
                return {"status": "error", "message": "Session not found"}

            # Atualizar steps
            steps = session.get("steps", {})
            steps[step] = data

            # Salvar no banco
            client.table(self.table).update({
                "steps": steps,
                "current_step": step,
                "updated_at": datetime.utcnow().isoformat()
            }).eq("id", session_id).execute()

            return {"status": "saved", "step": step}

        except Exception as e:
            print(f"[WIZARD] DB save_step failed: {e}")
            return {"status": "error", "message": str(e)}

    def get_user_sessions(
        self,
        user_id: str,
        status: str = "active",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Lista sessões do usuário.
        """
        client = get_supabase_client()

        try:
            response = (
                client.table(self.table)
                .select("id, project_name, municipality, current_step, status, created_at, updated_at")
                .eq("user_id", user_id)
                .eq("status", status)
                .order("updated_at", desc=True)
                .limit(limit)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[WIZARD] DB get_user_sessions failed: {e}")
            return []

    def complete_session(self, session_id: str, user_id: str = None) -> Dict[str, Any]:
        """
        Marca uma sessão como completa.
        """
        client = get_supabase_client()

        try:
            client.table(self.table).update({
                "status": "completed",
                "updated_at": datetime.utcnow().isoformat()
            }).eq("id", session_id).execute()

            return {"status": "completed", "session_id": session_id}
        except Exception as e:
            print(f"[WIZARD] DB complete_session failed: {e}")
            return {"status": "error", "message": str(e)}

    def delete_session(self, session_id: str, user_id: str) -> Dict[str, Any]:
        """
        Remove uma sessão (soft delete via status).
        """
        client = get_supabase_client()

        try:
            client.table(self.table).update({
                "status": "deleted",
                "updated_at": datetime.utcnow().isoformat()
            }).eq("id", session_id).eq("user_id", user_id).execute()

            return {"status": "deleted", "session_id": session_id}
        except Exception as e:
            print(f"[WIZARD] DB delete_session failed: {e}")
            return {"status": "error", "message": str(e)}
