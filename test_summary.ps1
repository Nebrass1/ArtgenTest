# Script de résumé des outils de test - Artygen
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "ARTYGEN - OUTILS DE TEST DISPONIBLES" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Vérification de l'environnement
if (Test-Path "..\.venv\Scripts\python.exe") {
    Write-Host "[OK] Environnement virtuel detecte" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Environnement virtuel manquant" -ForegroundColor Red
    Write-Host ""
    return
}

Write-Host ""
Write-Host "SCRIPTS DE TEST DISPONIBLES:" -ForegroundColor Yellow
Write-Host ""

# Lister tous les scripts de test
$scripts = @(
    @{Name="run_auth_tests_simple.ps1"; Description="Tests d'authentification unitaires (rapide)"},
    @{Name="run_chrome_tests.ps1"; Description="Tests Chrome uniquement (optimise)"},
    @{Name="run_cross_browser_stable.ps1"; Description="Tests multi-navigateurs complets"},
    @{Name="analyze_complete.ps1"; Description="Analyse de code complete (Pylint + Coverage)"},
    @{Name="show_reports.ps1"; Description="Affichage des rapports generes"}
)

$index = 1
foreach ($script in $scripts) {
    $exists = Test-Path $script.Name
    $status = if ($exists) { "[OK]" } else { "[MANQUANT]" }
    $color = if ($exists) { "Green" } else { "Red" }
    
    Write-Host "$index. $($script.Name)" -ForegroundColor White
    Write-Host "   Status: $status" -ForegroundColor $color
    Write-Host "   Description: $($script.Description)" -ForegroundColor Gray
    Write-Host ""
    $index++
}

Write-Host "TESTS UNITAIRES DISPONIBLES:" -ForegroundColor Yellow
Write-Host ""

$testFiles = @(
    @{Name="test_auth_unit.py"; Description="Tests unitaires d'authentification"},
    @{Name="test_auth_ui.py"; Description="Tests d'interface utilisateur Selenium"},
    @{Name="test_auth_cross_browser.py"; Description="Tests de compatibilite multi-navigateurs"},
    @{Name="test_data.py"; Description="Tests de donnees et modeles"}
)

foreach ($test in $testFiles) {
    $path = "accounts/tests/$($test.Name)"
    $exists = Test-Path $path
    $status = if ($exists) { "[OK]" } else { "[MANQUANT]" }
    $color = if ($exists) { "Green" } else { "Red" }
    
    Write-Host "- $($test.Name)" -ForegroundColor White
    Write-Host "  Status: $status - $($test.Description)" -ForegroundColor $color
}

Write-Host ""
Write-Host "COMMANDES RAPIDES:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Tests rapides:" -ForegroundColor White
Write-Host "  .\run_auth_tests_simple.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tests Chrome:" -ForegroundColor White  
Write-Host "  .\run_chrome_tests.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tests complets:" -ForegroundColor White
Write-Host "  .\run_cross_browser_stable.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Analyse de code:" -ForegroundColor White
Write-Host "  .\analyze_complete.ps1" -ForegroundColor Cyan
Write-Host ""

# Vérifier les navigateurs disponibles
Write-Host "NAVIGATEURS DETECTES:" -ForegroundColor Yellow

$chromePaths = @(
    "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
    "${env:LOCALAPPDATA}\Google\Chrome\Application\chrome.exe"
)
$chromeFound = $false
foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        Write-Host "  [OK] Chrome trouve" -ForegroundColor Green
        $chromeFound = $true
        break
    }
}
if (-not $chromeFound) {
    Write-Host "  [INFO] Chrome non detecte" -ForegroundColor Yellow
}

$firefoxPath = "${env:ProgramFiles}\Mozilla Firefox\firefox.exe"
if (Test-Path $firefoxPath) {
    Write-Host "  [OK] Firefox trouve" -ForegroundColor Green
} else {
    Write-Host "  [INFO] Firefox non detecte" -ForegroundColor Yellow
}

$edgePaths = @(
    "${env:ProgramFiles}\Microsoft\Edge\Application\msedge.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
)
$edgeFound = $false
foreach ($path in $edgePaths) {
    if (Test-Path $path) {
        Write-Host "  [OK] Edge trouve" -ForegroundColor Green
        $edgeFound = $true
        break
    }
}
if (-not $edgeFound) {
    Write-Host "  [INFO] Edge non detecte" -ForegroundColor Yellow
}

Write-Host ""

# Vérifier les rapports existants
if (Test-Path "../test_reports") {
    Write-Host "DERNIERS RAPPORTS:" -ForegroundColor Yellow
    Get-ChildItem "../test_reports/*.html" | Sort-Object LastWriteTime -Descending | Select-Object -First 5 | ForEach-Object {
        $age = (Get-Date) - $_.LastWriteTime
        $ageString = if ($age.Days -gt 0) { "$($age.Days)j" } elseif ($age.Hours -gt 0) { "$($age.Hours)h" } else { "$($age.Minutes)m" }
        $size = [math]::Round($_.Length / 1KB, 1)
        Write-Host "  $($_.Name) (${size} KB, il y a ${ageString})" -ForegroundColor White
    }
} else {
    Write-Host "RAPPORTS: Aucun rapport trouve" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Pret pour les tests!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""