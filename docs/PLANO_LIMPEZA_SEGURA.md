# Plano de Limpeza Segura — Documentos / SARA

**Data**: 26/05/2026  
**Baseado no relatório**: RELATORIO_LIMPEZA_DOCUMENTOS.md  
**Nada será executado automaticamente.** Este plano documenta as etapas propostas para aprovação.

---

## Etapa 1 — Backup / Quarentena (antes de qualquer exclusão)

1. Criar uma pasta `C:\Users\joao.silva\Documents\_QUARENTENA`
2. Mover itens candidatos para lá (em vez de excluir diretamente):
   - `New project` → `_QUARENTENA\New project`
   - `Codex` → `_QUARENTENA\Codex`
   - `Project CRM.zip` → `_QUARENTENA\Project CRM.zip`
3. **Não mover** itens com dúvida (AD Auditory, Project CRM)
4. **Não mover** nada do SARA, ServiceDesk ou painel de chamados

---

## Etapa 2 — Limpeza de Artefatos do SARA

Estes itens podem ser limpos sem risco, pois são regeneráveis:

```powershell
# Limpar __pycache__ (regenerado automaticamente)
Get-ChildItem -Path "C:\Users\joao.silva\Documents\SARA" `
  -Directory -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force

# Limpar builds do Agent (regenerado com dotnet build)
Remove-Item -Path "C:\Users\joao.silva\Documents\SARA\SaraServerAgent\bin" -Recurse -Force
Remove-Item -Path "C:\Users\joao.silva\Documents\SARA\SaraServerAgent\obj" -Recurse -Force
```

Economia estimada: ~200 MB (apenas build artifacts).

---

## Etapa 3 — Testar o SARA após limpeza

Após a limpeza dos artefatos, executar:

```cmd
cd C:\Users\joao.silva\Documents\SARA
python run.py
```

Testar:
- [ ] /health → 200
- [ ] /login → 200
- [ ] Login admin
- [ ] /dashboard → 200

Se falhar, restaurar imediatamente da quarentena.

---

## Etapa 4 — Aguardar 7 dias

Manter os itens em `_QUARENTENA` por **7 dias corridos**.
Nenhuma exclusão definitiva antes desse prazo.

---

## Etapa 5 — Exclusão Definitiva (somente após aprovação)

Após 7 dias sem incidentes:

```powershell
# Excluir quarentena (somente com confirmacao manual)
Remove-Item -Path "C:\Users\joao.silva\Documents\_QUARENTENA" -Recurse -Force
```

---

## Cronograma Proposto

| Etapa | Ação | Prazo |
|---|---|---|
| 1 | Mover para quarentena | Dia 1 |
| 2 | Limpar artefatos SARA | Dia 1 |
| 3 | Testar SARA | Dia 1 |
| 4 | Aguardar | Dias 2 a 7 |
| 5 | Excluir quarentena | Dia 8 (após aprovação) |

---

## Itens que NÃO entram no plano

| Item | Motivo |
|---|---|
| `SARA` | Projeto ativo — não limpar |
| `ServiceDesk` | Outro sistema ativo |
| `ServiceDeskAgent` | Agent do ServiceDesk |
| `painel de chamados` | Outro sistema (confirmar uso) |
| `AD Auditory` | Aguardar confirmação do usuário |
| `Project CRM` | Aguardar confirmação do usuário |
| `WindowsPowerShell` | Padrão do Windows |
| `logs/` do SARA | Necessário para suporte |
| `backups/` do SARA | Necessário para recuperação |
| `data/` do SARA | Backup de referência |
| `.env` do SARA | Configuração ativa |

---

## Riscos

| Risco | Probabilidade | Mitigação |
|---|---|---|
| Perder arquivo necessário | Baixa | Quarentena de 7 dias |
| Quebrar build do Agent | Média | `dotnet build` regenera tudo |
| Perder backup de banco | Baixa | Manter backups mais recentes |
| Excluir projeto errado | Muito baixa | Revisão manual antes da exclusão |

---

Este plano requer aprovação antes da execução. Nada foi executado automaticamente.
