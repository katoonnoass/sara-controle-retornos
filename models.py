from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(200), nullable=False)
    nome_exibicao = db.Column(db.String(100), nullable=False)
    setor = db.Column(db.String(100), nullable=False, default="")
    cargo = db.Column(db.String(100), nullable=False, default="")
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    ativo = db.Column(db.String(20), nullable=False, default="Sim")
    observacoes = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        if ":" in self.senha and (self.senha.startswith("pbkdf2") or self.senha.startswith("scrypt") or self.senha.startswith("bcrypt") or self.senha.startswith("argon2")):
            return check_password_hash(self.senha, password)
        if self.senha == password:
            self.set_password(password)
            return True
        return False

    def get_id(self):
        return str(self.id)

    @property
    def is_admin(self):
        return self.cargo in ("Administrador", "Diretor", "Diretora")

    @property
    def pode_editar(self):
        from config import Config
        return self.cargo in Config.CARGOS_EDICAO

    @property
    def pode_excluir(self):
        from config import Config
        return self.cargo in Config.CARGOS_EXCLUSAO

    @property
    def pode_produtividade(self):
        from config import Config
        return self.cargo in Config.CARGOS_PRODUTIVIDADE

    @property
    def pode_graficos(self):
        from config import Config
        return self.cargo in Config.CARGOS_GRAFICOS

    @property
    def pode_diretoria(self):
        from config import Config
        return self.cargo in Config.CARGOS_DIRETORIA


class Retorno(db.Model):
    __tablename__ = "retornos"

    id = db.Column(db.Integer, primary_key=True)
    id_retorno = db.Column(db.String(30), unique=True, nullable=False)
    ticket_atendimento = db.Column(db.String(30), unique=True, nullable=False)

    # E1 - Solicitar
    gp_recebimento_cliente = db.Column(db.String(30), default="")
    nome_pmo = db.Column(db.String(100), default="")
    numero_proposta = db.Column(db.String(50), default="")
    nome_cliente = db.Column(db.String(200), default="")
    nome_projeto = db.Column(db.String(200), default="")
    codigo_documento = db.Column(db.String(100), default="")
    tipo_retorno = db.Column(db.String(20), default="Normal")
    justificativa_prioridade = db.Column(db.String(200), default="")
    gp_ce_envio_recebimento = db.Column(db.String(30), default="")

    # E2 - Avaliar CE
    avaliador_retorno = db.Column(db.String(100), default="")
    area_responsavel = db.Column(db.String(100), default="")
    ce_ar_envio_recebimento = db.Column(db.String(30), default="")
    obs_avaliacao_ce = db.Column(db.Text, default="")

    # E3 - Executar
    status_execucao = db.Column(db.String(30), default="")
    responsavel_execucao = db.Column(db.String(100), default="")
    ar_ce_envio_recebimento = db.Column(db.String(30), default="")
    comentario_execucao = db.Column(db.Text, default="")

    # E4 - Validar CE
    aprovador_retorno = db.Column(db.String(100), default="")
    status_ce = db.Column(db.String(20), default="")
    ce_gp_envio_recebimento = db.Column(db.String(30), default="")
    comentario_validacao = db.Column(db.Text, default="")

    # E5 - Enviar
    gp_envio_cliente = db.Column(db.String(30), default="")
    obs_envio = db.Column(db.Text, default="")

    # Status geral
    status_retorno = db.Column(db.String(40), default="Aguardando Avaliação CE")

    # Exclusao logica
    status_exclusao = db.Column(db.String(20), default="-")
    responsavel_exclusao = db.Column(db.String(100), default="-")
    detalhamento_exclusao = db.Column(db.Text, default="-")
    data_exclusao = db.Column(db.String(30), default="-")

    # Prazo customizado
    prazo_execucao_customizado = db.Column(db.String(30), default="-")

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Patrocinador(db.Model):
    __tablename__ = "patrocinadores"

    id = db.Column(db.Integer, primary_key=True)
    id_patrocinador = db.Column(db.String(20), unique=True, nullable=False)
    nome_patrocinador = db.Column(db.String(200), nullable=False)
    empresa = db.Column(db.String(200), default="")
    ativo = db.Column(db.String(10), default="Sim")
    observacoes = db.Column(db.Text, default="")


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    usuario_login = db.Column(db.String(80), default="")
    usuario_nome = db.Column(db.String(200), default="")
    acao = db.Column(db.String(50), nullable=False)
    entidade = db.Column(db.String(50), default="")
    entidade_id = db.Column(db.String(50), default="")
    ticket_retorno = db.Column(db.String(30), default="")
    status_anterior = db.Column(db.String(50), default="")
    status_novo = db.Column(db.String(50), default="")
    detalhes = db.Column(db.Text, default="")
    ip = db.Column(db.String(45), default="")
    user_agent = db.Column(db.String(300), default="")


class Sessao(db.Model):
    __tablename__ = "sessoes"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), unique=True, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    usuario_login = db.Column(db.String(80), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    host = db.Column(db.String(100), default="")
    inicio = db.Column(db.String(20), default="")
    ativo = db.Column(db.Boolean, default=True)

    usuario_rel = db.relationship("Usuario", backref="sessoes")


def generate_id_retorno() -> str:
    year_suffix = datetime.now().strftime("%y")
    prefix = "IDRET"
    last = Retorno.query.filter(
        Retorno.id_retorno.like(f"{prefix}%/{year_suffix}")
    ).order_by(Retorno.id_retorno.desc()).first()
    if last:
        try:
            num = int(last.id_retorno.split("/")[0].replace(prefix, ""))
            return f"{prefix}{num + 1:05d}/{year_suffix}"
        except (ValueError, IndexError):
            pass
    return f"{prefix}00001/{year_suffix}"


def generate_id_patrocinador() -> str:
    last = Patrocinador.query.order_by(Patrocinador.id.desc()).first()
    if last:
        try:
            num = int(last.id_patrocinador.replace("PAT", ""))
            return f"PAT{num + 1:03d}"
        except ValueError:
            pass
    return "PAT001"
