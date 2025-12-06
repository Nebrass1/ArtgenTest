# Script PowerShell pour preparer le deploiement sur Render
# Verifie, commit et push les modifications

Write-Host "`nVERIFICATION PRE-DEPLOIEMENT RENDER`n" -ForegroundColor Cyan

# 1. Verifier les fichiers necessaires
Write-Host "Verification des fichiers requis..." -ForegroundColor Yellow

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
        Write-Host "  [OK] $file" -ForegroundColor Green
    } else {
        Write-Host "  [ERREUR] $file MANQUANT !" -ForegroundColor Red
        $allPresent = $false
    }
}

if (-not $allPresent) {
    Write-Host "`nDes fichiers requis sont manquants !`n" -ForegroundColor Red
    exit 1
}

# 2. Verifier les dependances dans requirements.txt
Write-Host "`nVerification des dependances critiques..." -ForegroundColor Yellow

$criticalDeps = @("Django", "gunicorn", "psycopg2-binary", "dj-database-url", "whitenoise")
$requirements = Get-Content requirements.txt

foreach ($dep in $criticalDeps) {
    if ($requirements -match $dep) {
        Write-Host "  [OK] $dep" -ForegroundColor Green
    } else {
        Write-Host "  [ATTENTION] $dep manquant" -ForegroundColor Yellow
    }
}

# 3. Afficher les prochaines etapes
Write-Host "`nVERIFICATION TERMINEE !`n" -ForegroundColor Green

Write-Host "PROCHAINES ETAPES :`n" -ForegroundColor Cyan

Write-Host "1. Commitez et pushez sur GitHub :" -ForegroundColor White
Write-Host "    git add ." -ForegroundColor Gray
Write-Host "    git commit -m 'Preparation deploiement Render'" -ForegroundColor Gray
Write-Host "    git push origin main`n" -ForegroundColor Gray

Write-Host "2. Sur Render.com :" -ForegroundColor White
Write-Host "    - Creez une base PostgreSQL" -ForegroundColor Gray
Write-Host "    - Creez un Web Service" -ForegroundColor Gray
Write-Host "    - Connectez votre repo GitHub`n" -ForegroundColor Gray

Write-Host "3. Configuration Render :" -ForegroundColor White
Write-Host "    Build Command:  ./build.sh" -ForegroundColor Gray
Write-Host "    Start Command:  gunicorn artify.wsgi:application`n" -ForegroundColor Gray

Write-Host "4. Variables d'environnement a ajouter :" -ForegroundColor White
Write-Host "    - SECRET_KEY (generez avec: python generate_secret_key.py)" -ForegroundColor Gray
Write-Host "    - DEBUG=False" -ForegroundColor Gray
Write-Host "    - DATABASE_URL (fourni par Render)" -ForegroundColor Gray
Write-Host "    - PYTHON_VERSION=3.11.0" -ForegroundColor Gray
Write-Host "    - ALLOWED_HOSTS=votre-app.onrender.com`n" -ForegroundColor Gray

Write-Host "Consultez RENDER_DEPLOYMENT.md pour plus de details`n" -ForegroundColor Cyan

# 4. Proposer de generer une SECRET_KEY
Write-Host "Voulez-vous generer une SECRET_KEY maintenant ? (O/N): " -ForegroundColor Yellow -NoNewline
$response = Read-Host

if ($response -eq "O" -or $response -eq "o") {
    Write-Host ""
    python generate_secret_key.py
}

Write-Host "`nBonne chance avec votre deploiement !`n" -ForegroundColor Green
