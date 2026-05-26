# Plano de Homologação — SARA

**Sistema**: SARA (Sistema de Acompanhamento e Registro de Atendimentos)
**Versão**: 5.4.0-WEB
**Data do plano**: 26/05/2026
**Responsável**: Time de desenvolvimento SARA

---

## 1. Objetivo da Homologação

Validar com usuários-chave se o SARA web está funcional, intuitivo e correto para substituir o processo anterior (Tkinter + Excel) no dia a dia operacional.

A homologação cobre:
- Fluxo completo de retorno (E1 → E5)
- Fluxo de reprovação e recuperação
- Dashboard e indicadores
- Lista de retornos com filtros e paginação
- Administração de usuários e patrocinadores
- Auditoria de ações
- Experiência visual e usabilidade geral

---

## 2. Perfis Participantes

| Perfil | Cargo no sistema | Responsabilidade |
|---|---|---|
| **PMO / Gestão de Projetos** | Administrador, Gerente | Criar retornos (E1), Enviar ao cliente (E5) |
| **Coordenação de Estudos (CE)** | Coordenador(a) | Avaliar (E2), Validar (E4) |
| **Área Responsável / Laboratório** | Supervisor(a), Analista | Executar retorno (E3) |
| **Administrador do sistema** | Administrador | Gerenciar usuários, patrocinadores, auditoria |

---

## 3. Escopo do Teste

### Dentro de escopo

- [x] Login e logout
- [x] Criação de retorno (E1) com múltiplos códigos de documento
- [x] Avaliação CE (E2) — direcionamento para área responsável
- [x] Execução (E3) — registro de execução e comentários
- [x] Validação CE (E4) — aprovação e reprovação
- [x] Envio ao cliente (E5) — conclusão do retorno
- [x] Dashboard com cards métricos, progress bar, ranking, gráficos
- [x] Lista de retornos com filtros e paginação
- [x] Edição manual de tickets
- [x] Gestão de usuários (CRUD)
- [x] Gestão de patrocinadores (CRUD)
- [x] Status de sessões e bloqueio de login
- [x] Auditoria de ações
- [x] Tema escuro e responsividade
- [x] Agent Windows (iniciar/parar servidor)

### Fora de escopo

- [ ] Testes de performance com carga (será feito em etapa posterior)
- [ ] Testes de segurança avançados (pentest)
- [ ] Migração de dados históricos do Excel
- [ ] Backup/restore do banco (já implementado, não testado em homologação)

---

## 4. Legenda dos Checklists

Cada item deve ser preenchido com:

| Símbolo | Significado |
|---|---|
| ✅ | Aprovado |
| ❌ | Reprovado |
| ⏭️ | Não testado |
| 👁️ | Evidência anexada (print, ticket, auditoria) |

---

## 5. Checklist por Perfil

### 5.1 PMO / Gestão de Projetos

| # | Item | Resultado | Evidência |
|---|---|---|---|
| 1 | Acessar o sistema com usuário e senha próprios | ⏭️ | |
| 2 | Visualizar dashboard com indicadores corretos | ⏭️ | |
| 3 | Criar um novo retorno (E1) com código de documento | ⏭️ | ticket: |
| 4 | Confirmar que o retorno aparece na lista | ⏭️ | |
| 5 | Confirmar que o retorno aparece na tela "Avaliar (CE)" | ⏭️ | |
| 6 | Visualizar detalhes do retorno | ⏭️ | |
| 7 | Avançar retorno até "Aguardando Envio Projetos" (após validação) | ⏭️ | |
| 8 | Executar E5 — Enviar ao cliente | ⏭️ | |
| 9 | Confirmar status **Concluído** | ⏭️ | ticket: |
| 10 | Confirmar que o retorno não aparece mais como pendente | ⏭️ | |
| 11 | Testar filtros na lista (status, tipo, área, busca) | ⏭️ | |
| 12 | Testar paginação na lista | ⏭️ | |
| 13 | Testar ordenação por colunas na lista | ⏭️ | |
| 14 | Exportar lista para Excel | ⏭️ | arquivo: |
| 15 | Verificar dashboard atualizada | ⏭️ | print: |

