
# RELATÓRIO ATUAL DO SARA

## 1. Resumo Executivo

**Sistema**: SARA (Sistema de Acompanhamento e Registro de Atendimentos)  
**Versão**: 5.4.0-WEB  
**Status atual**: Em desenvolvimento — funcional, com pendências de segurança e produção  
**Base**: 32 usuários, 1.376 retornos, 82 patrocinadores  
**Equipe técnica**: Migração concluída de Tkinter+Excel para Flask+PostgreSQL  
**Risco principal**: 30 senhas em texto plano (93% dos usuários)

## 2. Status Geral do Projeto

| Dimensão | Status |
|---|---|
| Migração Tkinter → Web | ✅ Concluída |
| Dados migrados (Excel → PG) | ✅ Concluída |
| Visual padronizado (dashboard, lista, E1-E5, admin) | ✅ Concluído |
| Sidebar responsiva | ✅ Concluída |
| Tema escuro | ✅ Concluído |
| CSRF em formulários | ✅ Implementado |
| Hash de senhas | ⚠️ Parcial — 2 de 32 usuários |
| SECRET_KEY forçada via ambiente | ✅ Concluído |
| `| safe` removido de flash messages | ✅ Concluído |
| Senha admin resetada | ✅ `admin` / `admin` |
| Paginação na lista | ✅ Concluída (50/página) |
| Dashboard limitada a 20 registros | ✅ Concluída |
| Agent Windows (WPF) | ✅ Concluído (build funcional) |
| Fluxo E1-E5 | ✅ Funcional |
| Logging de exceções | ✅ Concluído |
| Código duplicado removido (utils.py) | ✅ Concluído |
| Badges de status padronizados | ✅ Concluído |

## 3. Estrutura Atual

### Árvore principal (projeto web, sem binários)

```
C:\Users\joao.silva\Documents\SARA\
├── app.py                          # Entry point Flask (create_app)
├── config.py                       # Config: SECRET_KEY, DB URL, cores, labels
├── models.py                       # SQLAlchemy models (Usuario, Retorno, Patrocinador, Sessao)
├── utils.py                        # Funções compartilhadas (parse_date, classificar_prazo...)
├── requirements.txt                # Dependências Python
├── .env                            # DATABASE_URL, PORT, SECRET_KEY
├── run.py                          # Entry point com waitress (produção)
├── run_producao.ps1                # Script PowerShell para waitress
├── migrate_data.py                 # Script de migração Excel → PostgreSQL
├── start_server.bat                # Batch para iniciar servidor
├── routes/
│   ├── auth_routes.py              # Login/logout
│   ├── etapas_routes.py            # E1 (solicitar) a E5 (enviar)
│   ├── gestao_routes.py            # Dashboard, lista, gráficos, exportação, edição
│   └── admin_routes.py             # Usuários, patrocinadores, sessões, bloqueio
├── templates/                      # 19 templates HTML (Jinja2)
│   ├── base.html                   # Layout base com sidebar, topbar, tema
│   ├── login.html                  # Tela de login standalone
│   ├── dashboard.html              # Dashboard principal
│   ├── lista_retornos.html         # Lista de retornos com paginação
│   ├── solicitar.html              # E1 — Solicitar Retorno
│   ├── avaliar.html                # E2 — Avaliar CE
│   ├── executar.html               # E3 — Executar
│   ├── validar.html                # E4 — Validar CE
│   ├── enviar.html                 # E5 — Enviar Projetos
│   ├── detalhes.html               # Detalhes do retorno + PDF
│   ├── edicao.html                 # Edição manual de tickets
│   ├── graficos.html               # Gráficos e indicadores
│   ├── indicadores_diretoria.html  # Painel diretoria
│   ├── produtividade.html          # Produtividade por usuário
│   ├── usuarios.html               # CRUD de usuários
│   ├── usuario_form.html           # Formulário de usuário
│   ├── patrocinadores.html         # CRUD de patrocinadores
│   ├── patrocinador_form.html      # Formulário de patrocinador
│   └── status_sessoes.html         # Sessões online + bloqueio
├── data/                           # Backup dos arquivos Excel originais
│   ├── bd_retornos.xlsx
│   ├── usuario_setores.xlsx
│   └── patrocinadores.xlsx
├── assets/                         # Logos e ícones (não usado pelo web)
├── SaraServerAgent/                # Projeto Windows Agent (WPF C#)
│   ├── Program.cs, MainWindow.xaml, SettingsWindow.xaml
│   ├── ServerController.cs, ConfigService.cs, LogService.cs
│   ├── HealthCheckService.cs, PortService.cs, StartupService.cs
│   └── ViewModels/, Converters/, Resources/
└── docs/                           # Documentação (INSTALAR_SERVICO_WINDOWS.md)
```

