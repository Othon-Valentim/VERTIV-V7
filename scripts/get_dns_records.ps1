# Helper script to show DNS records for VERTIV domains
# Run as Administrator if you see permission errors

$REGION = "us-central1"
$PROJECT_ID = "vertiv-prod-v1"

Write-Host ">>> Retrieving DNS Records for vertiv.tech domains..." -ForegroundColor Cyan

function Get-Records($domain) {
    Write-Host "`n----------------------------------------"
    Write-Host "DOMAIN: $domain" -ForegroundColor Yellow
    Write-Host "----------------------------------------"
    
    try {
        # Fetch the full description
        gcloud beta run domain-mappings describe --domain $domain --region $REGION --platform managed --project $PROJECT_ID --format="value(status.resourceRecords)" 2>$null | Out-String | Write-Host
        
        Write-Host "If the output above is empty, the mapping might not exist yet." -ForegroundColor DarkGray
    } catch {
        Write-Host "Error retrieving records. Make sure the mapping exists." -ForegroundColor Red
    }
}

Get-Records "vertiv.tech"
Get-Records "www.vertiv.tech"
Get-Records "api.vertiv.tech"

Write-Host "`n>>> Instructions:" -ForegroundColor Cyan
Write-Host "1. Look for 'rrdata' (The value) and 'type' (Usually A or CNAME)."
Write-Host "2. Add these records to your DNS provider."
Write-Host "   - Type 'A': Map host to the IP address."
Write-Host "   - Type 'CNAME': Map host to the target domain (e.g., ghs.googlehosted.com)."
