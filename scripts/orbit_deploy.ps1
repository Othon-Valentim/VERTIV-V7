$ErrorActionPreference = "Stop"

# ============================================================================
# ORBIT DEPLOY v2.0 - Production Deployment Script (PowerShell)
# ============================================================================

$PROJECT_ID = "vertiv-platform-v5"
$REGION = "southamerica-east1"
$REPO = "vertiv-repo"
$ENV_FILE = ".env.production"

# --- Load Environment Variables from .env.production ---
Write-Host "Loading environment from $ENV_FILE..." -ForegroundColor Yellow
if (-Not (Test-Path $ENV_FILE)) {
    throw "BLOCKER: $ENV_FILE not found. Create it from .env.production.example and fill in secrets."
}

$envVars = @{}
Get-Content $ENV_FILE | ForEach-Object {
    if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        $envVars[$key] = $value
    }
}

# Validate critical secrets
$requiredKeys = @("SUPABASE_URL", "SUPABASE_KEY", "SERPER_API_KEY")
foreach ($key in $requiredKeys) {
    if (-Not $envVars.ContainsKey($key) -or $envVars[$key] -match "YOUR_|your-") {
        throw "BLOCKER: $key is missing or contains placeholder value in $ENV_FILE"
    }
}

Write-Host "Environment loaded. $($envVars.Count) variables found." -ForegroundColor Green

# --- Build Env Vars String for Cloud Run ---
function Build-EnvString {
    param([string[]]$Keys)
    $parts = @()
    foreach ($key in $Keys) {
        if ($envVars.ContainsKey($key)) {
            $parts += "$key=$($envVars[$key])"
        }
    }
    return $parts -join ","
}

$backendEnvKeys = @("ENV", "DEBUG", "SUPABASE_URL", "SUPABASE_KEY", "SUPABASE_JWT_SECRET", "SERPER_API_KEY", "CORS_ORIGINS", "LOG_LEVEL", "ENABLE_LIVE_SEARCH", "ENABLE_REAL_OPTIONS", "ENABLE_ESG_CALCULATION")
$workerEnvKeys = @("ENV", "DEBUG", "SUPABASE_URL", "SUPABASE_KEY", "GCP_PROJECT_ID", "GCP_REGION", "CLOUD_TASKS_QUEUE", "CLOUD_TASKS_LOCATION")
$frontendBuildArgs = "NEXT_PUBLIC_API_URL=$($envVars['API_URL']),NEXT_PUBLIC_SUPABASE_URL=$($envVars['SUPABASE_URL']),NEXT_PUBLIC_SUPABASE_ANON_KEY=$($envVars['SUPABASE_KEY'])"

Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "   LAUNCHING ORBIT DEPLOY v2.0" -ForegroundColor Magenta
Write-Host "========================================`n" -ForegroundColor Magenta

# --- 1. Backend ---
Write-Host "[1/3] Building Backend..." -ForegroundColor Cyan
docker build -t gcr.io/$PROJECT_ID/$REPO/backend:latest -f docker/Dockerfile.backend .
if ($LASTEXITCODE -ne 0) { throw "Backend Build Failed" }

Write-Host "[1/3] Pushing Backend..." -ForegroundColor Cyan
docker push gcr.io/$PROJECT_ID/$REPO/backend:latest
if ($LASTEXITCODE -ne 0) { throw "Backend Push Failed" }

Write-Host "[1/3] Deploying Backend to Cloud Run..." -ForegroundColor Cyan
$backendEnvString = Build-EnvString -Keys $backendEnvKeys
gcloud run deploy vertiv-backend `
    --image gcr.io/$PROJECT_ID/$REPO/backend:latest `
    --region $REGION `
    --platform managed `
    --allow-unauthenticated `
    --set-env-vars $backendEnvString
if ($LASTEXITCODE -ne 0) { throw "Backend Deploy Failed" }

# --- 2. Worker ---
Write-Host "[2/3] Building Worker..." -ForegroundColor Cyan
docker build -t gcr.io/$PROJECT_ID/$REPO/worker:latest -f apps/worker/Dockerfile .
if ($LASTEXITCODE -ne 0) { throw "Worker Build Failed" }

Write-Host "[2/3] Pushing Worker..." -ForegroundColor Cyan
docker push gcr.io/$PROJECT_ID/$REPO/worker:latest
if ($LASTEXITCODE -ne 0) { throw "Worker Push Failed" }

Write-Host "[2/3] Deploying Worker to Cloud Run..." -ForegroundColor Cyan
$workerEnvString = Build-EnvString -Keys $workerEnvKeys
gcloud run deploy vertiv-worker `
    --image gcr.io/$PROJECT_ID/$REPO/worker:latest `
    --region $REGION `
    --platform managed `
    --allow-unauthenticated `
    --set-env-vars $workerEnvString
if ($LASTEXITCODE -ne 0) { throw "Worker Deploy Failed" }

# --- 3. Frontend ---
Write-Host "[3/3] Building Frontend..." -ForegroundColor Cyan
docker build `
    --build-arg NEXT_PUBLIC_API_URL=$($envVars['API_URL']) `
    --build-arg NEXT_PUBLIC_SUPABASE_URL=$($envVars['SUPABASE_URL']) `
    --build-arg NEXT_PUBLIC_SUPABASE_ANON_KEY=$($envVars['SUPABASE_KEY']) `
    -t gcr.io/$PROJECT_ID/$REPO/frontend:latest `
    -f docker/Dockerfile.frontend .
if ($LASTEXITCODE -ne 0) { throw "Frontend Build Failed" }

Write-Host "[3/3] Pushing Frontend..." -ForegroundColor Cyan
docker push gcr.io/$PROJECT_ID/$REPO/frontend:latest
if ($LASTEXITCODE -ne 0) { throw "Frontend Push Failed" }

Write-Host "[3/3] Deploying Frontend to Cloud Run..." -ForegroundColor Cyan
gcloud run deploy vertiv-frontend `
    --image gcr.io/$PROJECT_ID/$REPO/frontend:latest `
    --region $REGION `
    --platform managed `
    --allow-unauthenticated
if ($LASTEXITCODE -ne 0) { throw "Frontend Deploy Failed" }

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "   ORBIT COMPLETE. SYSTEMS ONLINE." -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green
