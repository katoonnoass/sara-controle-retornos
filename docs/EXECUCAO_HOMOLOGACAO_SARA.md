# Execução da Homologação — SARA

## Dados da Sessão

| Campo | Valor |
|---|---|
| **Data** | ___/___/______ |
| **Horário** | __:__ às __:__ |
| **Ambiente** | Homologação |
| **URL do sistema** | http://localhost:5000 |
| **Versão** | 5.4.0-WEB |
| **Servidor** | Waitress (threads=8) |
| **Banco** | PostgreSQL 16 — localhost:5433/sara |
| **Responsável técnico** | |

---

## Participantes

| Nome | Perfil | Cargo no sistema | Início | Fim |
|---|---|---|---|---|
| | | | | |
| | | | | |

---

## Usuários de Teste

As senhas serão fornecidas individualmente aos participantes durante a sessão. Não armazenar senhas neste documento.

| Perfil | Usuário | Cargo |
|---|---|---|
| PMO / Gestão de Projetos | `vonilto.ferreira` | Gerente |
| Coordenação de Estudos (CE) | `aline.cristine` | Coordenadora |
| Área Responsável / Laboratório | `maykon.santos` | Supervisor |
| Administrador | `admin` | Administrador |

---

## Massa de Teste

### Fluxo normal

| ID | Proposta | Projeto | Cliente | Código | Tipo | Ticket | Status |
|---|---|---|---|---|---|---|---|
| 1 | HOMOLOG-001 | Homologação Fluxo Normal | TESTE HOMOLOGACAO SARA | DOC-HOM-001 | Normal | | |
| 2 | HOMOLOG-002 | Homologação com Prioridade | TESTE HOMOLOGACAO SARA | DOC-HOM-002 | Prioritário | | |
| 3 | HOMOLOG-003 | Homologação Urgente | TESTE HOMOLOGACAO SARA | DOC-HOM-003 | Normal | | |

### Fluxo de reprovação

| ID | Proposta | Projeto | Código | Ticket |
|---|---|---|---|---|
| 4 | HOMOLOG-004 | Homologação Reprovação | DOC-HOM-004 | |
| 5 | HOMOLOG-005 | Homologação Reprovação 2 | DOC-HOM-005 | |

### Massa já criada (pré-homologacão)

| Proposta | Ticket | Status atual |
|---|---|---|
| AUDIT-001 | IDRET00593/26 | Aguardando Avaliação CE |
| AUDIT-003 | IDRET00594/26 | Aguardando Avaliação CE |
| REPROV-001 | IDRET00595/26 | Aguardando Avaliação CE |
| REPROV-002 | IDRET00596/26 | Aguardando Avaliação CE |

---

## Checklist Resumido

### PMO / Gestão de Projetos

| # | Item | Resultado | Evidência |
|---|---|---|---|
| 1 | Acessar o sistema | ⏭️ | |
| 2 | Visualizar dashboard | ⏭️ | |
| 3 | Criar novo retorno (E1) | ⏭️ | ticket: |
| 4 | Confirmar retorno na lista | ⏭️ | |
| 5 | Confirmar retorno em "Avaliar (CE)" | ⏭️ | |
| 6 | Visualizar detalhes do retorno | ⏭️ | |
| 7 | Avançar até "Aguardando Envio Projetos" | ⏭️ | |
| 8 | Executar E5 — Enviar ao cliente | ⏭️ | |
| 9 | Confirmar status **Concluído** | ⏭️ | ticket: |
| 10 | Confirmar retorno não aparece como pendente | ⏭️ | |
| 11 | Testar filtros na lista | ⏭️ | |
| 12 | Testar paginação | ⏭️ | |
| 13 | Testar ordenação por colunas | ⏭️ | |
| 14 | Exportar lista para Excel | ⏭️ | |
| 15 | Verificar dashboard atualizada | ⏭️ | |

### Coordenação de Estudos (CE)

| # | Item | Resultado | Evidência |
|---|---|---|---|
| 1 | Acessar o sistema | ⏭️ | |
| 2 | Visualizar dashboard | ⏭️ | |
| 3 | Acessar "Avaliar (CE)" | ⏭️ | |
| 4 | Selecionar ticket, definir área + avaliador | ⏭️ | |
| 5 | Salvar → "Aguardando Execução" | ⏭️ | |
| 6 | Acessar "Validar (CE)" | ⏭️ | |
| 7 | Validar como **Aprovado** | ⏭️ | auditoria: |
| 8 | Validar como **Reprovado** | ⏭️ | auditoria: |
| 9 | Ticket reprovado reaparece em "Executar" | ⏭️ | |
| 10 | Comentários anteriores visíveis | ⏭️ | |

### Área Responsável / Laboratório

| # | Item | Resultado | Evidência |
|---|---|---|---|
| 1 | Acessar o sistema | ⏭️ | |
| 2 | Visualizar dashboard | ⏭️ | |
| 3 | Acessar "Executar" | ⏭️ | |
| 4 | Registrar execução + comentário | ⏭️ | |
| 5 | Salvar → "Aguardando Validação CE" | ⏭️ | |
| 6 | Reexecutar após reprovação | ⏭️ | |
| 7 | Comentários anteriores preservados | ⏭️ | |

### Administrador

| # | Item | Resultado | Evidência |
|---|---|---|---|
| 1 | Acessar como admin | ⏭️ | |
| 2 | Verificar menus da sidebar | ⏭️ | |
| 3 | Gerenciar usuários | ⏭️ | |
| 4 | Gerenciar patrocinadores | ⏭️ | |
| 5 | Acessar "Status Sessões" | ⏭️ | |
| 6 | Testar bloqueio/desbloqueio | ⏭️ | |
| 7 | Acessar "Auditoria" | ⏭️ | |
| 8 | Ações E1-E5 registradas | ⏭️ | |
| 9 | Não-admin BLOQUEADO | ⏭️ | |

---

## Registro de Problemas

| ID | Data | Relator | Perfil | Módulo | Descrição | Severidade | Evidência | Status | Responsável |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

---

## Decisão Final

( ) **Aprovado** — todos os itens do checklist passaram
( ) **Aprovado com ressalvas** — itens com falha não bloqueantes, plano de correção definido
( ) **Reprovado** — falha crítica no fluxo principal

**Observações:**
____________________________________________________________

**Responsável pela homologação:** ___________________
**Assinatura:** ___________________
**Data:** ___/___/_______
