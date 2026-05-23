-- ============================================================================
-- VERTIV V7 — Supabase Migration: data_room_ingestions
-- Run this in Supabase SQL Editor BEFORE the Dry Run
-- ============================================================================

-- 1. Create the data_room_ingestions table
CREATE TABLE IF NOT EXISTS data_room_ingestions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  status TEXT NOT NULL DEFAULT 'UPLOADING'
    CHECK (status IN (
      'UPLOADING',
      'INGESTING',
      'AUTONOMOUS_SENTENCED',
      'PENDING_HUMAN_AUDIT',
      'MANUAL_ASSISTED',
      'KILLED',
      'FAILED'
    )),
  raw_storage_url TEXT,
  llm_extracted_payload JSONB,
  polars_calculations JSONB,
  kill_reasons JSONB,
  legacy_simulation_id TEXT,
  accuracy_score FLOAT,
  validation_metrics JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Enable RLS
ALTER TABLE data_room_ingestions ENABLE ROW LEVEL SECURITY;

-- 3. RLS Policies
CREATE POLICY "Users see own ingestions"
  ON data_room_ingestions FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users create own ingestions"
  ON data_room_ingestions FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- 4. Service role can update (Worker uses service_role key)
CREATE POLICY "Service role full access"
  ON data_room_ingestions FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- 5. Auto-update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_data_room_ingestions_updated_at
  BEFORE UPDATE ON data_room_ingestions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- 6. Create private storage bucket and least-privilege policies
INSERT INTO storage.buckets (id, name, public)
VALUES ('data-rooms', 'data-rooms', false)
ON CONFLICT (id) DO NOTHING;

CREATE POLICY "Users upload own data rooms"
  ON storage.objects FOR INSERT
  TO authenticated
  WITH CHECK (
    bucket_id = 'data-rooms'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

CREATE POLICY "Users read own data rooms"
  ON storage.objects FOR SELECT
  TO authenticated
  USING (
    bucket_id = 'data-rooms'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

CREATE POLICY "Service role manages data rooms"
  ON storage.objects FOR ALL
  TO service_role
  USING (bucket_id = 'data-rooms')
  WITH CHECK (bucket_id = 'data-rooms');

-- ============================================================================
-- DONE. The 'data-rooms' bucket is private and scoped by user-id folder.
-- ============================================================================
