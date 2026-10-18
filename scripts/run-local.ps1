# run-local.ps1 — Start backend + frontend locally WITHOUT Docker
# Run from the project root: .\scripts\run-local.ps1

Set-Location (Split-Path $PSScriptRoot -Parent)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BRAC AISP DMS — Local Dev Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Using SQLite (no Docker/PostgreSQL needed)" -ForegroundColor Yellow
Write-Host ""

# ── 1. Create SQLite DB tables & seed data ────────────────────────────────
Write-Host "Step 1/3  Creating database tables and seeding demo data..." -ForegroundColor Green
Push-Location backend
$env:DATABASE_URL = "sqlite+aiosqlite:///./local_dev.db"
$env:SECRET_KEY   = "local_dev_secret_key_for_development_only_32chars"
$env:SEED_DEMO_DATA = "true"
$env:ENVIRONMENT  = "development"
$env:BACKEND_CORS_ORIGINS = "http://localhost:3000"
python -m scripts.migrate
if ($LASTEXITCODE -ne 0) {
    Pop-Location
    throw "Database migrations failed."
}
python -m scripts.seed_demo_data
if ($LASTEXITCODE -ne 0) {
    Pop-Location
    throw "Demo data seeding failed."
}
Pop-Location

# ── 2. Start FastAPI backend ───────────────────────────────────────────────
Write-Host ""
Write-Host "Step 2/3  Starting FastAPI backend on http://localhost:8000 ..." -ForegroundColor Green
Push-Location backend
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    $env:DATABASE_URL = "sqlite+aiosqlite:///./local_dev.db"
    $env:SECRET_KEY   = "local_dev_secret_key_for_development_only_32chars"
    $env:SEED_DEMO_DATA = "true"
    $env:ENVIRONMENT  = "development"
    $env:BACKEND_CORS_ORIGINS = "http://localhost:3000"
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}
Pop-Location

# Wait for backend to become ready
Write-Host "   Waiting for backend to start..." -ForegroundColor Gray
Start-Sleep -Seconds 5
$retries = 0
while ($retries -lt 15) {
    try {
        $null = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing -TimeoutSec 2
        Write-Host "   Backend ready!" -ForegroundColor Green
        break
    } catch {
        Start-Sleep -Seconds 2
        $retries++
    }
}

# ── 3. Start Next.js frontend ──────────────────────────────────────────────
Write-Host ""
Write-Host "Step 3/3  Starting Next.js frontend on http://localhost:3000 ..." -ForegroundColor Green
Push-Location frontend
$env:NEXT_PUBLIC_API_BASE_URL = "http://localhost:8000"
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    $env:NEXT_PUBLIC_API_BASE_URL = "http://localhost:8000"
    npm run dev
}
Pop-Location

# Wait for frontend
Start-Sleep -Seconds 8

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  All services started!" -ForegroundColor Green
Write-Host ""
Write-Host "  Dashboard  → http://localhost:3000" -ForegroundColor Cyan
Write-Host "  API Docs   → http://localhost:8000/api/docs" -ForegroundColor Cyan
Write-Host "  Health     → http://localhost:8000/api/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Login: admin@brac-aisp.org / Admin@1234" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop all services." -ForegroundColor Gray

# Open browser
Start-Process "http://localhost:3000"

# Keep alive and stream logs
try {
    while ($true) {
        Receive-Job $backendJob  2>&1 | ForEach-Object { Write-Host "[backend] $_" -ForegroundColor DarkGray }
        Receive-Job $frontendJob 2>&1 | ForEach-Object { Write-Host "[frontend] $_" -ForegroundColor DarkCyan }
        Start-Sleep -Seconds 2
    }
} finally {
    Write-Host "Stopping services..." -ForegroundColor Yellow
    Stop-Job  $backendJob,  $frontendJob
    Remove-Job $backendJob, $frontendJob
    Write-Host "Done." -ForegroundColor Green
}