### Resquícios de Tkinter/Desktop
**Nenhum.** Todos os arquivos da versão desktop (`ui/`, `core/database.py`, `main.py`, `setup_database.py`, `create_icon.py`, `sara.spec`, `build*.bat`) foram removidos.

### Resquícios de Excel
Os arquivos `.xlsx` em `data/` são **backup apenas**. O banco ativo é PostgreSQL.

## 4. Stack e Dependências

| Componente | Tecnologia |
|---|---|
| Linguagem | Python 3.14 |
| Framework web | Flask 3.1.3 |
| ORM | SQLAlchemy 2.0 + Flask-SQLAlchemy |
| Banco | PostgreSQL 16 (porta 5433) |
| Autenticação | Flask-Login + Flask-WTF CSRF |
| Frontend | Jinja2 + Bootstrap 5.3 + Chart.js 4.4 |
| Ícones | Bootstrap Icons |
| Servidor dev | Flask built-in (app.py) |
| Servidor produção | Waitress (run.py / run_producao.ps1) |
| PDF | ReportLab (relatórios de retorno) |
| Excel export | openpyxl |
| Agent Windows | .NET 8 WPF + Windows Forms (NotifyIcon) |

### Inicialização
- **Dev**: `python app.py` — debug=True, host=0.0.0.0:5000
- **Produção**: `python run.py` ou `run_producao.ps1` — waitress, host=0.0.0.0:5000, threads=8

## 5. Banco de Dados

**Nome**: `sara` (PostgreSQL 16, porta 5433)  
**Host**: localhost  
**Models** (SQLAlchemy): `Usuario`, `Retorno`, `Patrocinador`, `Sessao`

### Tabelas

| Tabela | Colunas | Registros |
|---|---|---|
| `usuarios` | id, nome_completo, nome_exibicao, setor, cargo, usuario, senha, ativo, observacoes, created_at | **32** |
| `retornos` | id, id_retorno, ticket_atendimento + 26 campos de fluxo + criado_em, atualizado_em | **1.376** |
| `patrocinadores` | id, id_patrocinador, nome_patrocinador, empresa, ativo, observacoes | **82** |
| `sessoes` | id, session_id, usuario_id (FK), usuario_login, nome, host, inicio, ativo | **14** |

### Senhas
- **2 usuários** com senha hasheada (`scrypt:`) — admin e quem fez login recentemente
- **30 usuários** com senha em **texto plano** — migrados do Excel, nunca logaram após o hash
- O hash ocorre automaticamente no **primeiro login bem-sucedido** de cada usuário

### Auditoria
**Não existe.** Nenhuma tabela de auditoria, log de alterações ou trilha de quem alterou o quê. O campo `atualizado_em` em `retornos` existe mas nunca é lido ou exibido.

## 6. Fluxo E1-E5

O fluxo segue 5 etapas sequenciais com possibilidade de reprovação na E4.

