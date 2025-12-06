# Script PowerShell pour préparer le déploiement sur Render
# Vérifie, commit et push les modifications

Write-Host "`n🔍 VÉRIFICATION PRÉ-DÉPLOIEMENT RENDER`n" -ForegroundColor Cyan

# 1. Vérifier les fichiers nécessaires
Write-Host "📋 Vérification des fichiers requis..." -ForegroundColor Yellow

$requiredFiles = @(
    "build.sh",
    "requirements.txt",
    "artify/settings.py",
    "artify/wsgi.py",
    "manage.py"
)

$allPresent = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file MANQUANT !" -ForegroundColor Red
        $allPresent = $false
    }
}

if (-not $allPresent) {
    Write-Host "`n❌ Des fichiers requis sont manquants !`n" -ForegroundColor Red
    exit 1
}

# 2. Vérifier les dépendances dans requirements.txt
Write-Host "`n📦 Vérification des dépendances critiques..." -ForegroundColor Yellow

$criticalDeps = @("Django", "gunicorn", "psycopg2-binary", "dj-database-url", "whitenoise")
$requirements = Get-Content requirements.txt

foreach ($dep in $criticalDeps) {
    if ($requirements -match $dep) {
        Write-Host "  ✓ $dep" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ $dep manquant (peut causer des erreurs)" -ForegroundColor Yellow
    }
}

# 3. Afficher les prochaines étapes
Write-Host "`n✅ VÉRIFICATION TERMINÉE !`n" -ForegroundColor Green

Write-Host "🚀 PROCHAINES ÉTAPES :`n" -ForegroundColor Cyan

Write-Host "1️⃣  Commitez et pushez sur GitHub :" -ForegroundColor White
Write-Host "    git add ." -ForegroundColor Gray
Write-Host "    git commit -m 'Préparation déploiement Render'" -ForegroundColor Gray
Write-Host "    git push origin main`n" -ForegroundColor Gray

Write-Host "2️⃣  Sur Render.com :" -ForegroundColor White
Write-Host "    • Créez une base PostgreSQL" -ForegroundColor Gray
Write-Host "    • Créez un Web Service" -ForegroundColor Gray
Write-Host "    • Connectez votre repo GitHub`n" -ForegroundColor Gray

Write-Host "3️⃣  Configuration Render :" -ForegroundColor White
Write-Host "    Build Command:  ./build.sh" -ForegroundColor Gray
Write-Host "    Start Command:  gunicorn artify.wsgi:application`n" -ForegroundColor Gray

Write-Host "4. Variables d'environnement a ajouter :" -ForegroundColor White
Write-Host "    • SECRET_KEY (générez avec: python generate_secret_key.py)" -ForegroundColor Gray
Write-Host "    • DEBUG=False" -ForegroundColor Gray
Write-Host "    • DATABASE_URL (fourni par Render)" -ForegroundColor Gray
Write-Host "    • PYTHON_VERSION=3.11.0" -ForegroundColor Gray
Write-Host "    • ALLOWED_HOSTS=votre-app.onrender.com`n" -ForegroundColor Gray

Write-Host "📖 Consultez RENDER_DEPLOYMENT.md pour plus de détails`n" -ForegroundColor Cyan

# 4. Proposer de générer une SECRET_KEY
Write-Host "🔐 Voulez-vous générer une SECRET_KEY maintenant ? (O/N): " -ForegroundColor Yellow -NoNewline
$response = Read-Host

if ($response -eq "O" -or $response -eq "o") {
    Write-Host ""
    python generate_secret_key.py
}

Write-Host "`n✨ Bonne chance avec votre déploiement ! ✨`n" -ForegroundColor Green
