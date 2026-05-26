import logging
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db, Usuario, Patrocinador, Sessao, generate_id_patrocinador
from datetime import datetime

from utils import registrar_auditoria

logger = logging.getLogger(__name__)
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ─── Usuários ────────────────────────────────────────────────────────────────

@admin_bp.route("/usuarios")
@login_required
def usuarios():
    if not current_user.is_admin:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("core.dashboard"))

    usuarios = Usuario.query.order_by(Usuario.nome_exibicao).all()
    return render_template("usuarios.html", usuarios=usuarios)


@admin_bp.route("/usuarios/novo", methods=["GET", "POST"])
@login_required
def usuario_novo():
    if not current_user.is_admin:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("core.dashboard"))

    if request.method == "POST":
        data = {
            "nome_completo": request.form.get("nome_completo", "").strip(),
            "nome_exibicao": request.form.get("nome_exibicao", "").strip(),
            "setor": request.form.get("setor", "").strip(),
            "cargo": request.form.get("cargo", "").strip(),
            "usuario": request.form.get("usuario", "").strip(),
            "senha": request.form.get("senha", "").strip(),
            "ativo": request.form.get("ativo", "Sim"),
            "observacoes": request.form.get("observacoes", "").strip(),
        }

        for fld in ["nome_completo", "nome_exibicao", "cargo", "usuario", "senha"]:
            if not data[fld]:
                flash(f"Preencha '{fld}'.", "warning")
                return render_template("usuario_form.html", record=None, edit=False)

        if Usuario.query.filter_by(usuario=data["usuario"]).first():
            flash(f"Usuário '{data['usuario']}' já existe.", "danger")
            return render_template("usuario_form.html", record=None, edit=False)

        user = Usuario(**data)
        user.set_password(user.senha)
        db.session.add(user)
        registrar_auditoria(acao="criar_usuario", entidade="usuario",
                            entidade_id=data["usuario"],
                            detalhes=f"Cargo: {data['cargo']}, Setor: {data['setor']}")
        db.session.commit()
        flash("Usuário salvo com sucesso!", "success")
        return redirect(url_for("admin.usuarios"))

    return render_template("usuario_form.html", record=None, edit=False)


@admin_bp.route("/usuarios/editar/<int:uid>", methods=["GET", "POST"])
@login_required
def usuario_editar(uid):
    if not current_user.is_admin:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("core.dashboard"))

    user = Usuario.query.get_or_404(uid)

    if request.method == "POST":
        user.nome_completo = request.form.get("nome_completo", "").strip()
        user.nome_exibicao = request.form.get("nome_exibicao", "").strip()
        user.setor = request.form.get("setor", "").strip()
        user.cargo = request.form.get("cargo", "").strip()
        user.ativo = request.form.get("ativo", "Sim")
        user.observacoes = request.form.get("observacoes", "").strip()
        senha = request.form.get("senha", "").strip()
        if senha:
            user.set_password(senha)
        registrar_auditoria(acao="editar_usuario", entidade="usuario",
                            entidade_id=user.usuario,
                            detalhes=f"Cargo: {user.cargo}, Setor: {user.setor}, Ativo: {user.ativo}")
        db.session.commit()
        flash("Usuário atualizado!", "success")
        return redirect(url_for("admin.usuarios"))

    return render_template("usuario_form.html", record=user, edit=True)


@admin_bp.route("/usuarios/excluir/<int:uid>", methods=["POST"])
@login_required
def usuario_excluir(uid):
    if not current_user.is_admin:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("core.dashboard"))

    user = Usuario.query.get_or_404(uid)
    if user.id == current_user.id:
        flash("Você não pode excluir seu próprio usuário.", "danger")
        return redirect(url_for("admin.usuarios"))

    db.session.delete(user)
    registrar_auditoria(acao="excluir_usuario", entidade="usuario",
                        entidade_id=user.usuario)
    db.session.commit()
    flash(f"Usuário '{user.usuario}' removido.", "success")
    return redirect(url_for("admin.usuarios"))

    return render_template("usuario_form.html", record=None, edit=False)


# ─── Patrocinadores ──────────────────────────────────────────────────────────

@admin_bp.route("/patrocinadores")
@login_required
def patrocinadores():
    if not current_user.is_admin:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("core.dashboard"))

    pats = Patrocinador.query.order_by(Patrocinador.nome_patrocinador).all()
    return render_template("patrocinadores.html", pats=pats)


