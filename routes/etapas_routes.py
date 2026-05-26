import logging
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Retorno, generate_id_retorno, Usuario
from datetime import datetime
from utils import today, registrar_auditoria

logger = logging.getLogger(__name__)
etapas_bp = Blueprint("etapas", __name__, url_prefix="/etapas")


def _get_tickets_por_status(status: str):
    q = Retorno.query.filter_by(status_retorno=status)
    q = q.filter(Retorno.status_exclusao != "Excluído")
    return [r.ticket_atendimento for r in q.order_by(Retorno.id.desc()).all()]


def _get_pmo_ativos():
    users = Usuario.query.filter(
        Usuario.setor.ilike("%gestão de projetos%"),
        Usuario.ativo == "Sim"
    ).all()
    if not users:
        users = Usuario.query.filter_by(ativo="Sim").all()
    return sorted(set(u.nome_exibicao for u in users if u.nome_exibicao)) or ["PMO"]


def _get_pessoas_por_setor(keyword: str):
    kw = keyword.lower()
    users = Usuario.query.filter(
        Usuario.setor.ilike(f"%{kw}%"),
        Usuario.ativo == "Sim"
    ).all()
    return sorted(set(u.nome_exibicao for u in users if u.nome_exibicao))


def _get_pessoas_por_setores(keywords: list):
    from sqlalchemy import or_
    filters = [Usuario.setor.ilike(f"%{kw}%") for kw in keywords]
    users = Usuario.query.filter(
        or_(*filters),
        Usuario.ativo == "Sim"
    ).all()
    return sorted(set(u.nome_exibicao for u in users if u.nome_exibicao))


def _get_responsaveis_ativos():
    users = Usuario.query.filter_by(ativo="Sim").all()
    return sorted(set(u.nome_exibicao for u in users if u.nome_exibicao))


def _get_patrocinadores_ativos():
    from models import Patrocinador
    pats = Patrocinador.query.filter_by(ativo="Sim").all()
    return sorted(set(p.nome_patrocinador for p in pats if p.nome_patrocinador))


# ─── E1: Solicitar ───────────────────────────────────────────────────────────

@etapas_bp.route("/solicitar", methods=["GET", "POST"])
@login_required
def solicitar():

    from config import Config

    if request.method == "POST":
        codigos = request.form.getlist("codigo_documento[]")
        if not codigos:
            flash("Adicione pelo menos um Código de Documento.", "warning")
            return redirect(url_for("etapas.solicitar"))

        data_receb = request.form.get("gp_recebimento_cliente", "").strip()
        if not data_receb:
            flash("Selecione a Data de Recebimento.", "warning")
            return redirect(url_for("etapas.solicitar"))

        pmo = request.form.get("nome_pmo", "").strip()
        if not pmo:
            flash("Selecione o PMO responsável.", "warning")
            return redirect(url_for("etapas.solicitar"))

        is_prio = request.form.get("tipo_retorno") == "Sim"
        justif = request.form.get("justificativa_prioridade", "").strip()
        if is_prio and not justif:
            flash("Informe a justificativa para prioridade.", "warning")
            return redirect(url_for("etapas.solicitar"))

        tipo = "Prioritário" if is_prio else "Normal"

        ids_gerados = []
        for codigo in codigos:
            if not codigo.strip():
                continue
            new_id = generate_id_retorno()
            ret = Retorno(
                id_retorno=new_id,
                ticket_atendimento=new_id,
                gp_recebimento_cliente=data_receb,
                nome_pmo=pmo,
                numero_proposta=request.form.get("numero_proposta", "").strip(),
                nome_cliente=request.form.get("nome_cliente", "").strip(),
                nome_projeto=request.form.get("nome_projeto", "").strip(),
                codigo_documento=codigo.strip(),
                tipo_retorno=tipo,
                justificativa_prioridade=justif,
                gp_ce_envio_recebimento=today(),
                status_retorno=Config.STATUS_FLUXO[0],
                status_exclusao="-",
                responsavel_exclusao="-",
                detalhamento_exclusao="-",
                data_exclusao="-",
                prazo_execucao_customizado="-",
            )
            db.session.add(ret)
            ids_gerados.append(f"{new_id} — Cód: {codigo.strip()}")

        try:
            for tid in ids_gerados:
                registrar_auditoria(acao="e1_criar", entidade="retorno",
                                    entidade_id=tid.split(" — ")[0].strip(),
                                    ticket_retorno=tid.split(" — ")[0].strip(),
                                    status_novo="Aguardando Avaliação CE",
                                    detalhes=tid)
            db.session.commit()
            logger.info("E1 created: %d retorno(s) by user=%s", len(ids_gerados), current_user.usuario)
            flash(f"{len(ids_gerados)} retorno(s) cadastrado(s):<br>" + "<br>".join(ids_gerados), "success")
        except Exception as e:
            db.session.rollback()
            logger.error("E1 create error: %s", e)
            flash(f"Erro ao cadastrar: {e}", "danger")
        return redirect(url_for("core.lista"))

    pmos = _get_pmo_ativos()
    patrocinadores = _get_patrocinadores_ativos()
    return render_template("solicitar.html", pmos=pmos, patrocinadores=patrocinadores)


