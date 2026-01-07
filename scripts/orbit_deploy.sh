#!/bin/bash
set -e

PROJECT_ID="vertiv-prod-v1"
REGION="us-central1"

echo "=================================================="
echo "VERTIV v6.1.0-SINGULARITY - ORBIT DEPLOY"
echo "=================================================="

# 1. Build & Push Backend
echo "[1/3] Building Backend..."
gcloud builds submit . \
  --project $PROJECT_ID \
  --config docker/backend.cloudbuild.yaml

# 2. Build & Push Worker
echo "[2/3] Building Worker..."
gcloud builds submit . \
  --project $PROJECT_ID \
  --config docker/worker.cloudbuild.yaml

# 3. Build & Push Frontend (with env vars)
echo "[3/3] Building Frontend..."
gcloud builds submit . \
  --project $PROJECT_ID \
  --config docker/frontend.cloudbuild.yaml \
  --substitutions=_NEXT_PUBLIC_API_URL="https://api.vertiv.tech",_NEXT_PUBLIC_SUPABASE_URL="https://nutilcpmpapjowqmxoqf.supabase.co",_NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51dGlsY3BtcGFwam93cW14b3FmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU5NDg1OTksImV4cCI6MjA4MTUyNDU5OX0.VhvEhOJOLc_Xkf2BvMQs4IbqcJtnmSEXPNfMwvuPXgY"

# 4. Deploy Cloud Run Services
echo "=================================================="
echo "Deploying Services to Cloud Run..."
echo "=================================================="

gcloud run deploy vertiv-backend \
  --image gcr.io/$PROJECT_ID/vertiv-backend \
  --platform managed \
  --region $REGION \
  --project $PROJECT_ID \
  --allow-unauthenticated \
  --set-env-vars ENV=production,WORKER_URL=https://vertiv-worker-442551641682.us-central1.run.app

gcloud run deploy vertiv-worker \
  --image gcr.io/$PROJECT_ID/vertiv-worker \
  --platform managed \
  --region $REGION \
  --project $PROJECT_ID \
  --no-allow-unauthenticated

gcloud run deploy vertiv-frontend \
  --image gcr.io/$PROJECT_ID/vertiv-frontend \
  --platform managed \
  --region $REGION \
  --project $PROJECT_ID \
  --allow-unauthenticated \
  --port 8080

echo "=================================================="
echo "SINGULARITY DEPLOYED!"
echo "Frontend: https://vertiv.tech"
echo "API: https://api.vertiv.tech"
echo "=================================================="
