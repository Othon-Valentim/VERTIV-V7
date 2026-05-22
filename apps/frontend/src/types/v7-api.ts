export type IngestionStatus =
  | "UPLOADING"
  | "INGESTING"
  | "AUTONOMOUS_SENTENCED"
  | "PENDING_HUMAN_AUDIT"
  | "MANUAL_ASSISTED"
  | "KILLED"
  | "FAILED";

export interface IngestResponse {
  ingestion_id: string;
  status: IngestionStatus;
  message: string;
}

export interface IngestionDetail {
  id: string;
  status: IngestionStatus;
  raw_storage_url?: string | null;
  llm_extracted_payload?: Record<string, unknown> | null;
  polars_calculations?: Record<string, unknown> | null;
  kill_reasons?: unknown[] | null;
  legacy_simulation_id?: string | null;
  accuracy_score?: number | null;
  validation_metrics?: Record<string, unknown> | null;
  manual_audit_requested_at?: string | null;
  manual_audit_requested_by?: string | null;
  sentence_confirmed_at?: string | null;
  sentence_confirmed_by?: string | null;
  sentence_confirmation_notes?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
}

export interface ManualAuditRequest {
  reason?: string | null;
  expected_status?: IngestionStatus | string | null;
  idempotency_key?: string | null;
}

export interface ConfirmSentenceRequest {
  accepted: true;
  notes?: string | null;
  expected_status?: IngestionStatus | string | null;
  decision_snapshot_hash?: string | null;
  idempotency_key?: string | null;
}

export type IngestionActionStatus = "applied" | "idempotent_noop";
export type IngestionAction =
  | "REQUEST_MANUAL_AUDIT"
  | "CONFIRM_SENTENCE";

export interface IngestionActionResponse {
  ingestion_id: string;
  action: IngestionAction;
  action_status: IngestionActionStatus;
  previous_status: IngestionStatus | string;
  current_status: IngestionStatus | string;
  audit_event_id?: string | null;
  manual_audit_requested_at?: string | null;
  sentence_confirmed_at?: string | null;
  sentence_confirmed_by?: string | null;
  updated_at?: string | null;
}