# ─── E2: Avaliar ─────────────────────────────────────────────────────────────

@etapas_bp.route("/avaliar", methods=["GET", "POST"])
@login_required
def avaliar():
    from config import Config
    tickets = _get_tickets_por_status(Config.STATUS_FLUXO[0])

    if request.method == "POST":
        ticket = request.form.get("ticket", "").strip()
        if not ticket:
            flash("Selecione um ticket.", "warning")
            return redirect(url_for("etapas.avaliar"))

        area = request.form.get("area_responsavel", "").strip()
        avaliador = request.form.get("avaliador_retorno", "").strip()
        if not area:
            flash("Selecione a Área Responsável.", "warning")
            return redirect(url_for("etapas.avaliar"))
        if not avaliador:
            flash("Selecione o Avaliador.", "warning")
            return redirect(url_for("etapas.avaliar"))

        ret = Retorno.query.filter_by(ticket_atendimento=ticket).first()
        if not ret:
            flash("Ticket não encontrado.", "danger")
            return redirect(url_for("etapas.avaliar"))

        ret.avaliador_retorno = avaliador
        ret.area_responsavel = area
        ret.ce_ar_envio_recebimento = today()
        ret.obs_avaliacao_ce = request.form.get("obs_avaliacao_ce", "").strip() or "-"
        ret.status_retorno = Config.STATUS_FLUXO[1]
        try:
            registrar_auditoria(acao="e2_avaliar", entidade="retorno", ticket_retorno=ticket,
                                status_anterior="Aguardando Avaliação CE",
                                status_novo="Aguardando Execução",
                                detalhes=f"Area: {area}, Avaliador: {avaliador}")
            db.session.commit()
            logger.info("E2 avaliar: ticket=%s area=%s user=%s", ticket, area, current_user.usuario)
            flash(f"Ticket {ticket} direcionado para {area}.", "success")
        except Exception as e:
            db.session.rollback()
            logger.error("E2 avaliar error: ticket=%s error=%s", ticket, e)
            flash(f"Erro ao salvar avaliação: {e}", "danger")
        return redirect(url_for("core.lista"))

    record = None
    ticket_sel = request.args.get("ticket", "")
    if ticket_sel:
        record = Retorno.query.filter_by(ticket_atendimento=ticket_sel).first()

    pessoas_ce = _get_pessoas_por_setor("coordenação de estudos") or _get_responsaveis_ativos()
    return render_template("avaliar.html", tickets=tickets, ticket_sel=ticket_sel,
                           record=record, setores=Config.SETORES_EXECUTORES,
                           pessoas_ce=pessoas_ce)


# ─── E3: Executar ────────────────────────────────────────────────────────────