@admin_bp.route("/patrocinadores/novo", methods=["GET", "POST"])
@login_required
def patrocinador_novo():
    if not current_user.is_admin:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("core.dashboard"))

    if request.method == "POST":
        nome = request.form.get("nome_patrocinador", "").strip()
        if not nome:
            flash("Informe o nome do patrocinador.", "warning")
            return render_template("patrocinador_form.html", record=None, edit=False)

        pat = Patrocinador(
            id_patrocinador=generate_id_patrocinador(),
            nome_patrocinador=nome,
            empresa=request.form.get("empresa", "").strip(),
            ativo=request.form.get("ativo", "Sim"),
            observacoes=request.form.get("observacoes", "").strip(),
        )
        registrar_auditoria(acao="criar_patrocinador", entidade="patrocinador",
                            entidade_id=pat.id_patrocinador,
                            detalhes=f"Nome: {pat.nome_patrocinador}")
        db.session.add(pat)
        db.session.commit()
        flash("Patrocinador salvo!", "success")
        return redirect(url_for("admin.patrocinadores"))

    return render_template("patrocinador_form.html", record=None, edit=False)


@admin_bp.route("/patrocinadores/editar/<int:pid>", methods=["GET", "POST"])
@login_required
def patrocinador_editar(pid):
    if not current_user.is_admin:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("core.dashboard"))

    pat = Patrocinador.query.get_or_404(pid)

    if request.method == "POST":
        nome = request.form.get("nome_patrocinador", "").strip()
        if not nome:
            flash("Informe o nome do patrocinador.", "warning")
            return render_template("patrocinador_form.html", record=pat, edit=True)

        pat.nome_patrocinador = nome
        pat.empresa = request.form.get("empresa", "").strip()
        pat.ativo = request.form.get("ativo", "Sim")
        pat.observacoes = request.form.get("observacoes", "").strip()
        registrar_auditoria(acao="editar_patrocinador", entidade="patrocinador",
                            entidade_id=pat.id_patrocinador,
                            detalhes=f"Nome: {pat.nome_patrocinador}, Ativo: {pat.ativo}")
        db.session.commit()
        flash("Patrocinador atualizado!", "success")
        return redirect(url_for("admin.patrocinadores"))

    return render_template("patrocinador_form.html", record=pat, edit=True)


@admin_bp.route("/patrocinadores/excluir/<int:pid>", methods=["POST"])
@login_required
def patrocinador_excluir(pid):
    if not current_user.is_admin:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("core.dashboard"))

    pat = Patrocinador.query.get_or_404(pid)
    db.session.delete(pat)
    registrar_auditoria(acao="excluir_patrocinador", entidade="patrocinador",
                        entidade_id=pat.id_patrocinador,
                        detalhes=f"Nome: {pat.nome_patrocinador}")
    db.session.commit()
    flash(f"Patrocinador '{pat.nome_patrocinador}' removido.", "success")
    return redirect(url_for("admin.patrocinadores"))


@admin_bp.route("/auditoria")
@login_required
def auditoria():
    if not current_user.is_admin:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("core.dashboard"))

    page = request.args.get("page", 1, type=int)
    per_page = 50

    from models import AuditLog

    q = AuditLog.query.order_by(AuditLog.id.desc())

    usuario_f = request.args.get("usuario", "").strip()
    acao_f = request.args.get("acao", "").strip()
    ticket_f = request.args.get("ticket", "").strip()
    data_ini = request.args.get("data_ini", "").strip()
    data_fim = request.args.get("data_fim", "").strip()

    if usuario_f:
        q = q.filter(AuditLog.usuario_login.ilike(f"%{usuario_f}%"))
    if acao_f:
        q = q.filter(AuditLog.acao == acao_f)
    if ticket_f:
        q = q.filter(AuditLog.ticket_retorno.ilike(f"%{ticket_f}%"))
    if data_ini:
        try:
            from datetime import datetime as dt
            d = dt.strptime(data_ini, "%Y-%m-%d")
            q = q.filter(AuditLog.created_at >= d)
        except ValueError:
            pass
    if data_fim:
        try:
            from datetime import datetime as dt, timedelta
            d = dt.strptime(data_fim, "%Y-%m-%d") + timedelta(days=1)
            q = q.filter(AuditLog.created_at < d)
        except ValueError:
            pass

    pagination = q.paginate(page=page, per_page=per_page, error_out=False)
    registros = pagination.items
    total = pagination.total
    total_pages = pagination.pages

    # Distinct acoes for filter dropdown
    acoes = [r[0] for r in AuditLog.query.with_entities(AuditLog.acao).distinct().order_by(AuditLog.acao).all()]

    return render_template("auditoria.html", registros=registros,
                           total=total, page=page, total_pages=total_pages,
                           usuario_f=usuario_f, acao_f=acao_f,
                           ticket_f=ticket_f, data_ini=data_ini, data_fim=data_fim,
                           acoes=acoes)


@admin_bp.route("/status-sessoes")
@login_required
def status_sessoes():
    if not current_user.is_admin:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("core.dashboard"))

    from datetime import timedelta
    limite = datetime.now() - timedelta(minutes=10)
    sessoes_db = Sessao.query.filter_by(ativo=True).all()
    for s in sessoes_db:
        try:
            ultima = datetime.strptime(s.inicio, "%d/%m/%Y %H:%M:%S") if s.inicio else None
            if ultima and ultima < limite:
                s.ativo = False
        except (ValueError, TypeError):
            s.ativo = False
    db.session.commit()

    sessoes = Sessao.query.filter_by(ativo=True).order_by(Sessao.inicio.desc()).all()
    return render_template("status_sessoes.html", sessoes=sessoes)