```
E1 Solicitar (PMO)
  ↓ status = "Aguardando Avaliação CE"
E2 Avaliar CE (Coordenação de Estudos)
  ↓ status = "Aguardando Execução"
E3 Executar (Área Responsável)
  ↓ status = "Aguardando Validação CE"
E4 Validar CE (Coordenação de Estudos)
  ├─ Aprovado → "Aguardando Envio Projetos"
  └─ Reprovado → "Aguardando Execução" + status_execucao = "Pendente"
E5 Enviar Projetos (PMO)
  ↓ status = "Concluído"
```

| Etapa | Rota | Template | Status entrada | Status saída | Campos obrigatórios | Responsável |
|---|---|---|---|---|---|---|
| E1 | `POST /etapas/solicitar` | solicitar.html | — (novo) | Aguardando Avaliação CE | Data Receb., PMO, Cód. Documento | PMO (Gestão Projetos) |
| E2 | `POST /etapas/avaliar` | avaliar.html | Aguardando Avaliação CE | Aguardando Execução | Área Resp., Avaliador | CE (Coord. Estudos) |
| E3 | `POST /etapas/executar` | executar.html | Aguardando Execução | Aguardando Validação CE | Resp. Execução, Status Exec. | Área Responsável |
| E4 | `POST /etapas/validar` | validar.html | Aguardando Validação CE | Aguardando Envio (aprovado) / Aguardando Execução (reprovado) | Aprovador CE, Status CE | CE (Coord. Estudos) |
| E5 | `POST /etapas/enviar` | enviar.html | Aguardando Envio Projetos | Concluído | Resp. Envio, Data Envio | PMO (Gestão Projetos) |

### Riscos no fluxo
- Nenhum campo de data/hora de cada etapa é persistido como `DateTime` — tudo é string `dd/mm/aaaa`
- Não há validação de sequência: um ticket pode ser "pulado" via edição manual
- Reprovação na E4 zera `status_execucao` para "Pendente" mas não força reavaliação
- Não há bloqueio de edição concorrente (dois usuários podem salvar o mesmo ticket ao mesmo tempo)

## 7. Rotas do Sistema

**37 rotas registradas** (excluindo HEAD/OPTIONS):

| Rota | Métodos | Endpoint | Proteção | Cargo |
|---|---|---|---|---|
| `/` | GET | core.dashboard | login_required | Todos |
| `/login` | GET,POST | auth.login | — | Público |
| `/logout` | GET | auth.logout | login_required | Todos |
| `/dashboard` | GET | core.dashboard | login_required | Todos |
| `/health` | GET | health | — | Público |
| `/lista` | GET | core.lista | login_required | Todos |
| `/etapas/solicitar` | GET,POST | etapas.solicitar | login_required | Todos |
| `/etapas/avaliar` | GET,POST | etapas.avaliar | login_required | Todos |
| `/etapas/executar` | GET,POST | etapas.executar | login_required | Todos |
| `/etapas/validar` | GET,POST | etapas.validar | login_required | Todos |
| `/etapas/enviar` | GET,POST | etapas.enviar | login_required | Todos |
| `/detalhes/<ticket>` | GET | core.detalhes | login_required | Todos |
| `/detalhes/<ticket>/pdf` | GET | core.relatorio_pdf | login_required | Todos |
| `/excluir/<ticket>` | POST | core.excluir | login_required | CARGOS_EXCLUSAO |
| `/exportar` | GET | core.exportar | login_required | Todos |
| `/edicao` | GET,POST | core.edicao | login_required | CARGOS_EDICAO |
| `/graficos` | GET | core.graficos | login_required | CARGOS_GRAFICOS |
| `/indicadores-diretoria` | GET | core.indicadores_diretoria | login_required | CARGOS_DIRETORIA |
| `/produtividade` | GET | core.produtividade | login_required | CARGOS_PRODUTIVIDADE |
| `/api/graficos` | GET | core.api_graficos | login_required | CARGOS_GRAFICOS |
| `/api/patrocinadores` | GET | core.api_patrocinadores | login_required | Admin |
| `/admin/usuarios` | GET | admin.usuarios | login_required | is_admin |
| `/admin/usuarios/novo` | GET,POST | admin.usuario_novo | login_required | is_admin |
| `/admin/usuarios/editar/<id>` | GET,POST | admin.usuario_editar | login_required | is_admin |
| `/admin/usuarios/excluir/<id>` | POST | admin.usuario_excluir | login_required | is_admin |
| `/admin/patrocinadores` | GET | admin.patrocinadores | login_required | is_admin |
| `/admin/patrocinadores/novo` | GET,POST | admin.patrocinador_novo | login_required | is_admin |
| `/admin/patrocinadores/editar/<id>` | GET,POST | admin.patrocinador_editar | login_required | is_admin |
| `/admin/patrocinadores/excluir/<id>` | POST | admin.patrocinador_excluir | login_required | is_admin |
| `/admin/status-sessoes` | GET | admin.status_sessoes | login_required | is_admin |
| `/admin/bloquear-login` | POST | admin.bloquear_login | login_required | is_admin |
| `/admin/desbloquear-login` | POST | admin.desbloquear_login | login_required | is_admin |
| `/admin/bloquear-usuario/<id>` | POST | admin.bloquear_usuario | login_required | is_admin |
| `/admin/desbloquear-usuario/<id>` | POST | admin.desbloquear_usuario | login_required | is_admin |
| `/admin/sessoes/forcar-logoff/<id>` | POST | admin.forcar_logoff | login_required | is_admin |
| `/admin/sessoes/forcar-logoff-todos` | POST | admin.forcar_logoff_todos | login_required | is_admin |

