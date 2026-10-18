# reset-demo.ps1 — Wipe the database and re-seed fresh demo data
# Usage: .\scripts\reset-demo.ps1
#
# WARNING: This deletes ALL data in the development database.

Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "⚠️  This will ERASE all data and re-seed demo data." -ForegroundColor Red
$confirm = Read-Host "Type 'yes' to continue"

if ($confirm -ne "yes") {
    Write-Host "Aborted." -ForegroundColor Gray
    exit 0
}

Write-Host "🗑️  Removing database volume..." -ForegroundColor Yellow
docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v

Write-Host "🚀 Starting fresh stack..." -ForegroundColor Green
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

Write-Host "⏳ Waiting for backend to be ready..." -ForegroundColor Cyan
Start-Sleep -Seconds 15

Write-Host ""
Write-Host "✅ Demo data has been reset." -ForegroundColor Green
Write-Host "   🌐 Frontend → http://localhost:3000" -ForegroundColor Cyan
Write-Host "   📋 Login: admin@brac-aisp.org / Admin@1234" -ForegroundColor Yellow
