-- Harden RLS policies for data_room_ingestions and data-rooms storage.
-- This script is safe to rerun and intentionally grants no anon access.

ALTER TABLE data_room_ingestions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users see own ingestions" ON data_room_ingestions;
DROP POLICY IF EXISTS "Users create own ingestions" ON data_room_ingestions;
DROP POLICY IF EXISTS "Service role full access" ON data_room_ingestions;
DROP POLICY IF EXISTS "Allow authenticated insert" ON data_room_ingestions;
DROP POLICY IF EXISTS "Allow authenticated select" ON data_room_ingestions;
DROP POLICY IF EXISTS "Allow service update" ON data_room_ingestions;
DROP POLICY IF EXISTS "Allow anon update" ON data_room_ingestions;
DROP POLICY IF EXISTS "Allow anon insert" ON data_room_ingestions;
DROP POLICY IF EXISTS "Allow anon select" ON data_room_ingestions;

CREATE POLICY "Users see own ingestions"
ON data_room_ingestions
FOR SELECT
TO authenticated
USING (auth.uid() = user_id);

CREATE POLICY "Users create own ingestions"
ON data_room_ingestions
FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Service role full access"
ON data_room_ingestions
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

INSERT INTO storage.buckets (id, name, public)
VALUES ('data-rooms', 'data-rooms', false)
ON CONFLICT (id) DO NOTHING;

DO $$
BEGIN
  DROP POLICY IF EXISTS "Allow authenticated upload" ON storage.objects;
  DROP POLICY IF EXISTS "Allow authenticated read" ON storage.objects;
  DROP POLICY IF EXISTS "Allow anon upload" ON storage.objects;
  DROP POLICY IF EXISTS "Allow anon read" ON storage.objects;
  DROP POLICY IF EXISTS "Users upload own data rooms" ON storage.objects;
  DROP POLICY IF EXISTS "Users read own data rooms" ON storage.objects;
  DROP POLICY IF EXISTS "Service role manages data rooms" ON storage.objects;

  CREATE POLICY "Users upload own data rooms"
  ON storage.objects
  FOR INSERT
  TO authenticated
  WITH CHECK (
    bucket_id = 'data-rooms'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

  CREATE POLICY "Users read own data rooms"
  ON storage.objects
  FOR SELECT
  TO authenticated
  USING (
    bucket_id = 'data-rooms'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

  CREATE POLICY "Service role manages data rooms"
  ON storage.objects
  FOR ALL
  TO service_role
  USING (bucket_id = 'data-rooms')
  WITH CHECK (bucket_id = 'data-rooms');
END $$;