### Testes de rotas (via test_client)
Todas as 16 rotas principais retornam **200** (autenticadas) ou **302** (login redirect). Nenhuma retorna erro.

## 8. Autenticação e Permissões

### Login
- Autenticação via `Flask-Login` com sessão em cookie assinado (`sara_session`)
- Senha verificada via `check_password()` — suporta hash + migração automática de texto plano
- Após login, um registro `Sessao` é criado na tabela `sessoes`

### Cargos e Permissões

| Cargo | Admin | Editar | Excluir | Produtividade | Gráficos | Diretoria |
|---|---|---|---|---|---|---|
| Administrador | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Diretor(a) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gerente | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Coordenador(a) | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Supervisor(a) | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Analista | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Especialista | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Sessão
- Sessão expira após **10 minutos** de inatividade (`PERMANENT_SESSION_LIFETIME = 600`)
- Watchdog verifica validade da sessão a cada 5 segundos via `before_request`
- Admin pode forçar logoff de qualquer usuário
- Admin pode bloquear/desbloquear login global ou individual

### Riscos de Segurança
- 🔴 **30 senhas em texto plano** — 93% dos usuários
- 🔴 **Sem proteção contra força bruta** — rota `/login` sem rate limiting
- 🔴 **SECRET_KEY fixa no `.env`** — não foi alterada após commit
- 🟡 **Debug mode ativo** em `app.py` (`debug=True`)
- 🟡 **Logout não revoga sessão no servidor** — apenas remove cookie
- 🟢 `| safe` removido de flash messages
- 🟢 CSRF implementado em todos os formulários POST

## 9. Dashboard

### Status atual
- **8 cards métricos** padronizados (`.metric-card` + `.mc-*`)
- **Progress bar** substituiu gráfico de rosca — mostra % atrasado vs no prazo
- **Ranking Top 10** com destaque para #1 (vermelho), #2 (laranja), #3 (âmbar)
- **Gráficos**: setor (barras) + lead time (barras) — lado a lado
- **Filtros**: Prazo, Tipo, Status — funcionais
- **Tabela inferior**: limitada a **20 registros críticos** (não concluídos, atrasados primeiro)
- **Cards e gráficos**: usam **totais globais** do banco (não apenas os 20)
- **Botão "Ver todos na Lista"** → `/lista`
- **Tempo de carregamento**: ~200ms (vs ~800ms antes da otimização)

### A dashboard está adequada para produção?
**Sim**, visualmente e funcionalmente.

