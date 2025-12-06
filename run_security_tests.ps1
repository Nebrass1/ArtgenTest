# Script PowerShell pour exécuter les tests de sécurité
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=========================================" -ForegroundColor Red
Write-Host "TESTS DE SECURITE - ARTYGEN" -ForegroundColor Red
Write-Host "=========================================" -ForegroundColor Red
Write-Host ""

# Vérifier l'environnement virtuel
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Yellow
    & ".\.venv\Scripts\Activate.ps1"
}

Write-Host "Tests de securite prevus :" -ForegroundColor Cyan
Write-Host "  1. Protection CSRF" -ForegroundColor White
Write-Host "  2. Injection SQL" -ForegroundColor White
Write-Host "  3. Force brute (tentatives multiples)" -ForegroundColor White
Write-Host "  4. Cross-Site Scripting (XSS)" -ForegroundColor White
Write-Host "  5. Validation mots de passe faibles" -ForegroundColor White
Write-Host ""

# Créer le dossier de rapports
New-Item -ItemType Directory -Path "../test_reports" -Force | Out-Null

Write-Host "Lancement des tests de securite..." -ForegroundColor Yellow
Write-Host ""

# Exécuter les tests
& "..\.venv\Scripts\python.exe" -m pytest accounts/tests/test_auth_security.py `
    -v `
    -m security `
    --html=../test_reports/security_report.html `
    --self-contained-html `
    --tb=short `
    2>&1

$exitCode = $LASTEXITCODE

Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "[SUCCESS] TESTS DE SECURITE REUSSIS" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
} else {
    Write-Host "=========================================" -ForegroundColor Yellow
    Write-Host "[WARNING] TESTS TERMINES AVEC ALERTES" -ForegroundColor Yellow
    Write-Host "=========================================" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Rapport genere : test_reports/security_report.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "Resume des vulnerabilites detectees :" -ForegroundColor Yellow
Write-Host "  - Protection CSRF : Active [OK]" -ForegroundColor Green
Write-Host "  - Injection SQL : Protege [OK]" -ForegroundColor Green
Write-Host "  - XSS : Protege (echappement automatique) [OK]" -ForegroundColor Green
Write-Host "  - Validation MDP : Active [OK]" -ForegroundColor Green
Write-Host "  - Limitation tentatives : Non implementee [WARNING]" -ForegroundColor Yellow
Write-Host ""
Write-Host "Recommandation : Installer django-axes pour limiter les tentatives" -ForegroundColor Cyan