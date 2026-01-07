# VERTIV v6.0 - Production Deployment (Custom Domain)
# Deploys Frontend with API pointing to api.vertiv.tech

$REGION = "us-central1"
$PROJECT_ID = "vertiv-prod-v1"
$API_URL = "https://api.vertiv.tech"

Write-Host ">>> Deploying VERTIV v6.0 for vertiv.tech..." -ForegroundColor Cyan

# 1. Deploy Backend (No changes needed, just ensuring it's running)
# We assume backend is already live.

# 2. Deploy Frontend with new API URL
Write-Host "Building and Deploying Frontend pointing to $API_URL..."
gcloud builds submit . --config docker/frontend.cloudbuild.yaml --project $PROJECT_ID --substitutions=_NEXT_PUBLIC_API_URL=$API_URL

# 3. Deploy to Cloud Run
Write-Host "Deploying container image to Cloud Run..."
gcloud run deploy vertiv-frontend `
  --image gcr.io/$PROJECT_ID/vertiv-frontend `
  --platform managed `
  --region $REGION `
  --project $PROJECT_ID `
  --allow-unauthenticated

Write-Host ">>> Production Deployment Complete." -ForegroundColor Green
Write-Host "Frontend is now configured to talk to $API_URL"
