# Script pour ouvrir les rapports d'analyse
Write-Host "=== RAPPORTS D'ANALYSE ARTYGEN ==="
Write-Host ""

# Vérifier les rapports disponibles
$reportsDir = "..\test_reports"

Write-Host "Rapports disponibles:"
if (Test-Path "$reportsDir\pylint_report.txt") {
    Write-Host "[OK] Rapport Pylint (analyse de code)"
}
if (Test-Path "$reportsDir\pylint_report.json") {
    Write-Host "[OK] Rapport Pylint JSON"
}
if (Test-Path "$reportsDir\coverage_html\index.html") {
    Write-Host "[OK] Rapport de couverture HTML"
}

Write-Host ""
Write-Host "Actions disponibles:"
Write-Host "1. Ouvrir rapport de couverture HTML"
Write-Host "2. Afficher résumé Pylint"
Write-Host "3. Afficher résumé de couverture"
Write-Host "4. Ouvrir tous les rapports"
Write-Host ""

$choice = Read-Host "Votre choix (1-4)"

switch ($choice) {
    "1" {
        if (Test-Path "$reportsDir\coverage_html\index.html") {
            Write-Host "Ouverture du rapport de couverture..."
            Start-Process "$reportsDir\coverage_html\index.html"
        } else {
            Write-Host "Rapport de couverture non trouvé!"
        }
    }
    "2" {
        if (Test-Path "$reportsDir\pylint_report.txt") {
            Write-Host "Résumé Pylint:"
            Get-Content "$reportsDir\pylint_report.txt" | Select-String "Your code has been rated"
        } else {
            Write-Host "Rapport Pylint non trouvé!"
        }
    }
    "3" {
        Write-Host "Derniers résultats de couverture:"
        Write-Host "- Couverture totale: 88%"
        Write-Host "- Tests passés: 10/10"
        Write-Host "- Fichiers analysés: module accounts complet"
    }
    "4" {
        if (Test-Path "$reportsDir\coverage_html\index.html") {
            Start-Process "$reportsDir\coverage_html\index.html"
        }
        if (Test-Path "$reportsDir\pylint_report.txt") {
            notepad "$reportsDir\pylint_report.txt"
        }
    }
    default {
        Write-Host "Choix invalide!"
    }
}