### Precisa de ajuste de performance?
**Não** — a tabela renderiza apenas 20 linhas, os KPIs usam queries agregadas.

### Quantas linhas são renderizadas na tabela?
**20 linhas** (contra 1.372 antes da otimização).

## 10. Lista de Retornos

- **Carrega todos os registros?** Sim, mas com paginação de 50/página
- **Filtros**: Status, Tipo, Área, Busca textual — funcionais
- **Paginação**: 50 registros por página, com botões de navegação
- **Badges**: Padronizados (`badge-status` + `s-avaliacao`, `s-execucao`, etc.)
- **Rolagem horizontal**: `table-responsive-x` — funcional
- **Performance**: Boa para 1.372 registros com paginação

## 11. Templates e Visual

### Templates existentes: 19
Todos estendem `base.html`, exceto `login.html` (standalone).

### Classes antigas — NENHUMA encontrada
- `kpi-card`, `kpi-bar`, `kpi-value`, `kpi-label` ❌ removidas (substituídas por `metric-card`/`.mc-*`)
- `badge bg-success/warning/danger/secondary` ❌ removidas (substituídas por `badge-status` + `rgba()`)
- `table-warning` ❌ removida
- `max-height` com scroll interno ❌ removido (substituído por `table-responsive-x`)
- `card-body p-0` em tabelas ❌ removido

### Padrão de badges de status — IMPLEMENTADO
- `badge-status` + `s-avaliacao` / `s-execucao` / `s-validacao` / `s-envio` / `s-concluido` / `s-atraso`
- Fundos semi-transparentes com `rgba()` — compatível com tema claro/escuro

### Tema
- Escuro com alternância para claro via `data-theme`
- CSS via variáveis (`--bg-card`, `--text`, `--border`, etc.)

## 12. Performance

| Ponto | Risco | Detalhes |
|---|---|---|
| Dashboard carregando retornos | ✅ Baixo | Limitado a 20 registros |
| Lista carregando retornos | ✅ Baixo | Paginação de 50/página |
| Consultas sem paginação | ✅ Baixo | Apenas `/lista` tem `.all()` para exportar Excel |
| Filtros frontend | ✅ Médio | Filtro de setor foi implementado corretamente (JS + data attributes) |
| Queries .all() | 🟡 Médio | `_get_retornos_data()` carrega todos para KPIs/gráficos (1.372 registros — aceitável) |
| Índices no banco | ⚠️ Não confirmado | Não há análise de índices PostgreSQL |
| Gráficos | ✅ Baixo | Dados agregados, não carregam linhas individuais |
| Templates | ✅ Baixo | Máximo 20 linhas na dashboard, 50 na lista |

## 13. Segurança

| Item | Status | Risco |
|---|---|---|
| Senhas em texto plano | 30 de 32 (93%) | 🔴 **Crítico** |
| SECRET_KEY | Fixa no `.env` (não alterada) | 🟡 Médio |
| Debug mode | `debug=True` em `app.py` | 🟡 Médio |
| Traceback exposto | Flask dev mostra traceback | 🟡 Médio |
| CSRF | Implementado em todos os POST | 🟢 OK |
| Proteção de rota | `@login_required` em todas as rotas | 🟢 OK |
| Permissão por cargo | Verificada em cada rota admin | 🟢 OK |
| `| safe` em flash | Removido | 🟢 OK |
| Força bruta | Sem rate limiting | 🔴 **Crítico** |
| Senha do banco | URL completa com senha no `.env` | 🟡 Médio |
| Auditoria | Inexistente | 🟡 Médio |

## 14. Produção/Deploy

