<p align="center">
  <img src="assets/sara_icon.ico" width="80" alt="SARA logo">
</p>

<h1 align="center">🚀 SARA</h1>
<p align="center">
  <strong>Sistema de Acompanhamento e Registro de Atendimentos</strong>
  <br>
  <em>Controle de Retornos — E1 a E5</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-em%20produ%C3%A7%C3%A3o-success?style=flat-square">
  <img src="https://img.shields.io/badge/vers%C3%A3o-5.4.0--WEB-blue?style=flat-square">
  <img src="https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square&logo=python">
  <img src="https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql">
  <img src="https://img.shields.io/badge/.NET-8-512BD4?style=flat-square&logo=dotnet">
  <img src="https://img.shields.io/badge/licen%C3%A7a-EPHAR%20%C2%AE-yellow?style=flat-square">
</p>

---

## 📋 Sobre

O **SARA** é um sistema web completo para **controle e acompanhamento de retornos** de documentos técnicos, seguindo o fluxo de 5 etapas (E1 → E5). Desenvolvido para a **EPHAR Indústria Farmacêutica**, o sistema automatiza todo o ciclo de vida dos retornos, desde a solicitação até a conclusão.

> ✅ Em produção · 🐍 Python/Flask · 🐘 PostgreSQL · 🖥️ Agente Windows (.NET 8)

---

## 🧭 Fluxo de Etapas

```
📥 E1 — Solicitação
  ↓
📋 E2 — Avaliação CE (Coordenação de Estudos)
  ↓
🔧 E3 — Execução (Área Responsável)
  ↓
✅ E4 — Validação CE
  ↓
📤 E5 — Envio Projetos → Cliente
```

Cada etapa possui registro de **auditoria**, **controle de prazo** e **notificações** de urgência.

---

## ✨ Funcionalidades

### 🎯 Gestão de Retornos
- Cadastro e acompanhamento de retornos por cliente/projeto
- Fluxo completo E1–E5 com registro de responsáveis e datas
- Classificação automática de prazos (normal, próximo ao vencimento, em atraso)
- Exclusão lógica com responsável e justificativa

### 📊 Dashboard
- Cards de KPI com métricas em tempo real
- Gráfico de distribuição por tipo de retorno
- Ranking Top 10 por área responsável
- Tabela com últimos 20 retornos
- Indicadores de urgência (prazo final, em atraso)

### 👥 Usuários e Perfis
- Múltiplos níveis de acesso (Administrador, Diretor, Gerente, Coordenador, Supervisor)
- Controle granular de permissões por cargo
- Bloqueio administrativo de login

### 📈 Relatórios e Exportação
- Exportação para Excel com dados consolidados
- Indicadores de produtividade por responsável
- Gráficos interativos com Chart.js
- Relatórios de diretoria

### 🔒 Segurança
- Senhas hasheadas com Werkzeug (`scrypt`)
- Proteção CSRF em todos os formulários
- Rate limiting no login (5/minuto, 20/hora por IP)
- Sessão com timeout de 10 minutos
- Auditoria completa de 24 eventos
- `SECRET_KEY` obrigatória via variável de ambiente

---

## 🧱 Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| **Backend** | Python 3.11+ · Flask 3.0 |
| **ORM** | SQLAlchemy 2.0 + psycopg 3 |
| **Banco** | PostgreSQL 16 |
| **Frontend** | Bootstrap 5.3 · Chart.js 4.4 · Bootstrap Icons |
| **Autenticação** | Flask-Login + Flask-WTF (CSRF) |
| **Rate Limit** | Flask-Limiter |
| **Exportação** | pandas + openpyxl (Excel) |
| **PDF** | ReportLab |
| **Servidor** | Waitress (produção) |
| **Agente Windows** | .NET 8 · WPF · NotifyIcon |

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.11+
- PostgreSQL 16
- Git

### 1. Clone o repositório