@admin_bp.route("/sessoes/forcar-logoff/<int:sid>", methods=["POST"])
@login_required
def forcar_logoff(sid):
    if not current_user.is_admin:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("core.dashboard"))

    sess = Sessao.query.get_or_404(sid)
    sess.ativo = False
    registrar_auditoria(acao="forcar_logoff", entidade="sessao",
                        entidade_id=str(sid),
                        detalhes=f"Usuario: {sess.usuario_login}, Nome: {sess.nome}")
    db.session.commit()
    flash(f"Sessão de '{sess.nome}' encerrada.", "success")
    return redirect(url_for("admin.status_sessoes"))


@admin_bp.route("/sessoes/forcar-logoff-todos", methods=["POST"])
@login_required
def forcar_logoff_todos():
    if not current_user.is_admin:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("core.dashboard"))

    Sessao.query.filter(
        Sessao.ativo == True,
        Sessao.usuario_id != current_user.id
    ).update({"ativo": False})
    registrar_auditoria(acao="forcar_logoff_todos", entidade="sistema",
                        detalhes="Todas as outras sessoes foram encerradas")
    db.session.commit()
    flash("Todas as outras sessões foram encerradas.", "success")
    return redirect(url_for("admin.status_sessoes"))


# ─── Bloqueio de Login ───────────────────────────────────────────────────────

@admin_bp.route("/bloquear-login", methods=["POST"])
@login_required
def bloquear_login():
    if not current_user.is_admin:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("core.dashboard"))

    motivo = request.form.get("motivo", "Manutenção").strip()
    usuarios = Usuario.query.filter(
        Usuario.cargo.notin_(["Administrador", "Diretor", "Diretora"]),
        Usuario.ativo == "Sim"
    ).all()
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    for u in usuarios:
        u.ativo = "Bloqueado"
        obs = u.observacoes or ""
        u.observacoes = f"[BLOQ {timestamp}] {motivo}" + (f" | {obs}" if obs.strip() else "")
    registrar_auditoria(acao="bloquear_login_global", entidade="sistema",
                        detalhes=f"Motivo: {motivo}, Usuarios: {len(usuarios)}")
    db.session.commit()
    flash(f"Login bloqueado para {len(usuarios)} usuários.", "success")
    return redirect(url_for("admin.status_sessoes"))


@admin_bp.route("/desbloquear-login", methods=["POST"])
@login_required
def desbloquear_login():
    if not current_user.is_admin:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("core.dashboard"))

    usuarios = Usuario.query.filter_by(ativo="Bloqueado").all()
    for u in usuarios:
        u.ativo = "Sim"
        obs = u.observacoes or ""
        u.observacoes = " | ".join(
            p for p in obs.split(" | ") if not p.startswith("[BLOQ ")
        ).strip(" | ")
    registrar_auditoria(acao="desbloquear_login_global", entidade="sistema",
                        detalhes=f"Usuarios desbloqueados: {len(usuarios)}")
    db.session.commit()
    flash(f"{len(usuarios)} usuário(s) desbloqueado(s).", "success")
    return redirect(url_for("admin.status_sessoes"))


@admin_bp.route("/bloquear-usuario/<int:uid>", methods=["POST"])
@login_required
def bloquear_usuario(uid):
    if not current_user.is_admin:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("core.dashboard"))

    user = Usuario.query.get_or_404(uid)
    user.ativo = "Bloqueado"
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    obs = user.observacoes or ""
    user.observacoes = f"[BLOQ {timestamp}] Bloqueado pelo administrador" + (f" | {obs}" if obs.strip() else "")
    registrar_auditoria(acao="bloquear_usuario", entidade="usuario",
                        entidade_id=user.usuario)
    db.session.commit()
    flash(f"Usuário '{user.usuario}' bloqueado.", "success")
    return redirect(url_for("admin.status_sessoes"))


@admin_bp.route("/desbloquear-usuario/<int:uid>", methods=["POST"])
@login_required
def desbloquear_usuario(uid):
    if not current_user.is_admin:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("core.dashboard"))

    user = Usuario.query.get_or_404(uid)
    user.ativo = "Sim"
    obs = user.observacoes or ""
    user.observacoes = " | ".join(
        p for p in obs.split(" | ") if not p.startswith("[BLOQ ")
    ).strip(" | ")
    registrar_auditoria(acao="desbloquear_usuario", entidade="usuario",
                        entidade_id=user.usuario)
    db.session.commit()
    flash(f"Usuário '{user.usuario}' desbloqueado.", "success")
    return redirect(url_for("admin.status_sessoes"))
