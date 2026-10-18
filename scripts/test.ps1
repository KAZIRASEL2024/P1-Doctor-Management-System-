# test.ps1 — Run backend tests inside Docker
# Usage: .\scripts\test.ps1

Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "🧪 Running backend tests..." -ForegroundColor Cyan

# Install aiosqlite for test DB driver if needed, then run pytest
docker compose -f docker-compose.yml -f docker-compose.dev.yml run --rm backend `
    sh -c "pip install aiosqlite pytest-asyncio --quiet && pytest tests/ -v --tb=short"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All tests passed." -ForegroundColor Green
} else {
    Write-Host "❌ Some tests failed." -ForegroundColor Red
    exit 1
}
