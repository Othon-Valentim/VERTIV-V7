-- ============================================================================
-- VERTIV v6.1.0-SINGULARITY - Load Test Cleanup Script
-- ============================================================================
-- This script removes test data created during load testing.
-- Run this after completing load tests to clean up the database.
-- ============================================================================

-- Safety check: Only run in non-production or with explicit confirmation
-- Uncomment the line below to enable the script
-- SET @CONFIRM_CLEANUP = TRUE;

-- ============================================================================
-- 1. Delete Load Test Simulations
-- ============================================================================
-- Identifies simulations created by load tests (prefixed with 'proj_flood_' or 'sim_proj_')

DELETE FROM simulations
WHERE id LIKE 'sim_proj_%'
   OR project_data->>'name' LIKE 'Flood Project%'
   OR project_data->>'name' LIKE 'Project Alpha proj_%';

-- ============================================================================
-- 2. Delete Load Test Analyses
-- ============================================================================
-- Identifies analyses created during load tests

DELETE FROM analyses
WHERE name LIKE '%Load Test%'
   OR name LIKE '%Flood Test%'
   OR name LIKE '%Stress Test%';

-- ============================================================================
-- 3. Vacuum and Analyze (PostgreSQL)
-- ============================================================================
-- Reclaim storage and update statistics after bulk delete

VACUUM ANALYZE simulations;
VACUUM ANALYZE analyses;

-- ============================================================================
-- 4. Verification Queries
-- ============================================================================
-- Run these to verify cleanup was successful

-- Count remaining simulations
SELECT COUNT(*) as remaining_simulations FROM simulations;

-- Count remaining analyses
SELECT COUNT(*) as remaining_analyses FROM analyses;

-- Show recent simulations (should be real data only)
SELECT id, status, created_at
FROM simulations
ORDER BY created_at DESC
LIMIT 10;

-- ============================================================================
-- Usage Instructions:
-- ============================================================================
--
-- Option 1: Run via Supabase Dashboard
--   1. Go to SQL Editor in Supabase Dashboard
--   2. Copy and paste this script
--   3. Execute
--
-- Option 2: Run via psql
--   psql -h db.nutilcpmpapjowqmxoqf.supabase.co -U postgres -d postgres -f cleanup_load_test.sql
--
-- Option 3: Run via Python
--   See scripts/run_cleanup.py
--
-- ============================================================================
