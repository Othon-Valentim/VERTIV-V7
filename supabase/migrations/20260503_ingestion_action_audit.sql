-- ============================================================================
-- VERTIV V7 - Ingestion human actions audit trail
-- Additive migration for manual audit requests and sentence confirmations.
-- ============================================================================

ALTER TABLE data_room_ingestions
  ADD COLUMN IF NOT EXISTS manual_audit_requested_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS manual_audit_requested_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS sentence_confirmed_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS sentence_confirmed_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS sentence_confirmation_notes TEXT;

CREATE TABLE IF NOT EXISTS data_room_ingestion_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ingestion_id UUID NOT NULL REFERENCES data_room_ingestions(id) ON DELETE CASCADE,
  actor_user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  actor_email TEXT,
  action TEXT NOT NULL CHECK (
    action IN (
      'REQUEST_MANUAL_AUDIT',
      'CONFIRM_SENTENCE'
    )
  ),
  action_status TEXT NOT NULL DEFAULT 'applied' CHECK (
    action_status IN (
      'applied',
      'idempotent_noop'
    )
  ),
  previous_status TEXT,
  new_status TEXT,
  idempotency_key_hash TEXT,
  request_id TEXT,
  ip_hash TEXT,
  user_agent TEXT,
  payload_redacted JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_data_room_ingestion_events_idempotency
  ON data_room_ingestion_events (ingestion_id, action, idempotency_key_hash)
  WHERE idempotency_key_hash IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_data_room_ingestion_events_ingestion_id
  ON data_room_ingestion_events (ingestion_id, created_at DESC);

ALTER TABLE data_room_ingestion_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users see own ingestion events"
  ON data_room_ingestion_events FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1
      FROM data_room_ingestions i
      WHERE i.id = data_room_ingestion_events.ingestion_id
        AND i.user_id = auth.uid()
    )
  );

CREATE POLICY "Service role manages ingestion events"
  ON data_room_ingestion_events FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- ============================================================================
-- DONE. Status remains the pipeline/triage state; human decisions are metadata.
-- ============================================================================
