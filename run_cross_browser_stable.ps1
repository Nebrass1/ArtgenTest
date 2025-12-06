# Script PowerShell pour tests multi-navigateurs - Version stable
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "TESTS MULTI-NAVIGATEURS - ARTYGEN" -ForegroundColor Cyan  
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Fonction pour vérifier un navigateur
function Test-BrowserAvailable {
    param([string]$BrowserName, [string[]]$Paths, [string]$Command)
    
    if ($Command -and (Get-Command $Command -ErrorAction SilentlyContinue)) {
        Write-Host "[OK] $BrowserName detecte (PATH)" -ForegroundColor Green
        return $true
    }
    
    foreach ($path in $Paths) {
        if (Test-Path $path) {
            Write-Host "[OK] $BrowserName trouve" -ForegroundColor Green
            return $true
        }
    }
    
    Write-Host "[INFO] $BrowserName non detecte" -ForegroundColor Yellow
    return $false
}

# Vérification de l'environnement
Write-Host "Verification de l'environnement..." -ForegroundColor Cyan
if (Test-Path "..\.venv\Scripts\python.exe") {
    Write-Host "[OK] Environnement virtuel trouve" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Environnement virtuel manquant" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Installation des dependances..." -ForegroundColor Yellow
& "..\.venv\Scripts\python.exe" -m pip install --quiet selenium webdriver-manager pytest-html pytest-cov

Write-Host ""
Write-Host "Detection des navigateurs..." -ForegroundColor Cyan

# Détection Chrome
$chromePaths = @(
    "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "${env:LOCALAPPDATA}\Google\Chrome\Application\chrome.exe"
)
$chromeAvailable = Test-BrowserAvailable -BrowserName "Chrome" -Paths $chromePaths -Command "chrome"

# Détection Firefox  
$firefoxPaths = @(
    "${env:ProgramFiles}\Mozilla Firefox\firefox.exe",
    "${env:ProgramFiles(x86)}\Mozilla Firefox\firefox.exe"
)
$firefoxAvailable = Test-BrowserAvailable -BrowserName "Firefox" -Paths $firefoxPaths -Command "firefox"

# Détection Edge
$edgePaths = @(
    "${env:ProgramFiles}\Microsoft\Edge\Application\msedge.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
)
$edgeAvailable = Test-BrowserAvailable -BrowserName "Edge" -Paths $edgePaths -Command "msedge"

$totalBrowsers = ($chromeAvailable + $firefoxAvailable + $edgeAvailable)

Write-Host ""
Write-Host "Resume: $totalBrowsers/3 navigateurs disponibles" -ForegroundColor $(
    if ($totalBrowsers -eq 0) {'Red'} 
    elseif ($totalBrowsers -lt 3) {'Yellow'} 
    else {'Green'}
)

# Créer le dossier de rapports
New-Item -ItemType Directory -Path "../test_reports" -Force | Out-Null

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "LANCEMENT DES TESTS" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

if ($totalBrowsers -eq 0) {
    Write-Host "[MODE] Tests unitaires seulement (aucun navigateur)" -ForegroundColor Yellow
    Write-Host "Commande: pytest test_auth_unit.py" -ForegroundColor Gray
    & "..\.venv\Scripts\python.exe" -m pytest accounts/tests/test_auth_unit.py -v --html=../test_reports/unit_fallback_report.html --self-contained-html --cov=accounts --cov-report=html:../test_reports/coverage_unit
    
} elseif ($chromeAvailable -and $totalBrowsers -eq 1) {
    Write-Host "[MODE] Chrome uniquement" -ForegroundColor Yellow
    Write-Host "Commande: pytest -k chrome" -ForegroundColor Gray
    & "..\.venv\Scripts\python.exe" -m pytest accounts/tests/test_auth_cross_browser.py -k "chrome" -v --html=../test_reports/chrome_only_report.html --self-contained-html
    
} else {
    Write-Host "[MODE] Multi-navigateurs complet" -ForegroundColor Green
    Write-Host "Commande: pytest test_auth_cross_browser.py" -ForegroundColor Gray
    & "..\.venv\Scripts\python.exe" -m pytest accounts/tests/test_auth_cross_browser.py -v --html=../test_reports/full_cross_browser_report.html --self-contained-html --tb=short
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Magenta
Write-Host "RESULTATS DES TESTS" -ForegroundColor Magenta
Write-Host "=========================================" -ForegroundColor Magenta

if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCCESS] Tous les tests sont passes!" -ForegroundColor Green
} elseif ($LASTEXITCODE -eq 5) {
    Write-Host "[INFO] Tests sautes (navigateurs indisponibles)" -ForegroundColor Yellow  
} else {
    Write-Host "[WARNING] Certains tests ont echoue" -ForegroundColor Red
}

Write-Host ""
Write-Host "Rapports generes:" -ForegroundColor Cyan
if (Test-Path "../test_reports") {
    Get-ChildItem "../test_reports/*.html" | ForEach-Object {
        $sizeKB = [math]::Round($_.Length / 1024, 1)
        Write-Host "  - $($_.Name) ($sizeKB KB)" -ForegroundColor White
    }
} else {
    Write-Host "  Aucun rapport trouve" -ForegroundColor Red
}

Write-Host ""
Write-Host "Tests termines a $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray
Write-Host ""