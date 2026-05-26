import uuid
import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Usuario, Sessao
from datetime import datetime
import socket
from app import limiter
from utils import registrar_auditoria

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute;20 per hour", methods=["POST"], error_message="Muitas tentativas de login. Aguarde alguns minutos e tente novamente.")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("core.dashboard"))

    if request.method == "POST":
        username = request.form.get("usuario", "").strip()
        password = request.form.get("senha", "").strip()

        user = Usuario.query.filter_by(usuario=username).first()

        if not user:
            logger.warning("Login failed: user not found [%s]", username)
            flash("Usuário ou senha incorretos.", "danger")
            return render_template("login.html")

        if user.ativo.lower() == "bloqueado":
            motivo = ""
            if "[BLOQ" in (user.observacoes or ""):
                for parte in user.observacoes.split(" | "):
                    if parte.startswith("[BLOQ"):
                        motivo = parte
                        break
            logger.warning("Login blocked: user=%s motivo=%s", username, motivo or "bloqueado")
            flash(f"Acesso temporariamente bloqueado. {motivo}", "danger")
            return render_template("login.html")

        if user.ativo.lower() == "não":
            logger.warning("Login inactive: user=%s", username)
            flash("Usuário inativo. Contate o administrador.", "danger")
            return render_template("login.html")

        if not user.check_password(password):
            logger.warning("Login failed: wrong password [%s]", username)
            flash("Usuário ou senha incorretos.", "danger")
            return render_template("login.html")

        if user.ativo.lower() != "sim":
            logger.warning("Login denied: user=%s ativo=%s", username, user.ativo)
            flash("Acesso negado.", "danger")
            return render_template("login.html")

        logger.info("Login success: user=%s cargo=%s", user.usuario, user.cargo)
        registrar_auditoria(acao="login", entidade="usuario", entidade_id=user.usuario,
                            detalhes=f"Cargo: {user.cargo}")
        login_user(user)
        session.permanent = True
        try:
            db.session.commit()
        except Exception as e:
            logger.error("Login commit error: %s", e)
            db.session.rollback()

        # Register session - marca sessões anteriores como inativas
        Sessao.query.filter_by(usuario_id=user.id, ativo=True).update({"ativo": False})
        sess = Sessao(
            session_id=str(uuid.uuid4()),
            usuario_id=user.id,
            usuario_login=user.usuario,
            nome=user.nome_exibicao,
            host=socket.gethostname(),
            inicio=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            ativo=True,
        )
        db.session.add(sess)
        try:
            db.session.commit()
        except Exception as e:
            logger.error("Login commit error: %s", e)
            db.session.rollback()

        return redirect(url_for("core.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    try:
        usuario = current_user.usuario
        Sessao.query.filter_by(usuario_id=current_user.id, ativo=True).delete()
        db.session.commit()
    except Exception as e:
        logger.error("Logout error: %s", e)
        db.session.rollback()
    logout_user()
    logger.info("Logout: user=%s", usuario)
    registrar_auditoria(acao="logout", entidade="usuario", entidade_id=usuario)
    try:
        db.session.commit()
    except Exception as e:
        logger.error("Logout audit commit error: %s", e)
        db.session.rollback()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("auth.login"))
