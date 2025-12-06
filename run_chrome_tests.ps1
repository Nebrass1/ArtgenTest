# Script PowerShell simplifié pour tests Chrome uniquement
Write-Host ""
Write-Host "================================" -ForegroundColor Blue
Write-Host "TESTS CHROME - ARTYGEN" -ForegroundColor Blue
Write-Host "================================" -ForegroundColor Blue
Write-Host ""

# Vérifier Chrome
Write-Host "Recherche de Chrome..." -ForegroundColor Cyan

$chromePaths = @(
    "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe", 
    "${env:LOCALAPPDATA}\Google\Chrome\Application\chrome.exe"
)

$chromeFound = $false
foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        Write-Host "[OK] Chrome trouve: $path" -ForegroundColor Green
        $chromeFound = $true
        break
    }
}

if (-not $chromeFound -and (Get-Command chrome -ErrorAction SilentlyContinue)) {
    Write-Host "[OK] Chrome detecte via PATH" -ForegroundColor Green
    $chromeFound = $true
}

if (-not $chromeFound) {
    Write-Host "[ERROR] Chrome non trouve" -ForegroundColor Red
    Write-Host "[INFO] Installez Chrome: https://www.google.com/chrome/" -ForegroundColor Yellow
    Write-Host "[INFO] Execution des tests unitaires a la place..." -ForegroundColor Cyan
    
    & "..\.venv\Scripts\python.exe" -m pytest accounts/tests/test_auth_unit.py -v --html=../test_reports/unit_only_report.html --self-contained-html
    exit 0
}

# Vérifier l'environnement Python
Write-Host ""
Write-Host "Verification Python..." -ForegroundColor Cyan
if (Test-Path "..\.venv\Scripts\python.exe") {
    Write-Host "[OK] Environnement virtuel OK" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Environnement virtuel manquant" -ForegroundColor Red
    exit 1
}

# Installer les dépendances nécessaires
Write-Host ""
Write-Host "Installation des dependances Chrome..." -ForegroundColor Yellow
& "..\.venv\Scripts\python.exe" -m pip install --quiet selenium webdriver-manager pytest-html

# Créer le dossier de rapports
New-Item -ItemType Directory -Path "../test_reports" -Force | Out-Null

Write-Host ""
Write-Host "Lancement des tests Chrome..." -ForegroundColor Green
Write-Host ""

# Exécuter seulement les tests Chrome
& "..\.venv\Scripts\python.exe" -m pytest accounts/tests/test_auth_cross_browser.py -k "chrome" -v --html=../test_reports/chrome_report.html --self-contained-html

Write-Host ""
if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCCESS] TESTS CHROME REUSSIS!" -ForegroundColor Green
} elseif ($LASTEXITCODE -eq 5) {
    Write-Host "[INFO] Aucun test Chrome execute" -ForegroundColor Yellow
} else {
    Write-Host "[WARNING] Certains tests ont echoue" -ForegroundColor Yellow
}

Write-Host "Rapport: test_reports/chrome_report.html" -ForegroundColor Cyan
Write-Host ""