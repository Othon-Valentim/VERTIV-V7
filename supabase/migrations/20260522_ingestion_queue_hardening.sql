-- ============================================================================
-- VERTIV V7 - Ingestion queue hardening
-- Adds operational metadata for worker claims, attempts, completion and errors.
-- This migration is additive and does not alter RLS policies.
-- ============================================================================

ALTER TABLE data_room_ingestions
  ADD COLUMN IF NOT EXISTS processing_started_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS processing_finished_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS worker_id TEXT,
  ADD COLUMN IF NOT EXISTS attempt_count INTEGER DEFAULT 0,
  ADD COLUMN IF NOT EXISTS last_error TEXT;

UPDATE data_room_ingestions
SET attempt_count = 0
WHERE attempt_count IS NULL;

ALTER TABLE data_room_ingestions
  ALTER COLUMN attempt_count SET DEFAULT 0,
  ALTER COLUMN attempt_count SET NOT NULL;

ALTER TABLE data_room_ingestions
  ADD CONSTRAINT data_room_ingestions_attempt_count_nonnegative
  CHECK (attempt_count >= 0)
  NOT VALID;

ALTER TABLE data_room_ingestions
  VALIDATE CONSTRAINT data_room_ingestions_attempt_count_nonnegative;
