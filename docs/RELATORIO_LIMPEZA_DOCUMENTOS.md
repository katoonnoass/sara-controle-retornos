# Relatório de Inventário — Documentos / SARA

**Data**: 26/05/2026  
**Objetivo**: Identificar pastas e arquivos em `Documents`, classificar riscos e preparar limpeza segura.  
**Nada foi apagado ou movido.**

---

## 1. Resumo Geral

| Item | Valor |
|---|---|
| Pastas encontradas em Documents | 9 |
| Arquivos soltos em Documents | 3 (Default.rdp, desktop.ini, Project CRM.zip) |
| Pasta oficial do SARA | `Documents\SARA` |
| Pastas aparentemente em uso | 4 (SARA, ServiceDesk, ServiceDeskAgent, painel de chamados) |
| Pastas candidatas a limpeza | 4 (Codex, New project, AD Auditory, WindowsPowerShell) |
| Total ocupado em Documents | ~3 GB |

---

## 2. Pastas Encontradas em Documents

| # | Pasta | Tamanho | Arquivos | Tem código? | Recomendação |
|---|---|---|---|---|---|
| 1 | **SARA** | ~1 MB (sem bin/obj) | 81 | Python + C# | **MANTER** — projeto ativo |
| 2 | **ServiceDesk** | 1.228 MB | 3.946 | C# | **MANTER** — outro projeto ativo |
| 3 | **ServiceDeskAgent** | 155 MB | 22 | C# + .exe | **MANTER** — Agent do ServiceDesk |
| 4 | **painel de chamados** | 948 MB | 2.328 | HTML | **MANTER** — outro projeto ativo |
| 5 | **AD Auditory** | 218 MB | 378 | HTML + Excel + logs | **DÚVIDA** — verificar se ainda usado |
| 6 | **Project CRM** | 424 MB | 656 | — | **DÚVIDA** — verificar se ainda usado |
| 7 | **New project** | 1,4 MB | 19 | HTML | **PODE EXCLUIR** — provavelmente resíduo |
| 8 | **Codex** | 0 MB | 0 | — | **PODE EXCLUIR** — vazio |
| 9 | **WindowsPowerShell** | 0 MB | 0 | — | **MANTER** — padrão do Windows |

---

## 3. Pasta Oficial do SARA — Análise Detalhada

**Caminho**: `Documents\SARA`

### Arquivos essenciais (presentes)

- [x] `app.py` — entry point Flask
- [x] `run.py` — entry point produção (Waitress)
- [x] `config.py` — configurações
- [x] `models.py` — modelos SQLAlchemy
- [x] `requirements.txt` — dependências
- [x] `.env` — variáveis de ambiente
- [x] `utils.py` — funções compartilhadas
- [x] `logging_config.py` — configuração de log

### Diretórios essenciais (presentes)

- [x] `routes/` — 5 blueprints
- [x] `templates/` — 20 templates HTML
- [x] `scripts/` — 4 scripts (backup, auditoria, hash)
- [x] `docs/` — 4 documentos (plano homologação, execução, problemas, backup)
- [x] `logs/` — 2 logs (aplicação + backup)
- [x] `backups/` — 2 backups .dump
- [x] `data/` — 3 Excel de referência (backup)
- [x] `assets/` — 6 arquivos de mídia

### SARA Server Agent

- [x] 18 arquivos fonte C#/XAML
- [x] Publicado: `SARA Server Agent.exe` (154,5 MB)

---

## 4. Itens para Limpeza

### Dentro da pasta SARA

| Item | Localização | Ação recomendada |
|---|---|---|
| `__pycache__/` | Várias pastas (2 encontradas) | **Pode limpar** — regenerado automaticamente |
| `bin/` | `SaraServerAgent/bin/` | **Pode limpar** — artifacts de build |
| `obj/` | `SaraServerAgent/obj/` | **Pode limpar** — artifacts de build |
| `logs/sara-app.log` | `logs/` | **Manter** — necessário para suporte |
| `logs/backup.log` | `logs/` | **Manter** — necessário para verificação |
| `backups/*.dump` | `backups/` | **Manter mais recente**, limpar se > 30 dias |
| `data/*.xlsx` | `data/` | **Manter** — backup de referência |

### Fora da pasta SARA

| Pasta | Ação | Risco |
|---|---|---|
| `New project` | Excluir após confirmação | Baixo — vazio/quase vazio |
| `Codex` | Excluir após confirmação | Baixo — vazio |
| `AD Auditory` | Verificar se ainda usado | Médio — 218 MB |
| `Project CRM` | Verificar se ainda usado | Médio — 424 MB |

---

## 5. Pastas que NÃO devem ser apagadas

- `Documents\SARA` — projeto principal
- `Documents\ServiceDesk` — outro sistema
- `Documents\ServiceDeskAgent` — Agent do ServiceDesk
- `Documents\painel de chamados` — outro sistema
- `Documents\WindowsPowerShell` — padrão do sistema

---

## 6. Pastas Candidatas a Quarentena

| Pasta | Motivo | Tamanho |
|---|---|---|
| `New project` | 19 arquivos HTML, provavelmente resíduo | 1,4 MB |
| `Codex` | Vazia | 0 MB |

---

## 7. Arquivos Temporários Encontrados

| Arquivo | Local | Tamanho |
|---|---|---|
| `Project CRM.zip` | Documents (raiz) | ~285 MB |
| `Default.rdp` | Documents (raiz) | ~2 KB |
| `desktop.ini` | Documents (raiz) | ~0,4 KB (padrão Windows) |

---

## 8. Itens que Precisam de Confirmação Manual

| Item | Pergunta | Responsável |
|---|---|---|
| `AD Auditory` (218 MB) | Ainda está em uso? É outro sistema? | Usuário |
| `Project CRM` (424 MB) | Projeto ativo ou descontinuado? | Usuário |
| `painel de chamados` (948 MB) | Está em uso atualmente? | Usuário |
| `Project CRM.zip` (285 MB) | Pode ser removido? Já foi extraído? | Usuário |

---

## 9. Recomendação Final

1. **SARA**: Manter tudo. Nada deve ser removido.
2. **ServiceDesk + Agent**: Manter. São projetos separados.
3. **painel de chamados**: Manter se ainda usado.
4. **AD Auditory**: Revisar uso — 218 MB de arquivos HTML/Excel/logs.
5. **Project CRM**: Revisar uso — 424 MB.
6. **New project + Codex**: Podem ser limpos com segurança.
7. **Project CRM.zip**: Pode ser removido após confirmar que o conteúdo já foi extraído.

Nenhum arquivo foi apagado ou movido durante este inventário.
