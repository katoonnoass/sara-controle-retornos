<#
.SYNOPSIS
  Script de TESTE de restauracao de backup do SARA.
  ATENCAO: Este script NAO restaura no banco principal.
  Cria um banco separado sara_restore_test para validacao.
.DESCRIPTION
  Restaura o backup mais recente de backups/ em um banco de teste.
  Remove o banco de teste ao final (opcional).
.PARAMETER KeepTestDb
  Se true, mantem o banco de teste apos a validacao.
.PARAMETER DumpFile
  Caminho especifico do arquivo .dump. Se omitido, usa o mais recente.
.EXAMPLE
  .\test_backup_restore.ps1
  .\test_backup_restore.ps1 -DumpFile "C:\sara\backups\sara_2026-05-25_14-30-00.dump"
#>

param(
    [switch]$KeepTestDb,
    [string]$DumpFile = ""
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir
$BackupDir = Join-Path $ProjectDir "backups"
$LogFile   = Join-Path $ProjectDir "logs" "backup.log"

# ── Carregar .env ───────────────────────────────────────────────────────────
$EnvFile = Join-Path $ProjectDir ".env"
if (Test-Path $EnvFile) {
    Get-Content $EnvFile | ForEach-Object {
        if ($_ -match "^\s*([^#=]+)=(.+)$") {
            $key = $matches[1].Trim()
            $val = $matches[2].Trim()
            Set-Item -Path "Env:$key" -Value $val -ErrorAction SilentlyContinue
        }
    }
}

# ── Extrair dados de conexao ────────────────────────────────────────────────
$DbUrl = $env:DATABASE_URL
if (-not $DbUrl) { Write-Host "[ERRO] DATABASE_URL nao definida" -ForegroundColor Red; exit 1 }

$Regex = [regex] '://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)'
$Match = $Regex.Match($DbUrl)
if (-not $Match.Success) { Write-Host "[ERRO] Nao foi possivel interpretar DATABASE_URL" -ForegroundColor Red; exit 1 }

$DbUser   = $Match.Groups[1].Value
$DbPass   = [System.Uri]::UnescapeDataString($Match.Groups[2].Value)
$DbHost   = $Match.Groups[3].Value
$DbPort   = $Match.Groups[4].Value
$DbName   = $Match.Groups[5].Value
$TestDb   = "sara_restore_test"

# ── Verificar pg_dump/pg_restore ─────────────────────────────────────────────
if (-not (Get-Command "pg_restore" -ErrorAction SilentlyContinue)) {
    Write-Host "[ERRO] pg_restore nao encontrado." -ForegroundColor Red; exit 1
}
if (-not (Get-Command "psql" -ErrorAction SilentlyContinue)) {
    Write-Host "[ERRO] psql nao encontrado." -ForegroundColor Red; exit 1
}

# ── Escolher dump file ──────────────────────────────────────────────────────
if (-not $DumpFile) {
    $Latest = Get-ChildItem -Path $BackupDir -Filter "sara_*.dump" -File |
              Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if (-not $Latest) { Write-Host "[ERRO] Nenhum arquivo .dump encontrado em $BackupDir" -ForegroundColor Red; exit 1 }
    $DumpFile = $Latest.FullName
}

Write-Host "`n=============================================" -ForegroundColor Cyan
Write-Host "  TESTE DE RESTAURACAO DE BACKUP" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Arquivo:        $DumpFile" -ForegroundColor White
Write-Host "Banco de teste: $TestDb" -ForegroundColor Yellow
Write-Host "ATENCAO: Nao restaura no banco principal ($DbName)!" -ForegroundColor Red
Write-Host ""

# ── Criar banco de teste ────────────────────────────────────────────────────
$env:PGPASSWORD = $DbPass

Write-Host ">>> Criando banco de teste: $TestDb ..." -ForegroundColor Yellow
try {
    $result = & psql --host=$DbHost --port=$DbPort --username=$DbUser --dbname=postgres `
                     -c "DROP DATABASE IF EXISTS $TestDb;" -c "CREATE DATABASE $TestDb;" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERRO] Falha ao criar banco de teste: $result" -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] Banco de teste criado." -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Excecao ao criar banco de teste: $_" -ForegroundColor Red
    exit 1
}

# ── Restaurar backup ────────────────────────────────────────────────────────
Write-Host ">>> Restaurando backup no banco de teste ..." -ForegroundColor Yellow
try {
    & pg_restore --host=$DbHost --port=$DbPort --username=$DbUser `
                 --dbname=$TestDb --verbose --no-owner --no-acl `
                 "$DumpFile" 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Backup restaurado com sucesso no banco $TestDb" -ForegroundColor Green
    } else {
        Write-Host "[ERRO] pg_restore falhou (exit code: $LASTEXITCODE)" -ForegroundColor Red
    }
} catch {
    Write-Host "[ERRO] Excecao ao restaurar: $_" -ForegroundColor Red
}

# ── Verificar dados restaurados ─────────────────────────────────────────────
Write-Host ">>> Verificando dados restaurados ..." -ForegroundColor Yellow
try {
    $tables = & psql --host=$DbHost --port=$DbPort --username=$DbUser --dbname=$TestDb `
                     -t -c "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename;" 2>&1
    Write-Host "Tabelas encontradas:" -ForegroundColor Gray
    $tables.Trim().Split("`n") | ForEach-Object {
        $t = $_.Trim()
        if ($t) {
            $count = & psql --host=$DbHost --port=$DbPort --username=$DbUser --dbname=$TestDb `
                           -t -c "SELECT COUNT(*) FROM $t;" 2>&1
            Write-Host "  $t : $($count.Trim()) registros" -ForegroundColor White
        }
    }
} catch {
    Write-Host "[ERRO] Falha ao verificar dados: $_" -ForegroundColor Red
}

# ── Limpar banco de teste ───────────────────────────────────────────────────
if (-not $KeepTestDb) {
    Write-Host ">>> Removendo banco de teste ..." -ForegroundColor Yellow
    try {
        & psql --host=$DbHost --port=$DbPort --username=$DbUser --dbname=postgres `
               -c "DROP DATABASE IF EXISTS $TestDb;" 2>&1 | Out-Null
        Write-Host "[OK] Banco de teste removido." -ForegroundColor Green
    } catch {
        Write-Host "[ERRO] Falha ao remover banco de teste: $_" -ForegroundColor Red
    }
} else {
    Write-Host "Banco de teste mantido: $TestDb" -ForegroundColor Yellow
}

Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Teste de restauracao concluido." -ForegroundColor Green
Write-Host "Log: $LogFile" -ForegroundColor Gray
