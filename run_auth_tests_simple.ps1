# Script rapide pour tests d'authentification unitaires
Write-Host ""
Write-Host "=================================" -ForegroundColor Green
Write-Host "TESTS - ARTYGEN" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""

# Vérification environnement
if (-not (Test-Path "..\.venv\Scripts\python.exe")) {
    Write-Host "[ERROR] Environnement virtuel manquant" -ForegroundColor Red
    exit 1
}

Write-Host "[INFO] Lancement des tests unitaires..." -ForegroundColor Cyan
Write-Host ""

# Créer dossier rapports
New-Item -ItemType Directory -Path "../test_reports" -Force | Out-Null

# Exécuter les tests unitaires rapidement
& "..\.venv\Scripts\python.exe" -m pytest accounts/tests/test_auth_unit.py -v --html=../test_reports/quick_test_report.html --self-contained-html --tb=short

Write-Host ""
if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCCESS] Tests unitaires reussis!" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Certains tests ont echoue" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Rapport: test_reports/quick_test_report.html" -ForegroundColor Cyan
Write-Host ""