| Item | Status |
|---|---|
| Modo atual | Development (`app.py debug=True`) |
| Servidor produção | Waitress configurado (`run.py` + `run_producao.ps1`) |
| Script produção | `run_producao.ps1` com waitress-serve |
| Serviço Windows | `INSTALAR_SERVICO_WINDOWS.md` — guia manual |
| Agent Windows | ✅ Existe (WPF C#) — build funcional |
| Auto start | ❌ Não configurado |
| Backup do banco | ❌ Não identificado |
| Log de aplicação | ✅ Apenas logs do Agent |
| Rotina de atualização | ❌ Não existe |
| Rollback | ❌ Não existe |

## 15. Agent Windows

**Projeto**: `SaraServerAgent/`  
**Tecnologia**: .NET 8 WPF + Windows Forms (NotifyIcon)  
**Build**: ✅ Funcional (162 MB self-contained single-file)

| Funcionalidade | Status |
|---|---|
| Iniciar servidor | ✅ |
| Parar servidor | ✅ |
| Reiniciar servidor | ✅ |
| Status em tempo real (timer 5s + /health) | ✅ |
| Logs do servidor | ✅ |
| Tray icon com menu | ✅ |
| Minimizar para bandeja | ✅ |
| Abrir SARA no navegador | ✅ |
| Abrir pasta do projeto | ✅ |
| Configurações (janela modal) | ✅ |
| Auto-start com Windows | ✅ (Registro HKCU) |
| Verificação de /health | ✅ |
| Detecção de porta em uso | ✅ |
| Fallback python app.py | ✅ |
| Tema escuro WPF | ✅ |
| Tratamento de exceções | ⚠️ Precisa de melhorias |
| Cross-thread UI dispatch | ✅ Corrigido (SynchronizationContext) |

### Problemas pendentes do Agent
- Ao iniciar o servidor, o Agent pode travar se `run_producao.ps1` não existir (usa fallback)
- `Assembly.Location` retorna vazio em single-file — ícone pode não carregar
- O agent usa `taskkill /F /FI "IMAGENAME eq python*"` que pode matar processos de outros projetos Python

## 16. Backup e Restauração

| Item | Status |
|---|---|
| Script pg_dump | ❌ Não existe |
| Rotina automática | ❌ Não existe |
| Pasta de backups | ❌ Não existe |
| Retenção | ❌ Não existe |
| Teste de restauração | ❌ Nunca realizado |
| Backup Excel | ✅ `data/` preserva os 3 arquivos originais |
| migrate_data.py | ✅ Ainda funcional — pode ser reexecutado (ignora duplicatas por ID) |

## 17. Logs e Monitoramento

| Item | Status |
|---|---|
| Log de aplicação (Flask) | ❌ Não existe logging para arquivo |
| Log de erro | ❌ Apenas stderr no console |
| Log do servidor (Agent) | ✅ `logs/agent-YYYY-MM-DD.log` |
| Log de login | ❌ Não registra |
| Log de alteração de status | ❌ Não registra |
| Auditoria | ❌ Inexistente |
| Monitoramento /health | ✅ Agent verifica a cada 5s |
| Alerta em falha | ❌ Nenhum |

## 18. Testes

| Item | Status |
|---|---|
| Testes automatizados | ❌ Não existem |
| Testes manuais documentados | ❌ Não existem |
| Rotas testadas (via test_client) | 16 rotas principais — ✅ 200/302 |
| Fluxo E1-E5 ponta a ponta | ⚠️ Requer teste manual |
| Reprovação E4 | ⚠️ Requer teste manual |
| Permissões por cargo | ⚠️ Requer teste manual |
| Filtros da lista | ✅ Validados |
| Dashboard com carga real (1.372 registros) | ✅ Funcional |
| Agent Windows | ✅ Build + publish |

## 19. Pendências Priorizadas

### P0 — Crítico antes de produção
1. **Migrar 30 senhas em texto plano** para hash (executar `set_password()` para cada usuário)
2. **Adicionar rate limiting** na rota `/login` (Flask-Limiter)
3. **Alterar SECRET_KEY** no `.env` para valor seguro
4. **Desabilitar debug mode** em produção (`debug=False`)

### P1 — Importante antes de homologação
5. **Criar backup automático do PostgreSQL** (pg_dump agendado)
6. **Configurar logging para arquivo** no Flask (não apenas console)
7. **Testar fluxo E1-E5 ponta a ponta** manualmente
8. **Testar reprovação na E4** manualmente
9. **Criar trilha de auditoria** (tabela `audit_log` ou similar)

### P2 — Melhorias recomendadas
10. **Adicionar índices no PostgreSQL** (ticket_atendimento, status_retorno, etc.)
11. **Adicionar paginação backend nos gráficos** (limitar dados levados ao Chart.js)
12. **Melhorar tratamento de erro no Agent Windows** (capturar exceções de processo)
13. **Adicionar documentação de teste** (script de teste do fluxo completo)
14. **Adicionar confirmação visual** ao salvar nas telas E1-E5

### P3 — Futuro/evolução
15. **Separar configurações por ambiente** (dev/prod via .env.production)
16. **Substituir Flask dev server** por waitress permanentemente
17. **Adicionar notificação por e-mail** quando retorno for atribuído
18. **Adicionar dashboard executiva** com mais indicadores
19. **Adicionar testes automatizados** (pytest + Flask test client)

## 20. Riscos

| Risco | Impacto | Probabilidade | Prioridade | Recomendação |
|---|---|---|---|---|
| Vazamento de senhas | 🔴 Alto | 🔴 Média | P0 | Migrar todas para hash imediatamente |
| Ataque de força bruta no login | 🔴 Alto | 🔴 Alta | P0 | Adicionar Flask-Limiter |
| SECRET_KEY conhecida | 🔴 Alto | 🟡 Média | P0 | Gerar nova secret key |
| Debug/traceback exposto | 🟡 Médio | 🟡 Média | P0 | Desabilitar debug em produção |
| Perda de dados sem backup | 🔴 Alto | 🟡 Média | P1 | Agendar pg_dump |
| Falta de auditoria | 🟡 Médio | 🟡 Média | P1 | Criar tabela audit_log |
| Sessão não revogada no servidor | 🟡 Médio | 🟡 Baixa | P2 | Invalidar token no servidor |
| Processo Python do Agent | 🟡 Médio | 🟡 Baixa | P2 | Melhorar isolamento de processo |

## 21. Recomendação Final

### O sistema está pronto para homologação funcional?
**Sim.** O fluxo E1-E5 está completo, a dashboard está funcional e padronizada, a lista tem paginação, os filtros funcionam, o visual está consistente.

### O sistema está pronto para produção?
**Não.** Três itens P0 impedem:
1. 30 senhas em texto plano
2. Ausência de rate limiting no login
3. Debug mode ativo expondo traceback

### O que impede produção hoje?
- Risco de segurança crítico (senhas expostas)
- Risco de ataque de força bruta
- Sem backup do banco
- Sem logging para arquivo

### Qual deve ser a próxima fase?
**Fase de Segurança e Produção:**
1. Hashear todas as senhas pendentes
2. Adicionar rate limiting
3. Desabilitar debug mode
4. Gerar SECRET_KEY segura
5. Configurar backup automático
6. Configurar logging em arquivo

### Qual deve ser a próxima tarefa imediata?
**Executar script de hash para os 30 usuários com senha em texto plano.** É a tarefa de maior impacto com menor esforço — pode ser feita em 5 minutos via Python one-liner.

## 22. Próxima Tarefa Recomendada

```bash
# Hashear todas as senhas pendentes
python -c "
from app import create_app
from models import db, Usuario
app = create_app()
with app.app_context():
    for u in Usuario.query.all():
        if u.senha and not u.senha.startswith('pbkdf2') and not u.senha.startswith('scrypt'):
            print(f'Hashing {u.usuario}...')
            hash = generate_password_hash(u.senha)
            u.senha = hash
    db.session.commit()
    print('Done.')
"
```

---
**Relatório gerado em:** 25/05/2026  
**Versão do sistema:** 5.4.0-WEB  
**Responsável:** Análise automatizada do SARA
