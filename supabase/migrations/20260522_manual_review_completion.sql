-- ============================================================================
-- VERTIV V7 - Manual review completion for MANUAL_ASSISTED ingestions
-- Additive metadata and audit action support. RLS policies remain unchanged.
-- ============================================================================

ALTER TABLE data_room_ingestions
  ADD COLUMN IF NOT EXISTS manual_review_completed_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS manual_review_completed_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS manual_review_verdict TEXT CHECK (
    manual_review_verdict IS NULL OR manual_review_verdict IN (
      'APPROVE_WITH_NOTES',
      'REJECT',
      'REQUEST_REUPLOAD'
    )
  ),
  ADD COLUMN IF NOT EXISTS manual_review_notes TEXT,
  ADD COLUMN IF NOT EXISTS manual_review_corrected_payload JSONB;

DO $$
DECLARE
  action_constraint_name TEXT;
BEGIN
  SELECT c.conname
    INTO action_constraint_name
  FROM pg_constraint c
  JOIN pg_class t ON t.oid = c.conrelid
  JOIN pg_namespace n ON n.oid = t.relnamespace
  WHERE n.nspname = 'public'
    AND t.relname = 'data_room_ingestion_events'
    AND c.contype = 'c'
    AND pg_get_constraintdef(c.oid) LIKE '%REQUEST_MANUAL_AUDIT%'
    AND pg_get_constraintdef(c.oid) LIKE '%CONFIRM_SENTENCE%'
  LIMIT 1;

  IF action_constraint_name IS NOT NULL THEN
    EXECUTE format(
      'ALTER TABLE data_room_ingestion_events DROP CONSTRAINT %I',
      action_constraint_name
    );
  END IF;
END $$;

ALTER TABLE data_room_ingestion_events
  ADD CONSTRAINT data_room_ingestion_events_action_check
  CHECK (
    action IN (
      'REQUEST_MANUAL_AUDIT',
      'COMPLETE_MANUAL_REVIEW',
      'CONFIRM_SENTENCE'
    )
  );

-- ============================================================================
-- DONE. Corrected payload is preserved separately from llm_extracted_payload.
-- ============================================================================
