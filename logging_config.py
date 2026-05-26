"""
logging_config.py — Centralized logging configuration for SARA.
Creates daily rotating log files and integrates with Flask.
"""
import os
import logging
import logging.handlers
from flask import has_request_context, request
from flask_login import current_user


class RequestFormatter(logging.Formatter):
    """Custom formatter that includes request info (user, IP, route) when available."""

    def format(self, record):
        if has_request_context():
            record.user = current_user.is_authenticated or "-"
            if current_user.is_authenticated:
                try:
                    record.user = current_user.usuario
                except Exception:
                    record.user = "(authenticated)"
            else:
                record.user = "-"
            record.client_ip = request.remote_addr or "-"
            record.route = request.path or "-"
            record.method = request.method or "-"
        else:
            record.user = "-"
            record.client_ip = "-"
            record.route = "-"
            record.method = "-"
        return super().format(record)

    def formatTime(self, record, datefmt=None):
        return super().formatTime(record, datefmt="%d/%m/%Y %H:%M:%S")


LOG_FORMAT = "%(asctime)s [%(levelname)-5s] %(method)-4s %(route)-30s user=%(user)-16s ip=%(client_ip)-15s %(message)s"

_logging_initialized = False


def setup_logging(app) -> logging.Logger:
    """Configure logging for the SARA application.
    Creates logs/ directory and sets up file + console handlers.
    Returns the app logger.
    Safe to call multiple times (idempotent).
    """
    global _logging_initialized
    if _logging_initialized:
        app.logger.info("=== SARA Application restarted (reloader) ===")
        return app.logger
    _logging_initialized = True

    logs_dir = os.path.join(app.root_path, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log_file = os.path.join(logs_dir, "sara-app.log")

    # Remove default Flask handlers (we use root logger instead)
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)

    # File handler — daily rotation, keep 30 days
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=30,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(RequestFormatter(LOG_FORMAT))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
    console_handler.setFormatter(RequestFormatter(LOG_FORMAT))

    # Configure root logger — all modules (app, routes, utils) inherit from it
    root_logger = logging.getLogger()
    # Remove existing root handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # Disable propagation from app.logger to avoid double logging
    app.logger.propagate = True

    # Suppress Flask/Werkzeug default access logs
    logging.getLogger("werkzeug").setLevel(logging.WARNING)

    app.logger.info("=== SARA Application starting ===")
    app.logger.info("Environment: %s | Debug: %s | Log file: %s",
                    app.config.get("APP_ENV", "unknown"),
                    app.debug, log_file)

    return app.logger
