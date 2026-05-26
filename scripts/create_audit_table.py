"""
scripts/create_audit_table.py
Creates the audit_logs table without destroying any existing data.
Safe to run multiple times.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, AuditLog

app = create_app()
with app.app_context():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)

    # Create table only if it doesn't exist
    tables = inspector.get_table_names()
    if "audit_logs" not in tables:
        AuditLog.__table__.create(db.engine)
        print("[OK] Tabela audit_logs criada com sucesso.")
    else:
        print("[OK] Tabela audit_logs ja existe. Nenhuma acao necessaria.")

    # Verify
    tables = inspector.get_table_names()
    if "audit_logs" in tables:
        print("[OK] Confirmado: audit_logs esta presente no banco.")
    else:
        print("[ERRO] audit_logs NAO encontrada apos criacao.")
        sys.exit(1)
