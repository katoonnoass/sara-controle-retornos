import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable is required. Set it in .env or environment.")
    APP_ENV = os.environ.get("APP_ENV", "development")
    DEBUG = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    if APP_ENV in ("production", "homologation"):
        DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:Ephar%402026PG@localhost:5433/sara"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_NAME = "sara_session"
    PERMANENT_SESSION_LIFETIME = 600  # 10 minutes idle timeout

    # Tema / identidade visual (espelhado do config.py original)
    APP_NAME = "SARA"
    APP_SUBTITLE = "Acompanhamento de Retornos"
    APP_VERSION = "5.4.0-WEB"

    COLORS = {
        "primary": "#4472C4",
        "primary_light": "#5B9BD5",
        "accent": "#ED7D31",
        "dark": "#44546A",
        "success": "#70AD47",
        "warning": "#FFC000",
        "danger": "#C00000",
        "bg": "#F2F4F8",
        "bg_card": "#FFFFFF",
        "text": "#1E2D40",
        "text_muted": "#6B7A8D",
        "border": "#D0D8E8",
        "sidebar": "#1E2D40",
        "sidebar_hover": "#2E3D50",
        "sidebar_active": "#4472C4",
    }

    STATUS_FLUXO = [
        "Aguardando Avaliação CE",
        "Aguardando Execução",
        "Aguardando Validação CE",
        "Aguardando Envio Projetos",
        "Concluído",
    ]

    SETORES_EXECUTORES = [
        "LABORATÓRIO FÍSICO QUÍMICO",
        "LABORATÓRIO MICROBIOLÓGICO",
        "COORDENAÇÃO DE ESTUDOS",
        "PESQUISA E DESENVOLVIMENTO",
        "DESENVOLVIMENTO ANALÍTICO",
    ]

    CARGOS_EXCLUSAO = [
        "Administrador", "Gerente", "Supervisor", "Supervisora",
        "Coordenador", "Coordenadora", "Diretor", "Diretora",
    ]

    CARGOS_EDICAO = [
        "Administrador", "Diretor", "Gerente",
        "Coordenador", "Coordenadora", "Supervisor",
    ]

    CARGOS_PRODUTIVIDADE = [
        "Administrador", "Diretor", "Diretora", "Gerente",
        "Coordenador", "Coordenadora", "Supervisor", "Supervisora",
    ]

    CARGOS_GRAFICOS = [
        "Administrador", "Diretor", "Diretora", "Gerente",
        "Coordenador", "Coordenadora", "Supervisor", "Supervisora",
    ]

    CARGOS_DIRETORIA = [
        "Diretor", "Diretora", "Administrador",
        "Gerente", "Coordenador", "Coordenadora", "Supervisor", "Supervisora",
    ]

    COL_LABELS = {
        "ID_Retorno": "ID",
        "ticket_atendimento": "Ticket",
        "gp_recebimento_cliente": "Data Receb. GP",
        "nome_pmo": "PMO",
        "numero_proposta": "Nº Proposta",
        "nome_cliente": "Cliente / Patrocinador",
        "nome_projeto": "Projeto",
        "codigo_documento": "Código Documento",
        "tipo_retorno": "Tipo / Prioridade",
        "justificativa_prioridade": "Justificativa",
        "gp_ce_envio_recebimento": "Data Envio GP → CE",
        "avaliador_retorno": "Avaliador (CE)",
        "area_responsavel": "Área Responsável",
        "ce_ar_envio_recebimento": "Data Envio CE → AR",
        "obs_avaliacao_ce": "Pendências / Obs. Avaliação CE",
        "status_execucao": "Status Execução",
        "responsavel_execucao": "Responsável Execução",
        "ar_ce_envio_recebimento": "Data Envio AR → CE",
        "comentario_execucao": "Comentário da Execução",
        "aprovador_retorno": "Aprovador CE",
        "status_ce": "Status CE (Validação)",
        "ce_gp_envio_recebimento": "Data Envio CE → GP",
        "comentario_validacao": "Comentário da Validação",
        "gp_envio_cliente": "Data Envio GP → Cliente",
        "obs_envio": "Observações do Envio",
        "status_retorno": "Status Geral",
        "status_exclusao": "Status Exclusão",
        "responsavel_exclusao": "Responsável Exclusão",
        "detalhamento_exclusao": "Detalhamento Exclusão",
        "data_exclusao": "Data Exclusão",
        "prazo_execucao_customizado": "Prazo Customizado de Execução",
    }
