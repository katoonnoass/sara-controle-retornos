"""Shared utility functions for SARA web application."""
import logging
from datetime import datetime, date
from flask import has_request_context, request
from flask_login import current_user

logger = logging.getLogger(__name__)


PRAZO_CORES = {
    "Dentro do Prazo":       "#70AD47",
    "Próximo ao Vencimento": "#FFC000",
    "Prazo Final":           "#ED7D31",
    "Em Atraso":             "#C00000",
    "Concluído":             "#4472C4",
}

PRAZO_ORDEM = ["Em Atraso", "Prazo Final", "Próximo ao Vencimento", "Dentro do Prazo"]


def today() -> str:
    return datetime.now().strftime("%d/%m/%Y")


def parse_date(val):
    if not val or str(val).strip() in ("", "nan", "-"):
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(str(val).strip()[:10], fmt).date()
        except ValueError:
            continue
    return None


def classificar_prazo(row: dict) -> str:
    if row.get("gp_envio_cliente") and str(row.get("gp_envio_cliente", "")).strip():
        return "Concluído"
    if row.get("status_retorno") == "Concluído":
        return "Concluído"

    prazo_custom = parse_date(row.get("prazo_execucao_customizado", ""))
    if prazo_custom:
        dias = (prazo_custom - date.today()).days
        if dias < 0:
            return "Em Atraso"
        if dias == 0:
            return "Prazo Final"
        if dias == 1:
            return "Próximo ao Vencimento"
        return "Dentro do Prazo"

    entrada = parse_date(row.get("gp_ce_envio_recebimento", ""))
    if not entrada:
        entrada = parse_date(row.get("gp_recebimento_cliente", ""))
    if not entrada:
        return "Dentro do Prazo"

    dias = (date.today() - entrada).days
    if dias <= 3:
        return "Dentro do Prazo"
    if dias == 4:
        return "Próximo ao Vencimento"
    if dias == 5:
        return "Prazo Final"
    return "Em Atraso"


def prazo_envio(rec_date, env_date, prazo_customizado=None):
    """Classifica prazo de envio: compara data recebimento vs data envio."""
    if rec_date is None or env_date is None:
        return None
    if prazo_customizado is not None:
        return "Dentro do Prazo" if env_date <= prazo_customizado else "Em Atraso"
    dias = (env_date - rec_date).days
    if dias <= 3:
        return "Dentro do Prazo"
    if dias == 4:
        return "Próximo ao Vencimento"
    if dias == 5:
        return "Prazo Final"
    return "Em Atraso"


def registrar_auditoria(
        acao: str,
        entidade: str = "",
        entidade_id: str = "",
        ticket_retorno: str = "",
        status_anterior: str = "",
        status_novo: str = "",
        detalhes: str = "",
):
    """Register an audit event in the database.
    Safe to call anywhere — never raises.
    NOTE: Does NOT commit or flush — relies on the calling code's db.session.commit()
    to persist both the main operation and this audit entry atomically.
    """
    try:
        from models import db, AuditLog

        usuario_id = None
        usuario_login = ""
        usuario_nome = ""
        ip = ""
        user_agent = ""

        if has_request_context():
            ip = request.remote_addr or ""
            user_agent = str(request.headers.get("User-Agent", ""))[:300]
            if current_user.is_authenticated:
                try:
                    usuario_id = current_user.id
                    usuario_login = current_user.usuario
                    usuario_nome = current_user.nome_exibicao
                except Exception:
                    pass

        entry = AuditLog(
            usuario_id=usuario_id,
            usuario_login=usuario_login,
            usuario_nome=usuario_nome,
            acao=acao,
            entidade=entidade,
            entidade_id=entidade_id,
            ticket_retorno=ticket_retorno,
            status_anterior=status_anterior,
            status_novo=status_novo,
            detalhes=str(detalhes)[:500] if detalhes else "",
            ip=ip,
            user_agent=user_agent,
        )
        db.session.add(entry)
    except Exception as e:
        logger.error("Audit log error: %s", e)


def dias_atraso(row: dict) -> int:
    if row.get("gp_envio_cliente") and str(row.get("gp_envio_cliente", "")).strip():
        return -1
    entrada = parse_date(row.get("gp_ce_envio_recebimento", ""))
    if not entrada:
        entrada = parse_date(row.get("gp_recebimento_cliente", ""))
    if not entrada:
        return 0
    return max(0, (date.today() - entrada).days - 5)