### 5.2 Coordenação de Estudos (CE)

| # | Item | Resultado | Evidência |
|---|---|---|---|
| 1 | Acessar o sistema | ⏭️ | |
| 2 | Visualizar dashboard | ⏭️ | |
| 3 | Acessar "Avaliar (CE)" e ver tickets pendentes | ⏭️ | |
| 4 | Selecionar ticket e definir área responsável + avaliador | ⏭️ | |
| 5 | Salvar e confirmar avanço para "Aguardando Execução" | ⏭️ | |
| 6 | Acessar "Validar (CE)" e ver tickets executados | ⏭️ | |
| 7 | Validar como **Aprovado** → "Aguardando Envio" | ⏭️ | auditoria: |
| 8 | Validar como **Reprovado** → "Aguardando Execução" | ⏭️ | auditoria: |
| 9 | Confirmar que o ticket reprovado reaparece em "Executar" | ⏭️ | |
| 10 | Verificar que comentários de etapas anteriores são visíveis | ⏭️ | |

### 5.3 Área Responsável / Laboratório

| # | Item | Resultado | Evidência |
|---|---|---|---|
| 1 | Acessar o sistema | ⏭️ | |
| 2 | Visualizar dashboard | ⏭️ | |
| 3 | Acessar "Executar" e ver tickets aguardando | ⏭️ | |
| 4 | Selecionar ticket e registrar execução + comentário | ⏭️ | |
| 5 | Salvar e confirmar avanço para "Aguardando Validação CE" | ⏭️ | |
| 6 | Em caso de reprovação: reexecutar e registrar novo comentário | ⏭️ | |
| 7 | Confirmar que comentários anteriores são preservados (histórico) | ⏭️ | |

### 5.4 Administrador

| # | Item | Resultado | Evidência |
|---|---|---|---|
| 1 | Acessar o sistema como admin | ⏭️ | |
| 2 | Verificar todos os menus disponíveis na sidebar | ⏭️ | print: |
| 3 | Gerenciar usuários (criar, editar, excluir) | ⏭️ | |
| 4 | Gerenciar patrocinadores (criar, editar, desativar) | ⏭️ | |
| 5 | Acessar "Status Sessões" e ver usuários online | ⏭️ | |
| 6 | Testar bloqueio/desbloqueio de login | ⏭️ | |
| 7 | Acessar "Auditoria" e filtrar por ação, ticket, usuário | ⏭️ | print: |
| 8 | Confirmar que ações E1-E5 estão registradas na auditoria | ⏭️ | auditoria: |
| 9 | Confirmar que usuário não-admin **não** acessa auditoria | ⏭️ | |

---

## 6. Ambiente de Homologação

| Item | Valor |
|---|---|
| **URL do sistema** | http://192.168.1.235:5000 |
| **Banco de dados** | PostgreSQL 16 — `sara` (localhost:5433) |
| **Versão do sistema** | 5.4.0-WEB |
| **Servidor** | Waitress (threads=8) |
| **Responsável técnico** | Time de desenvolvimento SARA |
| **Observação** | Não utilizar dados oficiais ou sensíveis sem autorização prévia. Os retornos criados durante o teste devem usar cliente "TESTE HOMOLOGACAO SARA" para facilitar identificação e limpeza posterior. |

---

## 7. Agenda da Homologação

| Data | Horário | Perfil | Participante | Responsável técnico | Status |
|---|---|---|---|---|---|
| ___/___/___ | __:__ | PMO / Gestão de Projetos | | | Pendente |
| ___/___/___ | __:__ | Coordenação de Estudos (CE) | | | Pendente |
| ___/___/___ | __:__ | Área Responsável / Lab. | | | Pendente |
| ___/___/___ | __:__ | Administrador | | | Pendente |

