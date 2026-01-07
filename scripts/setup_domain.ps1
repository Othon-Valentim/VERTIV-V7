# VERTIV v6.0 - Domain Setup Script
# Run this as Administrator

$REGION = "us-central1"
$PROJECT_ID = "vertiv-prod-v1"

Write-Host ">>> Mapping domains for VERTIV v6.0..." -ForegroundColor Cyan

# 1. Map Frontend -> vertiv.tech
Write-Host "Mapping vertiv.tech to vertiv-frontend..."
gcloud beta run domain-mappings create --service vertiv-frontend --domain vertiv.tech --region $REGION --platform managed --project $PROJECT_ID

# 2. Map Frontend -> www.vertiv.tech
Write-Host "Mapping www.vertiv.tech to vertiv-frontend..."
gcloud beta run domain-mappings create --service vertiv-frontend --domain www.vertiv.tech --region $REGION --platform managed --project $PROJECT_ID

# 3. Map Backend -> api.vertiv.tech
Write-Host "Mapping api.vertiv.tech to vertiv-backend..."
gcloud beta run domain-mappings create --service vertiv-backend --domain api.vertiv.tech --region $REGION --platform managed --project $PROJECT_ID

Write-Host ">>> Domain mapping commands executed." -ForegroundColor Green
Write-Host "IMPORTANT: You must now go to your DNS Provider (GoDaddy, Namecheap, etc.) and add the DNS records shown in the output above." -ForegroundColor Yellow
