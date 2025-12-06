# Script PowerShell pour executer les tests multi-navigateurs
# Configuration de l'encodage
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🌐 TESTS MULTI-NAVIGATEURS - ARTYGEN" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Verifier l'environnement virtuel
if ($env:VIRTUAL_ENV) {
    Write-Host "✅ Environnement virtuel actif: $env:VIRTUAL_ENV" -ForegroundColor Green
} elseif (Test-Path "..\.venv\Scripts\python.exe") {
    Write-Host "⚠️  Activation de l'environnement virtuel..." -ForegroundColor Yellow
} else {
    Write-Host "❌ Environnement virtuel non trouve" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 Installation des dependances..." -ForegroundColor Yellow
& "..\.venv\Scripts\python.exe" -m pip install --quiet webdriver-manager selenium pytest-html

Write-Host ""
Write-Host "Verification des navigateurs disponibles..."

# Test de disponibilite des navigateurs
$browsersAvailable = @()

# Chrome
try {
    $chromePath = Get-Command chrome -ErrorAction SilentlyContinue
    if ($chromePath) {
        Write-Host "  [OK] Chrome detecte"
        $browsersAvailable += "Chrome"
    }
} catch {
    Write-Host "  [INFO] Chrome non detecte"
}

# Firefox
try {
    $firefoxPath = Get-Command firefox -ErrorAction SilentlyContinue
    if ($firefoxPath) {
        Write-Host "  [OK] Firefox detecte"
        $browsersAvailable += "Firefox"
    }
} catch {
    Write-Host "  [INFO] Firefox non detecte"
}

# Edge
try {
    $edgePath = Get-Command msedge -ErrorAction SilentlyContinue
    if ($edgePath) {
        Write-Host "  [OK] Edge detecte" 
        $browsersAvailable += "Edge"
    }
} catch {
    Write-Host "  [INFO] Edge non detecte"
}

Write-Host ""
Write-Host "Navigateurs disponibles: $($browsersAvailable -join ', ')"

Write-Host ""
Write-Host "========================================="
Write-Host "LANCEMENT DES TESTS"
Write-Host "========================================="
Write-Host ""

# Creer le dossier de rapports s'il n'existe pas
New-Item -ItemType Directory -Path "../test_reports" -Force | Out-Null

# Lancer les tests multi-navigateurs
Write-Host "Execution des tests de compatibilite..."
& "..\.venv\Scripts\python.exe" -m pytest accounts/tests/test_auth_cross_browser.py -v --html=../test_reports/cross_browser_report.html --self-contained-html --tb=short

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================="
    Write-Host "[SUCCESS] TESTS MULTI-NAVIGATEURS REUSSIS"
    Write-Host "========================================="
    Write-Host ""
    Write-Host "Rapport genere: test_reports/cross_browser_report.html"
} else {
    Write-Host ""
    Write-Host "========================================="
    Write-Host "[WARNING] CERTAINS TESTS ONT ECHOUE"
    Write-Host "========================================="
    Write-Host ""
    Write-Host "Consultez le rapport: test_reports/cross_browser_report.html"
}

Write-Host ""
Write-Host "Note: Les tests s'executent en mode headless"