---

## 8. Roteiro de Teste E1-E5 — Fluxo Normal

### Massa de teste sugerida

| # | Proposta | Projeto | Cliente | Código | Tipo |
|---|---|---|---|---|---|
| 1 | HOMOLOG-001 | Homologação Fluxo Normal | Cliente Homologação | DOC-HOM-001 | Normal |
| 2 | HOMOLOG-002 | Homologação com Prioridade | Cliente Homologação | DOC-HOM-002 | Prioritário |
| 3 | HOMOLOG-003 | Homologação Urgente | Cliente Homologação | DOC-HOM-003 | Normal |

### Roteiro

1. Login como **PMO** (usuário e senha definidos pelo administrador)
2. Acessar "Solicitar Retorno"
3. Criar retorno com os dados acima
4. Anotar o ticket gerado (ex: `IDRET00XXX/26`)
5. Confirmar que o status inicial é "Aguardando Avaliação CE"
6. Login como **Coordenador CE** (usuário e senha fornecidos individualmente)
7. Acessar "Avaliar (CE)", selecionar o ticket
8. Preencher área responsável e avaliador, salvar
9. Confirmar status: "Aguardando Execução"
10. Login como **Supervisor** (usuário e senha fornecidos individualmente)
11. Acessar "Executar", selecionar o ticket
12. Preencher responsável e status, salvar
13. Confirmar status: "Aguardando Validação CE"
14. Login como **Coordenador CE** novamente
15. Acessar "Validar (CE)", selecionar o ticket
16. Marcar como **Aprovado**, salvar
17. Confirmar status: "Aguardando Envio Projetos"
18. Login como **PMO** novamente
19. Acessar "Enviar Projetos", selecionar o ticket
20. Preencher data de envio, salvar
21. Confirmar status: **Concluído**
22. Verificar que o ticket aparece na lista como Concluído
23. Verificar dashboard — ticket concluído não conta como pendente

---

## 9. Roteiro de Reprovação

### Massa de teste sugerida

| # | Proposta | Projeto | Código |
|---|---|---|---|
| 4 | HOMOLOG-004 | Homologação Reprovação | DOC-HOM-004 |
| 5 | HOMOLOG-005 | Homologação Reprovação 2 | DOC-HOM-005 |

### Roteiro

1. Avançar o retorno até E3 (Executar)
2. Login como **Coordenador CE**
3. Acessar "Validar (CE)", selecionar o ticket
4. Marcar como **Reprovado**, preencher comentário
5. Confirmar que o status voltou para "Aguardando Execução"
6. Confirmar que `status_execucao` voltou para "Pendente"
7. Login como **Supervisor**
8. Reexecutar o ticket (E3 novamente)
9. Login como **Coordenador CE**
10. Validar como **Aprovado**
11. Login como **PMO**
12. Enviar e concluir
13. Confirmar status final: **Concluído**
14. Verificar auditoria — devem constar 2 registros de validação (reprovado + aprovado)

---

## 10. Teste de Dashboard

- [ ] KPIs (8 cards) com valores condizentes com a base
- [ ] Progress bar de prazo com percentuais coerentes
- [ ] Ranking Top 10 com destaque visual para #1, #2, #3
- [ ] Gráfico de setor (barras)
- [ ] Gráfico de lead time (barras)
- [ ] Tabela de retornos críticos (máximo 20 itens)
- [ ] Botão "Ver todos na Lista" → /lista
- [ ] Filtros (prazo, tipo, status) funcionando
- [ ] Clique em card métrico aplica filtro correspondente

---

## 11. Teste de Lista de Retornos

- [ ] Lista carrega com paginação
- [ ] Filtro por status funciona
- [ ] Filtro por tipo funciona
- [ ] Filtro por área funciona
- [ ] Busca textual funciona
- [ ] Checkbox "Mostrar excluídos" funciona (admin)
- [ ] Paginação (50/página) funciona
- [ ] Ordenação por colunas funciona
- [ ] Botão "Excel" exporta dados atuais