@etapas_bp.route("/executar", methods=["GET", "POST"])
@login_required
def executar():

    from config import Config
    tickets = _get_tickets_por_status(Config.STATUS_FLUXO[1])

    if request.method == "POST":
        ticket = request.form.get("ticket", "").strip()
        if not ticket:
            flash("Selecione um ticket.", "warning")
            return redirect(url_for("etapas.executar"))

        responsavel = request.form.get("responsavel_execucao", "").strip()
        if not responsavel:
            flash("Selecione o responsável pela execução.", "warning")
            return redirect(url_for("etapas.executar"))

        ret = Retorno.query.filter_by(ticket_atendimento=ticket).first()
        if not ret:
            flash("Ticket não encontrado.", "danger")
            return redirect(url_for("etapas.executar"))

        status_exec = request.form.get("status_execucao", "").strip()
        novo_coment = request.form.get("comentario_execucao", "").strip()
        existente = (ret.comentario_execucao or "").strip()
        if existente in ("-", ""):
            existente = ""

        if novo_coment and existente:
            ts = datetime.now().strftime("%d/%m %H:%M")
            comentario_final = f"{existente} | [{ts}] {novo_coment}"
        elif novo_coment:
            comentario_final = novo_coment
        else:
            comentario_final = existente or "-"

        ret.responsavel_execucao = responsavel
        ret.status_execucao = status_exec
        ret.ar_ce_envio_recebimento = today()
        ret.comentario_execucao = comentario_final
        ret.status_retorno = Config.STATUS_FLUXO[2]
        try:
            registrar_auditoria(acao="e3_executar", entidade="retorno", ticket_retorno=ticket,
                                status_anterior="Aguardando Execução",
                                status_novo="Aguardando Validação CE",
                                detalhes=f"Status: {status_exec}, Responsavel: {responsavel}")
            db.session.commit()
            logger.info("E3 executar: ticket=%s status=%s resp=%s user=%s", ticket, status_exec, responsavel, current_user.usuario)
            flash(f"Ticket {ticket} registrado como executado.", "success")
        except Exception as e:
            db.session.rollback()
            logger.error("E3 executar error: ticket=%s error=%s", ticket, e)
            flash(f"Erro ao salvar execução: {e}", "danger")
        return redirect(url_for("core.lista"))

    record = None
    ticket_sel = request.args.get("ticket", "")
    if ticket_sel:
        record = Retorno.query.filter_by(ticket_atendimento=ticket_sel).first()

    setor_usuario = (current_user.setor or "").strip()
    setores_exec_kw = [
        "laboratório físico químico", "laboratório microbiológico",
        "pesquisa e desenvolvimento", "desenvolvimento analítico",
        "coordenação de estudos",
    ]
    setor_lower = setor_usuario.lower()
    eh_setor_exec = any(kw in setor_lower for kw in setores_exec_kw)
    if eh_setor_exec:
        exec_pessoas = _get_pessoas_por_setor(setor_usuario) or _get_responsaveis_ativos()
    else:
        exec_pessoas = _get_pessoas_por_setores(setores_exec_kw) or _get_responsaveis_ativos()

    return render_template("executar.html", tickets=tickets, ticket_sel=ticket_sel,
                           record=record, exec_pessoas=exec_pessoas,
                           status_execucao=Config.STATUS_EXECUCAO if hasattr(Config, 'STATUS_EXECUCAO') else ["Pendente", "Em andamento", "Concluído"])


# ─── E4: Validar ─────────────────────────────────────────────────────────────

