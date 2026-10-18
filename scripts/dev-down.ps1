# dev-down.ps1 — Stop the development stack
# Usage: .\scripts\dev-down.ps1

Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "🛑 Stopping BRAC AISP Doctor Management System..." -ForegroundColor Yellow

docker compose -f docker-compose.yml -f docker-compose.dev.yml down

Write-Host "✅ All services stopped." -ForegroundColor Green
Write-Host "   Database volume is preserved. Use reset-demo.ps1 to wipe it." -ForegroundColor Gray
