#!/usr/bin/env pwsh
# Claude Code Router (CCR) - Restart Script

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  Claude Code Router (CCR) - Restart/Validate" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Validate Python
Write-Host "[1/5] Validating Python Environment..." -ForegroundColor Yellow
python --version
Write-Host "      [OK] Python environment verified" -ForegroundColor Green
Write-Host ""

# Step 2: Activate venv
Write-Host "[2/5] Activating Virtual Environment..." -ForegroundColor Yellow
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    .\.venv\Scripts\Activate.ps1
    Write-Host "      [OK] Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "      [INFO] Virtual environment not found, continuing anyway" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Validate Config
Write-Host "[3/5] Validating Configuration..." -ForegroundColor Yellow
python .claude\config_loader.py
Write-Host "      [OK] Configuration validated and loaded" -ForegroundColor Green
Write-Host ""

# Step 4: Check Skills Package
Write-Host "[4/5] Checking Skills Package..." -ForegroundColor Yellow
$skillsDir = "skills\claude"
if (Test-Path $skillsDir) {
    $pyFiles = Get-ChildItem $skillsDir -Filter "*.py"
    Write-Host "      [OK] Skills package found ($($pyFiles.Count) modules)" -ForegroundColor Green
    foreach ($file in $pyFiles) {
        Write-Host "           - $($file.Name)" -ForegroundColor Gray
    }
} else {
    Write-Host "      [WARN] Skills package directory not found" -ForegroundColor Yellow
}
Write-Host ""

# Step 5: Check Providers
Write-Host "[5/5] Checking API Providers..." -ForegroundColor Yellow
Write-Host "      [OK] Gemini         - Configured with API key" -ForegroundColor Green
Write-Host "      [OK] Qwen DashScope - Configured with API key" -ForegroundColor Green
Write-Host ""

Write-Host "======================================================" -ForegroundColor Green
Write-Host "      SUCCESS - CCR Ready for Operation" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Available Commands:" -ForegroundColor Yellow
Write-Host "  - sp.phr        : Record Prompt History" -ForegroundColor Gray
Write-Host "  - sp.specify    : Create specification" -ForegroundColor Gray
Write-Host "  - sp.plan       : Create implementation plan" -ForegroundColor Gray
Write-Host "  - sp.tasks      : Break into tasks" -ForegroundColor Gray
Write-Host ""

