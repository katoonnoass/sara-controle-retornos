# Backup do PostgreSQL — SARA

## Visão Geral

Script de backup automático do banco PostgreSQL do SARA usando `pg_dump`.
Os backups são salvos em formato custom `.dump` (comprimido) e também em `.sql` (texto plano).

## Requisitos

- PostgreSQL Client Tools (`pg_dump`, `pg_restore`, `psql`)
  - Instalar via: https://www.postgresql.org/download/windows/
  - Ou via Chocolatey: `choco install postgresql --params="/NoInstallation"`

## Scripts

| Script | Descrição |
|---|---|
| `scripts/backup_postgres.ps1` | Backup principal |
| `scripts/test_backup_restore.ps1` | Teste de restauração em banco separado |

## Como Executar o Backup Manual

Abra o PowerShell na pasta do projeto e execute:

```powershell
.\scripts\backup_postgres.ps1
```

Para especificar retenção diferente (ex.: 60 dias):

```powershell
.\scripts\backup_postgres.ps1 -RetentionDays 60
```

## Onde os Arquivos São Salvos

| Item | Caminho |
|---|---|
| Backups | `backups/sara_YYYY-MM-DD_HH-mm-ss.dump` |
| Backups SQL | `backups/sara_YYYY-MM-DD_HH-mm-ss.sql` |
| Log | `logs/backup.log` |

## Retenção

- Padrão: **30 dias**
- Configurar via parâmetro `-RetentionDays` ou variável de ambiente `BACKUP_RETENTION_DAYS`
- Backups mais antigos que o período de retenção são removidos automaticamente

## Como Agendar no Windows (Task Scheduler)

1. Abra o **Agendador de Tarefas** (`taskschd.msc`)
2. Clique em **Criar Tarefa Básica**
3. Nome: `SARA Backup PostgreSQL`
4. Gatilho: **Diariamente** ou conforme desejado
5. Ação: **Iniciar um programa**
   - Programa: `powershell.exe`
   - Argumentos:
     ```
     -ExecutionPolicy Bypass -File "C:\Users\joao.silva\Documents\SARA\scripts\backup_postgres.ps1"
     ```
   - Iniciar em: `C:\Users\joao.silva\Documents\SARA`
6. Concluir

### Opção: Executar como usuário do banco

Crie um arquivo `C:\Users\joao.silva\.pgpass` com:

```
localhost:5433:*:postgres:Ephar@2026PG
```

E ajuste o script para não usar `PGPASSWORD`.

## Como Restaurar em Banco Separado (Teste)

Use o script de teste:

```powershell
.\scripts\test_backup_restore.ps1
```

Este script:
1. Cria um banco `sara_restore_test`
2. Restaura o backup mais recente
3. Lista as tabelas com contagem de registros
4. Remove o banco de teste (a menos que use `-KeepTestDb`)

### Restauração Manual

Para restaurar em um banco específico:

```powershell
pg_restore --host=localhost --port=5433 --username=postgres `
           --dbname=sara_restore_test --no-owner --no-acl `
           "backups\sara_2026-05-25_14-30-00.dump"
```

**ATENÇÃO:** Nunca aponte `--dbname` para o banco de produção (`sara`) sem confirmar que é intencional.

## Cuidados

1. **Nunca** restaurar um backup diretamente no banco principal (`sara`) sem confirmar que é a ação desejada.
2. A senha do banco é lida do `.env` — mantenha o `.env` fora do versionamento (`.gitignore` já protege).
3. Verifique periodicamente se os backups estão sendo gerados consultando `logs/backup.log`.
4. Teste a restauração periodicamente usando `scripts/test_backup_restore.ps1`.

## Validação do Backup

Para verificar rapidamente se o backup é válido:

```powershell
pg_restore --list "backups\sara_2026-05-25_14-30-00.dump" | Select-Object -First 20
```

Isso lista o conteúdo do arquivo sem restaurar os dados.