```bash
git clone https://github.com/katoonnoass/sara-controle-retornos.git
cd sara-controle-retornos
```

### 2. Configure o ambiente

```bash
python -m venv venv
.\venv\Scripts\Activate    # Windows
source venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

### 3. Configure o banco PostgreSQL

Crie um banco chamado `sara` no PostgreSQL e ajuste as credenciais:

```bash
cp .env.example .env
```

Edite o `.env` com suas configurações:

```ini
APP_ENV=development
DATABASE_URL=postgresql+psycopg://postgres:SUA_SENHA@localhost:5433/sara
SECRET_KEY=python -c "import secrets; print(secrets.token_urlsafe(64))"
FLASK_DEBUG=true
```

### 4. Execute

```bash
python app.py
```

Acesse [`http://localhost:5000`](http://localhost:5000)

> 👤 Login padrão: `admin` · senha: `admin` _(altere em produção!)_

---

## 🖥️ Agente Windows (SARA Server Agent)

O SARA inclui um **agente de bandeja** desenvolvido em .NET 8 (WPF) para monitoramento do servidor:

- ▶️ **Start / Stop** — Controla o servidor Flask
- 🌐 **Open SARA** — Abre o sistema no navegador
- 🔔 **NotifyIcon** — Ícone na bandeja do Windows
- ⚙️ **Configuração** — Porta e caminho do servidor

### Build do Agente

```bash
cd SaraServerAgent
dotnet publish -c Release -r win-x64 --self-contained true -o publish
```

O executável estará em `SaraServerAgent/publish/SaraServerAgent.exe`.

---

## 📁 Estrutura do Projeto

```
📦 sara-controle-retornos
├── 📂 assets/              # Imagens e ícones do sistema
├── 📂 docs/                # Documentação e planos de homologação
├── 📂 routes/              # Blueprints Flask
│   ├── auth_routes.py      #   Autenticação
│   ├── etapas_routes.py    #   Fluxo E1–E5
│   ├── gestao_routes.py    #   Dashboard, listas, exportação
│   └── admin_routes.py     #   Administração (usuários, auditoria)
├── 📂 scripts/             # Utilitários (backup, migração)
├── 📂 SaraServerAgent/     # Agente Windows (.NET 8 WPF)
├── 📂 templates/           # Templates Jinja2
├── 📜 app.py               # Fábrica da aplicação Flask
├── 📜 config.py            # Configurações e constantes
├── 📜 models.py            # Modelos SQLAlchemy
├── 📜 utils.py             # Funções utilitárias
├── 📜 logging_config.py    # Configuração de logs
└── 📜 run.py               # Ponto de entrada
```

---

## 🔐 Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `SECRET_KEY` | ✅ | Chave para assinatura de sessão |
| `DATABASE_URL` | ✅ | URL de conexão PostgreSQL |
| `APP_ENV` | ❌ | `development`, `homologation` ou `production` |
| `FLASK_DEBUG` | ❌ | `true`/`false` (forçado `false` em produção/homologação) |
| `PORT` | ❌ | Porta do servidor (padrão: 5000) |

---

## 🧪 Homologação

O SARA passou por ciclo completo de homologação:

- ✅ Todos os fluxos E1–E5 testados (aprovação e reprovação)
- ✅ Auditoria validada (24 eventos registrados)
- ✅ Backup PostgreSQL testado (retenção de 30 dias)
- ✅ Segurança validada (CSRF, rate limiting, senhas hasheadas)
- ✅ Tema claro/escuro validado
- ✅ Responsividade testada (1366×768 e <768px)

---

## 🛡️ Licença

**© 2026 EPHAR Indústria Farmacêutica** — Todos os direitos reservados.

Este software é de uso interno da EPHAR Indústria Farmacêutica. Não é permitida a distribuição, cópia ou modificação sem autorização expressa.

---

<p align="center">
  Feito com 💙 pela equipe EPHAR
  <br>
  <sub>versão 5.4.0-WEB</sub>
</p>
