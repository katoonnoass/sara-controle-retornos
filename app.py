import logging
import sys
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, redirect, url_for, flash, request, render_template
from flask_login import LoginManager, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from models import db, Usuario
from logging_config import setup_logging

logger = logging.getLogger(__name__)

csrf = CSRFProtect()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_uri="memory://",
)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para acessar o sistema."


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)

    setup_logging(app)

    from routes.auth_routes import auth_bp
    from routes.etapas_routes import etapas_bp
    from routes.gestao_routes import gestao_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(etapas_bp)
    app.register_blueprint(gestao_bp)
    app.register_blueprint(admin_bp)

    @app.template_filter("first")
    def first_filter(s):
        return s[0] if s else ""

    @app.template_filter("date_input")
    def date_input_filter(val):
        if not val:
            return ""
        s = str(val).strip()[:10]
        if len(s) == 10 and s[2] == "/" and s[5] == "/":
            return s[6:10] + "-" + s[3:5] + "-" + s[0:2]
        return s

    @app.after_request
    def force_utf8(response):
        content_type = response.headers.get("Content-Type", "")
        if "text/html" in content_type or content_type.startswith("text/plain"):
            response.headers["Content-Type"] = content_type.split(";")[0] + "; charset=utf-8"
        return response

    @app.before_request
    def verificar_sessao():
        if request.endpoint in ("auth.login", "health", "static"):
            return
        from models import Sessao
        from datetime import datetime
        if current_user.is_authenticated:
            sess = Sessao.query.filter_by(usuario_id=current_user.id, ativo=True).first()
            if not sess and not current_user.is_admin:
                logout_user()
                flash("Sua sessão expirou. Faça login novamente.", "warning")
                return redirect(url_for("auth.login"))
            if sess:
                sess.inicio = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                try:
                    db.session.commit()
                except Exception as e:
                    logger.error("Error saving session: %s", e)
                    db.session.rollback()

    @app.context_processor
    def inject_globals():
        from config import Config as Cfg
        from datetime import datetime, date
        from models import Retorno
        from utils import classificar_prazo
        try:
            retornos = Retorno.query.filter(
                Retorno.status_exclusao != "Excluído",
                Retorno.status_retorno != "Concluído"
            ).all()
            urgencias = {"Prazo Final": 0, "Em Atraso": 0, "Próximo ao Vencimento": 0}
            for r in retornos:
                prazo = classificar_prazo(r.to_dict())
                if prazo in urgencias:
                    urgencias[prazo] += 1
        except Exception as e:
            logger.error("Error in inject_globals: %s", e)
            urgencias = {"Prazo Final": 0, "Em Atraso": 0}
        return {
            "app_name": Cfg.APP_NAME,
            "app_subtitle": Cfg.APP_SUBTITLE,
            "app_version": Cfg.APP_VERSION,
            "colors": Cfg.COLORS,
            "status_fluxo": Cfg.STATUS_FLUXO,
            "datetime": datetime,
            "urgencias": urgencias,
        }

    @app.route("/health")
    def health():
        return {"status": "ok", "app": Config.APP_NAME, "version": Config.APP_VERSION}

    @app.errorhandler(404)
    def not_found(e):
        return "Página não encontrada.", 404

    @app.errorhandler(429)
    def ratelimit_handler(e):
        logger.warning("Rate limit exceeded from IP: %s", get_remote_address())
        flash("Muitas tentativas de login. Aguarde alguns minutos e tente novamente.", "warning")
        return render_template("login.html"), 429

    @app.errorhandler(500)
    def internal_error_handler(e):
        db.session.rollback()
        logger.error("Internal server error: %s", e)
        return "Erro interno do servidor. Tente novamente.", 500

    with app.app_context():
        db.create_all()
        if not Usuario.query.first():
            admin = Usuario(
                nome_completo="Administrador",
                nome_exibicao="Admin",
                setor="TI",
                cargo="Administrador",
                usuario="admin",
                senha="",
                ativo="Sim",
                observacoes="Usuário inicial criado automaticamente",
            )
            admin.set_password("admin")
            db.session.add(admin)
            db.session.commit()
            print("[OK] Usuário admin criado com senha hasheada!")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=Config.DEBUG, host="0.0.0.0", port=5000)