---

## 12. Teste de Auditoria

- [ ] Ações E1-E5 registradas na auditoria
- [ ] Reprovação registrada com status_anterior e status_novo corretos
- [ ] Filtro por ticket funciona
- [ ] Filtro por ação funciona
- [ ] Filtro por usuário funciona
- [ ] Paginação funciona
- [ ] Apenas admin acessa (usuário comum é bloqueado)
- [ ] Nenhum dado sensível (senha, hash, SECRET_KEY) visível

---

## 13. Critérios de Aprovação

### Aprovado
- Todos os itens do checklist do perfil foram executados e passaram
- Fluxo E1-E5 completo funcionou sem erros
- Reprovação e recuperação funcionaram corretamente
- Dashboard reflete os dados corretamente
- Auditoria registra todas as ações
- Nenhum erro crítico ou bloqueante identificado

### Aprovado com Ressalvas
- Até 3 itens do checklist não passaram, mas:
  - Não afetam o fluxo principal
  - Têm plano de correção conhecido
  - Não expõem dados sensíveis
  - Não causam perda de dados

### Reprovado
- Fluxo E1-E5 apresenta erro que impede conclusão
- Reprovação não retorna para execução
- Dados são perdidos ou exibidos incorretamente
- Auditoria não registra ações
- Segurança comprometida (dados sensíveis expostos)

---

## 14. Modelo de Registro de Problemas

| Campo | Exemplo |
|---|---|
| ID | PROB-001 |
| Data | 26/05/2026 |
| Relator | João Silva (PMO) |
| Módulo | E2 - Avaliar CE |
| Descrição | Após salvar avaliação, mensagem de erro aparece |
| Severidade | Alta / Média / Baixa |
| Evidência | print_screen_001.png |
| Status | Aberto / Em análise / Corrigido / Fechado |
| Observações | |

---

## 15. Modelo de Aceite

```markdown
### Termo de Aceite — Homologação SARA

**Perfil:** _______________
**Responsável:** _______________
**Data:** ___/___/_______

( ) Aprovado
( ) Aprovado com ressalvas: ________________________________
( ) Reprovado

**Observações:**
____________________________________________________________
____________________________________________________________

**Assinatura:** _______________________
```

---

## 16. Evidências Esperadas

Após a homologação, coletar:
- [ ] Prints da dashboard após criar/concluir retornos
- [ ] Tickets gerados (IDRET00XXX/26)
- [ ] Tela de auditoria filtrada por ticket
- [ ] Logs do arquivo `logs/sara-app.log`
- [ ] Logs do Agent (`logs/agent-*.log`)
- [ ] Relatório de problemas encontrados (se houver)

---

## 17. Plano de Rollback

Caso algo dê errado durante a homologação:

1. **Parar servidor** via Agent Windows ou `Ctrl+C` no terminal
2. **Restaurar banco** a partir do último backup em `backups/`:
   ```powershell
   pg_restore --host=localhost --port=5433 --username=postgres \
              --dbname=sara backups\sara_MAIS_RECENTE.dump
   ```
3. **Reiniciar servidor** com `python run.py`
4. **Validar** `/health` retorna 200 e login funciona
5. **Registrar** o rollback no log e no relatório de problemas

### Contatos de emergência

| Contato | Responsabilidade |
|---|---|
| Desenvolvimento SARA | Correção de bugs, suporte técnico |
| DBA | Suporte PostgreSQL, restauração de backup |
| Administrador do sistema | Liberação de acesso, criação de usuários |

---

## 18. Próxima Ação Recomendada

1. Revisar este plano com o gerente do projeto
2. Agendar sessão de homologação com cada perfil
3. Preparar ambiente de homologação (produção ou staging)
4. Executar os roteiros de teste
5. Coletar evidências e registrar problemas
6. Aplicar correções necessárias
7. Obter termo de aceite de cada perfil
8. Homologação concluída → autorização para produção