@etapas_bp.route("/validar", methods=["GET", "POST"])
@login_required
def validar():

    from config import Config
    tickets = _get_tickets_por_status(Config.STATUS_FLUXO[2])

    if request.method == "POST":
        ticket = request.form.get("ticket", "").strip()
        if not ticket:
            flash("Selecione um ticket.", "warning")
            return redirect(url_for("etapas.validar"))

        aprovador = request.form.get("aprovador_retorno", "").strip()
        status_ce = request.form.get("status_ce", "").strip()
        if not aprovador:
            flash("Selecione o Aprovador CE.", "warning")
            return redirect(url_for("etapas.validar"))
        if not status_ce:
            flash("Selecione o Status da Validação.", "warning")
            return redirect(url_for("etapas.validar"))

        ret = Retorno.query.filter_by(ticket_atendimento=ticket).first()
        if not ret:
            flash("Ticket não encontrado.", "danger")
            return redirect(url_for("etapas.validar"))

        novo_coment = request.form.get("comentario_validacao", "").strip()
        existente = (ret.comentario_validacao or "").strip()
        if existente in ("-", ""):
            existente = ""

        if novo_coment and existente:
            ts = datetime.now().strftime("%d/%m %H:%M")
            comentario_final = f"{existente} | [{ts}] {novo_coment}"
        elif novo_coment:
            comentario_final = novo_coment
        else:
            comentario_final = existente or "-"

        ret.aprovador_retorno = aprovador
        ret.status_ce = status_ce
        ret.ce_gp_envio_recebimento = today()
        ret.comentario_validacao = comentario_final
        if status_ce == "Reprovado":
            ret.status_retorno = Config.STATUS_FLUXO[1]
            ret.status_execucao = "Pendente"
        else:
            ret.status_retorno = Config.STATUS_FLUXO[3]
        try:
            novo_status = "Aguardando Execução" if status_ce == "Reprovado" else "Aguardando Envio Projetos"
            registrar_auditoria(acao="e4_validar", entidade="retorno", ticket_retorno=ticket,
                                status_anterior="Aguardando Validação CE",
                                status_novo=novo_status,
                                detalhes=f"Status CE: {status_ce}, Aprovador: {aprovador}")
            db.session.commit()
            action = "reprovado" if status_ce == "Reprovado" else "aprovado"
            logger.info("E4 validar: ticket=%s status_ce=%s user=%s", ticket, status_ce, current_user.usuario)
            msg = f"Ticket {ticket} reprovado. Voltou para Execução." if status_ce == "Reprovado" else f"Ticket {ticket} aprovado!"
            flash(msg, "success")
        except Exception as e:
            db.session.rollback()
            logger.error("E4 validar error: ticket=%s error=%s", ticket, e)
            flash(f"Erro ao salvar validação: {e}", "danger")
        return redirect(url_for("core.lista"))

    record = None
    ticket_sel = request.args.get("ticket", "")
    if ticket_sel:
        record = Retorno.query.filter_by(ticket_atendimento=ticket_sel).first()

    pessoas_ce = _get_pessoas_por_setor("coordenação de estudos") or _get_responsaveis_ativos()
    return render_template("validar.html", tickets=tickets, ticket_sel=ticket_sel,
                           record=record, pessoas_ce=pessoas_ce)


# ─── E5: Enviar ──────────────────────────────────────────────────────────────

@etapas_bp.route("/enviar", methods=["GET", "POST"])
@login_required
def enviar():

    from config import Config
    tickets = _get_tickets_por_status(Config.STATUS_FLUXO[3])

    if request.method == "POST":
        ticket = request.form.get("ticket", "").strip()
        if not ticket:
            flash("Selecione um ticket.", "warning")
            return redirect(url_for("etapas.enviar"))

        responsavel = request.form.get("responsavel_envio", "").strip()
        if not responsavel:
            flash("Selecione o responsável pelo envio.", "warning")
            return redirect(url_for("etapas.enviar"))

        data_envio = request.form.get("gp_envio_cliente", "").strip()
        if not data_envio:
            flash("Selecione a data de envio.", "warning")
            return redirect(url_for("etapas.enviar"))

        ret = Retorno.query.filter_by(ticket_atendimento=ticket).first()
        if not ret:
            flash("Ticket não encontrado.", "danger")
            return redirect(url_for("etapas.enviar"))

        ret.gp_envio_cliente = data_envio
        ret.obs_envio = request.form.get("obs_envio", "").strip() or "-"
        ret.status_retorno = Config.STATUS_FLUXO[4]
        try:
            registrar_auditoria(acao="e5_enviar", entidade="retorno", ticket_retorno=ticket,
                                status_anterior="Aguardando Envio Projetos",
                                status_novo="Concluído",
                                detalhes=f"Data envio: {data_envio}")
            db.session.commit()
            logger.info("E5 enviar: ticket=%s data_envio=%s user=%s", ticket, data_envio, current_user.usuario)
            flash(f"Ticket {ticket} concluído! Data de envio: {data_envio}", "success")
        except Exception as e:
            db.session.rollback()
            logger.error("E5 enviar error: ticket=%s error=%s", ticket, e)
            flash(f"Erro ao salvar envio: {e}", "danger")
        return redirect(url_for("core.lista"))

    record = None
    ticket_sel = request.args.get("ticket", "")
    if ticket_sel:
        record = Retorno.query.filter_by(ticket_atendimento=ticket_sel).first()

    pmo_pessoas = _get_pmo_ativos() or _get_responsaveis_ativos()
    return render_template("enviar.html", tickets=tickets, ticket_sel=ticket_sel,
                           record=record, pmo_pessoas=pmo_pessoas)
