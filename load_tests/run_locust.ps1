# Script PowerShell simplifié pour Locust
Write-Host "========================================" -ForegroundColor Green
Write-Host "       TESTS DE CHARGE ARTYGEN" -ForegroundColor Green  
Write-Host "        VERSION SIMPLIFIÉE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 Configuration des tests:" -ForegroundColor Yellow
Write-Host "   - Version: SIMPLIFIÉE (sans CSRF)" -ForegroundColor Cyan
Write-Host "   - Focus: Tests GET fiables uniquement" -ForegroundColor Cyan
Write-Host "   - Endpoints: 8 tests robustes" -ForegroundColor Cyan

Write-Host ""
Write-Host "📊 Interface Locust:" -ForegroundColor Yellow
Write-Host "   http://localhost:8089" -ForegroundColor Green

Write-Host ""
Write-Host "⚙️  Configuration recommandée:" -ForegroundColor Yellow
Write-Host "   - Number of users: 5-10" -ForegroundColor Cyan
Write-Host "   - Spawn rate: 2" -ForegroundColor Cyan
Write-Host "   - Host: http://127.0.0.1:8000" -ForegroundColor Cyan

Write-Host ""
Write-Host "🎯 Tests disponibles (100% fiables):" -ForegroundColor Yellow
Write-Host "   ✅ Page d'accueil (poids 10)" -ForegroundColor Green
Write-Host "   ✅ Blog (poids 5)" -ForegroundColor Green  
Write-Host "   ✅ Catégories (poids 3)" -ForegroundColor Green
Write-Host "   ✅ Artworks (poids 3)" -ForegroundColor Green
Write-Host "   ✅ Galleries (poids 2)" -ForegroundColor Green
Write-Host "   ✅ Login page (poids 2)" -ForegroundColor Green
Write-Host "   ✅ Admin redirect (poids 2)" -ForegroundColor Green
Write-Host "   ✅ Artwork create (poids 1)" -ForegroundColor Green
Write-Host "   ✅ Static CSS (poids 1)" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 Démarrage..." -ForegroundColor Green

# Lance Locust avec la version simplifiée
locust -f locustfile_simple.py --host=http://127.0.0.1:8000