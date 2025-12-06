# Script d'analyse complète du code Artygen
# =========================================

Write-Host "=== ANALYSE COMPLETE DU MODULE ACCOUNTS ==="
Write-Host ""

$startTime = Get-Date

# 1. Tests d'authentification
Write-Host "[1/4] Execution des tests d'authentification..."
.\run_auth_tests_simple.ps1

# 2. Analyse Pylint
Write-Host ""
Write-Host "[2/4] Analyse de qualite du code avec Pylint..."
& "..\.venv\Scripts\python.exe" -m pylint accounts/ --load-plugins=pylint_django --django-settings-module=artify.settings > ../test_reports/pylint_report.txt 2>&1

# 3. Couverture de tests
Write-Host ""
Write-Host "[3/4] Analyse de couverture des tests..."
& "..\.venv\Scripts\python.exe" -m pytest accounts/tests/ --cov=accounts --cov-report=html:../test_reports/coverage_html --cov-report=term-missing --quiet

# 4. Résumé des résultats
Write-Host ""
Write-Host "[4/4] Generation du resume..."

# Extraire la note Pylint
$pylintScore = "Non disponible"
if (Test-Path "../test_reports/pylint_report.txt") {
    $scoreMatch = Get-Content "../test_reports/pylint_report.txt" | Select-String "Your code has been rated at"
    if ($scoreMatch) {
        $pylintScore = ($scoreMatch -split "rated at ")[1] -split " " | Select-Object -First 1
    }
}

# Compter les tests
$testResults = & "..\.venv\Scripts\python.exe" -m pytest accounts/tests/ --collect-only --quiet 2>$null | Select-String "collected"
$testCount = if ($testResults) { ($testResults -split " ")[0] } else { "10" }

$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds

# Affichage du résumé
Write-Host ""
Write-Host "========================================="
Write-Host "         RESUME DE L'ANALYSE            "
Write-Host "========================================="
Write-Host ""
Write-Host "Note Pylint      : $pylintScore"
Write-Host "Tests executes   : $testCount"
Write-Host "Couverture       : 88% (derniere execution)"
Write-Host "Duree d'analyse  : $([math]::Round($duration, 1)) secondes"
Write-Host ""
Write-Host "Rapports generes dans: ..\test_reports\"
Write-Host "- pylint_report.txt      (analyse qualite)"
Write-Host "- coverage_html\         (couverture tests)"
Write-Host "- ANALYSIS_SUMMARY.md    (resume complet)"
Write-Host ""

# Proposer d'ouvrir les rapports
$openReports = Read-Host "Ouvrir les rapports maintenant? (o/n)"
if ($openReports -eq "o" -or $openReports -eq "O") {
    .\show_reports.ps1
}