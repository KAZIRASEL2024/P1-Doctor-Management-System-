# dev-up.ps1 — Start the full development stack
# Usage: .\scripts\dev-up.ps1

param(
    [switch]$Build,      # Force rebuild images
    [switch]$NoDaemon    # Run in foreground (shows all logs)
)

Set-Location (Split-Path $PSScriptRoot -Parent)

# Copy .env if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "📋 Copying .env.example to .env ..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Edit .env and set secure passwords before production use." -ForegroundColor Yellow
}

$composeFiles = "-f docker-compose.yml -f docker-compose.dev.yml"

if ($Build) {
    Write-Host "🔨 Building images..." -ForegroundColor Cyan
    Invoke-Expression "docker compose $composeFiles build"
}

Write-Host "🚀 Starting BRAC AISP Doctor Management System (dev)..." -ForegroundColor Green

if ($NoDaemon) {
    Invoke-Expression "docker compose $composeFiles up"
} else {
    Invoke-Expression "docker compose $composeFiles up -d"
    Write-Host ""
    Write-Host "✅ Services started:" -ForegroundColor Green
    Write-Host "   🌐 Frontend    → http://localhost:3000" -ForegroundColor Cyan
    Write-Host "   ⚡ Backend API → http://localhost:8000/api/docs" -ForegroundColor Cyan
    Write-Host "   🗄️  Database   → localhost:5432 (dms_user)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📋 Demo login: admin@brac-aisp.org / Admin@1234" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To view logs:  docker compose $composeFiles logs -f" -ForegroundColor Gray
    Write-Host "To stop:       .\scripts\dev-down.ps1" -ForegroundColor Gray
}
