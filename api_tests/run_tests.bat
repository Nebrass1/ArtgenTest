@echo off
echo ==========================================
echo   TESTS API ARTYGEN AVEC NEWMAN
echo ==========================================

npx newman run collections/artygen_api_tests.json --environment environments/artygen_local.json --reporters cli,html --reporter-html-export reports/test_report.html --delay-request 1000

pause