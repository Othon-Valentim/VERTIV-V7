$ErrorActionPreference = "Stop"

$PROJECT_ID = "vertiv-prod-v1"
$REGION = "us-central1"
$BACKEND_URL = "https://vertiv-backend-294263810288.us-central1.run.app"
$WORKER_URL = "https://vertiv-worker-294263810288.us-central1.run.app"

Write-Host "🚀 Starting Phase 2 Deployment..." -ForegroundColor Green

# 1. Build Backend
Write-Host "📦 Building Backend..." -ForegroundColor Cyan
gcloud builds submit apps/backend --tag gcr.io/$PROJECT_ID/vertiv-backend --project $PROJECT_ID
if ($LASTEXITCODE -ne 0) { throw "Backend Build Failed" }

# 2. Build Worker
Write-Host "📦 Building Worker..." -ForegroundColor Cyan
gcloud builds submit . --config docker/worker.cloudbuild.yaml --project $PROJECT_ID
if ($LASTEXITCODE -ne 0) { throw "Worker Build Failed" }

# 3. Build Frontend (with API URL baked in)
Write-Host "📦 Building Frontend (Connecting to Backend: $BACKEND_URL)..." -ForegroundColor Cyan
gcloud builds submit . `
    --config docker/frontend.cloudbuild.yaml `
    --project $PROJECT_ID `
    --substitutions=_NEXT_PUBLIC_API_URL=$BACKEND_URL
if ($LASTEXITCODE -ne 0) { throw "Frontend Build Failed" }

# 4. Deploy Services
Write-Host "🚀 Deploying Services to Cloud Run..." -ForegroundColor Cyan

# Deploy Backend (Needs Worker URL + Supabase)
# Note: Assuming secrets are already managed or passed via Env Vars in Dashboard. 
# Re-applying ENV vars to be safe, but NOT overwriting secrets if they exist.
# WARNING: If you haven't set SUPABASE_URL/KEY in Cloud Run secrets yet, this might fail startup if code crashes without them.
# We will set the known non-secret env vars.
gcloud run deploy vertiv-backend `
    --image gcr.io/$PROJECT_ID/vertiv-backend `
    --platform managed `
    --region $REGION `
    --project $PROJECT_ID `
    --allow-unauthenticated `
    --set-env-vars "ENV=PRODUCTION,WORKER_URL=$WORKER_URL"

# Deploy Worker (Needs Supabase)
gcloud run deploy vertiv-worker `
    --image gcr.io/$PROJECT_ID/vertiv-worker `
    --platform managed `
    --region $REGION `
    --project $PROJECT_ID `
    --no-allow-unauthenticated `
    --set-env-vars "ENV=PRODUCTION"

# Deploy Frontend (Runtime vars if needed, but mostly baked in)
gcloud run deploy vertiv-frontend `
    --image gcr.io/$PROJECT_ID/vertiv-frontend `
    --platform managed `
    --region $REGION `
    --project $PROJECT_ID `
    --allow-unauthenticated

Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "Backend: $BACKEND_URL"
Write-Host "Frontend: https://vertiv-frontend-294263810288.us-central1.run.app"
