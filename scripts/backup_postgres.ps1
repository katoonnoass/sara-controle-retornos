<#
.SYNOPSIS
  Backup do banco PostgreSQL do SARA usando pg_dump.
.DESCRIPTION
  Gera backup custom (.dump) do banco sara, salva em backups/ com data/hora,
  registra log em logs/backup.log, remove backups antigos conforme retencao.
.PARAMETER RetentionDays
  Numero de dias para manter backups. Padrao: 30.
.PARAMETER BackupDir
  Diretorio de destino. Padrao: ..\backups\ (relativo ao script).
.PARAMETER LogFile
  Arquivo de log. Padrao: ..\logs\backup.log (relativo ao script).
.EXAMPLE
  .\backup_postgres.ps1
  .\backup_postgres.ps1 -RetentionDays 60
#>

param(
    [int]$RetentionDays = 30,
    [string]$BackupDir = "",
    [string]$LogFile = ""
)

# ── Caminhos ─────────────────────────────────────────────────────────────────
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

if (-not $BackupDir) { $BackupDir = Join-Path $ProjectDir "backups" }
if (-not $LogFile)   { $LogFile   = Join-Path (Join-Path $ProjectDir "logs") "backup.log" }

# ── Carregar .env (se existir) ──────────────────────────────────────────────
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

# ── Extrair dados da DATABASE_URL ───────────────────────────────────────────
$DbUrl = $env:DATABASE_URL
if (-not $DbUrl) {
    Write-Host "[ERRO] DATABASE_URL nao definida. Verifique .env" -ForegroundColor Red
    exit 1
}

# Parse: postgresql+psycopg://user:pass@host:port/dbname
$Regex = [regex] '://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)'
$Match = $Regex.Match($DbUrl)

if (-not $Match.Success) {
    Write-Host "[ERRO] Nao foi possivel interpretar DATABASE_URL" -ForegroundColor Red
    exit 1
}

$DbUser   = $Match.Groups[1].Value
$DbPass   = [System.Uri]::UnescapeDataString($Match.Groups[2].Value)
$DbHost   = $Match.Groups[3].Value
$DbPort   = $Match.Groups[4].Value
$DbName   = $Match.Groups[5].Value

# ── Verificar pg_dump ───────────────────────────────────────────────────────
$PgDump = Get-Command "pg_dump" -ErrorAction SilentlyContinue
if (-not $PgDump) {
    # Try common PostgreSQL paths
    $PossiblePaths = @(
        "${env:ProgramFiles}\PostgreSQL\16\bin\pg_dump.exe",
        "${env:ProgramFiles}\PostgreSQL\15\bin\pg_dump.exe",
        "${env:ProgramFiles}\PostgreSQL\14\bin\pg_dump.exe",
        "${env:ProgramFiles}\PostgreSQL\17\bin\pg_dump.exe"
    )
    foreach ($p in $PossiblePaths) {
        if (Test-Path $p) {
            $env:Path += ";$(Split-Path $p -Parent)"
            $PgDump = Get-Command "pg_dump" -ErrorAction SilentlyContinue
            break
        }
    }
}
if (-not $PgDump) {
    Write-Host "[ERRO] pg_dump nao encontrado. Instale PostgreSQL Client ou ajuste o PATH." -ForegroundColor Red
    Write-Host "Esperado em: C:\Program Files\PostgreSQL\16\bin\pg_dump.exe" -ForegroundColor Gray
    exit 1
}

# ── Criar diretorios ────────────────────────────────────────────────────────
New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path $LogFile -Parent) -Force | Out-Null

# ── Timestamp e nomes ───────────────────────────────────────────────────────
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$DumpFile  = Join-Path $BackupDir "sara_$Timestamp.dump"
$SqlFile   = Join-Path $BackupDir "sara_$Timestamp.sql"

function Write-Log {
    param([string]$Level, [string]$Message)
    $Line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [$Level] $Message"
    Add-Content -Path $LogFile -Value $Line
    if ($Level -eq "ERRO") {
        Write-Host $Line -ForegroundColor Red
    } elseif ($Level -eq "OK") {
        Write-Host $Line -ForegroundColor Green
    } else {
        Write-Host $Line -ForegroundColor Gray
    }
}

Write-Log "INFO" "=== Inicio do backup ==="
Write-Log "INFO" "Banco: $DbName Host: ${DbHost}:${DbPort} Usuario: $DbUser"

# ── Executar pg_dump (formato custom) ──────────────────────────────────────
$env:PGPASSWORD = $DbPass

 try {
    & pg_dump --host="${DbHost}" --port="${DbPort}" --username="${DbUser}" `
              --format=custom --compress=9 --verbose `
              --file="$DumpFile" "$DbName" 2>> $LogFile

    if ($LASTEXITCODE -eq 0 -and (Test-Path $DumpFile)) {
        $Size = "{0:N2} MB" -f ((Get-Item $DumpFile).Length / 1MB)
        Write-Log "OK"   "Backup custom criado: $DumpFile ($Size)"
    } else {
        Write-Log "ERRO" "pg_dump falhou (exit code: $LASTEXITCODE)"
    }
} catch {
    Write-Log "ERRO" "Excecao ao executar pg_dump: $_"
} finally {
    Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
}

# ── Opcional: backup SQL plain ──────────────────────────────────────────────
try {
    & pg_dump --host="${DbHost}" --port="${DbPort}" --username="${DbUser}" `
              --format=plain --no-owner --no-acl `
              --file="$SqlFile" "$DbName" 2>> $LogFile

    if ($LASTEXITCODE -eq 0 -and (Test-Path $SqlFile)) {
        $SizeSql = "{0:N2} MB" -f ((Get-Item $SqlFile).Length / 1MB)
        Write-Log "OK" "Backup SQL criado: $SqlFile ($SizeSql)"
    }
} catch {
    Write-Log "ERRO" "Excecao ao gerar SQL: $_"
}

# ── Remover backups antigos ─────────────────────────────────────────────────
$Cutoff = (Get-Date).AddDays(-$RetentionDays)
$Removidos = 0
Get-ChildItem -Path $BackupDir -Filter "sara_*.dump" -File | Where-Object {
    $_.LastWriteTime -lt $Cutoff
} | ForEach-Object {
    Remove-Item -Path $_.FullName -Force
    Write-Log "INFO" "Removido backup antigo: $($_.Name)"
    $Removidos++
}

Get-ChildItem -Path $BackupDir -Filter "sara_*.sql" -File | Where-Object {
    $_.LastWriteTime -lt $Cutoff
} | ForEach-Object {
    Remove-Item -Path $_.FullName -Force
    Write-Log "INFO" "Removido SQL antigo: $($_.Name)"
    $Removidos++
}

Write-Log "INFO" "Retencao: $RetentionDays dias | Removidos: $Removidos"
Write-Log "INFO" "=== Backup concluido ==="

Write-Host ""
Write-Host "Backup concluido. Arquivos em: $BackupDir" -ForegroundColor Green
Write-Host "Log: $LogFile" -ForegroundColor Gray
