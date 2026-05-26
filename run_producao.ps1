# Script para rodar o SARA em produção com waitress
# Execute como: PowerShell -File run_producao.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SARA - Servidor de Producao" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Instalar dependencias se necessario
pip install -r requirements.txt -q

# Forcar modo producao
$env:APP_ENV = "production"
$env:FLASK_DEBUG = "false"

# Rodar com python run.py (que usa waitress)
Write-Host "Iniciando servidor em http://0.0.0.0:5000" -ForegroundColor Green
Write-Host "Modo: PRODUCAO (debug=false, waitress)" -ForegroundColor Green
Write-Host "Para parar: Ctrl+C" -ForegroundColor Yellow
Write-Host ""

python run.py
