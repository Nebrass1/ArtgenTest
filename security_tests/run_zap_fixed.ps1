Write-Host "==========================================" -ForegroundColor Green
Write-Host "   SCAN ZAP CORRIGE" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

Write-Host "1. Premier test avec host.docker.internal..." -ForegroundColor Yellow
try {
    docker run --rm -v "$(pwd)/zap_reports:/zap/wrk/:rw" -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t "http://host.docker.internal:8000" -r "zap_report.html"
    
    if (Test-Path "zap_reports/zap_report.html") {
        Write-Host "✅ Scan réussi avec host.docker.internal" -ForegroundColor Green
        Start-Process "zap_reports/zap_report.html"
        exit
    }
} catch {
    Write-Host "❌ Échec avec host.docker.internal" -ForegroundColor Red
}

Write-Host ""
Write-Host "2. Test avec network host..." -ForegroundColor Yellow
try {
    docker run --rm -v "$(pwd)/zap_reports:/zap/wrk/:rw" --network host -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t "http://localhost:8000" -r "zap_report.html"
    
    if (Test-Path "zap_reports/zap_report.html") {
        Write-Host "✅ Scan réussi avec network host" -ForegroundColor Green
        Start-Process "zap_reports/zap_report.html"
        exit
    }
} catch {
    Write-Host "❌ Échec avec network host" -ForegroundColor Red
}

Write-Host ""
Write-Host "💡 SOLUTION MANUELLE REQUISE:" -ForegroundColor Yellow
Write-Host "1. Ouvre un NOUVEAU terminal" -ForegroundColor Cyan
Write-Host "2. cd vers ton projet Artygen" -ForegroundColor Cyan
Write-Host "3. python manage.py runserver 0.0.0.0:8000" -ForegroundColor Cyan
Write-Host "4. Reviens ici et relance: docker run --rm -v `$(pwd)/zap_reports:/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://host.docker.internal:8000 -r zap_report.html" -ForegroundColor Cyan