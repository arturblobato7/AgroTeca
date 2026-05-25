import os
import sqlite3
from contextlib import contextmanager

from werkzeug.security import generate_password_hash

DB_PATH = os.environ.get("AGROTECA_DB_PATH", "database.db")


@contextmanager
def get_db():
    """Context-managed sqlite connection. Commits on success, rolls back on
    exception, and always closes the handle."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def criar_banco():
    with get_db() as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS conteudos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                categoria TEXT NOT NULL,
                tipo TEXT,
                autor TEXT,
                arquivo TEXT,
                status TEXT NOT NULL DEFAULT 'pendente'
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_conteudos_status ON conteudos(status)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_conteudos_status_categoria ON conteudos(status, categoria)")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                nome    TEXT NOT NULL,
                usuario TEXT NOT NULL UNIQUE,
                senha   TEXT NOT NULL,
                role    TEXT NOT NULL DEFAULT 'aluno'
            )
        """)

        _seed_admin_if_configured(cur)


def _seed_admin_if_configured(cur):
    """Seed an initial admin only when explicit credentials are provided via
    environment. Avoids shipping a well-known default password."""
    admin_user = os.environ.get("AGROTECA_ADMIN_USER")
    admin_pass = os.environ.get("AGROTECA_ADMIN_PASSWORD")
    if not admin_user or not admin_pass:
        return

    cur.execute("SELECT 1 FROM usuarios WHERE role = 'admin' LIMIT 1")
    if cur.fetchone():
        return

    cur.execute(
        "INSERT INTO usuarios (nome, usuario, senha, role) VALUES (?, ?, ?, 'admin')",
        (
            os.environ.get("AGROTECA_ADMIN_NAME", "Curador"),
            admin_user,
            generate_password_hash(admin_pass),
        ),
    )


def buscar_usuario(usuario):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM usuarios WHERE usuario = ?", (usuario,)
        ).fetchone()
        return dict(row) if row else None
