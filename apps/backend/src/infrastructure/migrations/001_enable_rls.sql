-- Enable RLS
ALTER TABLE simulations ENABLE ROW LEVEL SECURITY;

-- Creating Policy: Select Own Data
CREATE POLICY "Users can only see their own simulations"
ON simulations
FOR SELECT
USING (auth.uid() = user_id);

-- Creating Policy: Insert Own Data
CREATE POLICY "Users can insert their own simulations"
ON simulations
FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Creating Policy: Update Own Data (for Worker/System which uses Service Role, it bypasses RLS)
-- But for users, they might update metadata?
-- For now, allow Users to update their own.
CREATE POLICY "Users can update their own simulations"
ON simulations
FOR UPDATE
USING (auth.uid() = user_id);

-- Note: The Worker/Backend uses the SERVICE_ROLE_KEY which bypasses RLS.
-- This ensures the backend can always write results.
