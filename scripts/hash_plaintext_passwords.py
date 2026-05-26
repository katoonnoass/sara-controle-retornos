"""
scripts/hash_plaintext_passwords.py
Converts all plain-text passwords to secure hashes using Werkzeug.
Does NOT alter users, roles, permissions, retornos, or patrocinadores.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.security import generate_password_hash
from app import create_app
from models import db, Usuario

HASH_PREFIXES = ("scrypt:", "pbkdf2:")


def main():
    app = create_app()
    with app.app_context():
        usuarios = Usuario.query.order_by(Usuario.id).all()
        total = len(usuarios)
        ja_hash = 0
        convertidos = 0
        ignorados = 0
        erros = 0

        for u in usuarios:
            senha_atual = u.senha or ""
            if not senha_atual:
                ignorados += 1
                continue
            if senha_atual.startswith(HASH_PREFIXES):
                ja_hash += 1
                continue

            # Plain text — hash it
            try:
                u.senha = generate_password_hash(senha_atual)
                convertidos += 1
            except Exception as e:
                print(f"  [ERRO] Falha ao hashear usuario {u.usuario} (id={u.id}): {e}")
                erros += 1

        try:
            db.session.commit()
            print(f"\n=== RELATORIO DE CONVERSAO DE SENHAS ===")
            print(f"  Total de usuarios analisados: {total}")
            print(f"  Usuarios ja com hash:         {ja_hash}")
            print(f"  Senhas convertidas:            {convertidos}")
            print(f"  Usuarios ignorados (vazias):   {ignorados}")
            print(f"  Erros:                         {erros}")

            # Final verification
            restantes = Usuario.query.filter(
                ~Usuario.senha.startswith("scrypt:"),
                ~Usuario.senha.startswith("pbkdf2:"),
                Usuario.senha != "",
                Usuario.senha.isnot(None)
            ).count()
            # The query above might be complex, let's do it safely
            restantes = 0
            for u in Usuario.query.all():
                s = u.senha or ""
                if s and not s.startswith(HASH_PREFIXES):
                    restantes += 1
            print(f"  Senhas ainda em texto plano:   {restantes}")

            if restantes == 0:
                print("\n  RESULTADO: Todas as senhas estao hasheadas com sucesso!")
            else:
                print(f"\n  ATENCAO: {restantes} usuario(s) ainda possuem senha em texto plano.")

        except Exception as e:
            db.session.rollback()
            print(f"\n  [FATAL] Erro ao salvar: {e}")
            print("  Rollback executado. Nenhuma senha foi alterada.")
            sys.exit(1)


if __name__ == "__main__":
    main()
