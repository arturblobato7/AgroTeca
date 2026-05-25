import logging
import os
import secrets
from functools import wraps

from flask import Flask, abort, redirect, render_template, request, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from db import buscar_usuario, criar_banco, get_db


# -------------------------
# CONSTANTS
# -------------------------

STATUS_PENDENTE = "pendente"
STATUS_APROVADO = "aprovado"
STATUS_REJEITADO = "rejeitado"
STATUS_VALIDOS = (STATUS_PENDENTE, STATUS_APROVADO, STATUS_REJEITADO)

ROLE_ADMIN = "admin"
ROLE_ALUNO = "aluno"

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "mp4", "mp3", "doc", "docx"}
MAX_UPLOAD_BYTES = 25 * 1024 * 1024  # 25 MiB

TITULO_MAX = 160
AUTOR_MAX = 120
DESCRICAO_MAX = 5000
CATEGORIA_MAX = 60
TIPO_MAX = 40


# -------------------------
# APP FACTORY
# -------------------------

def create_app():
    app = Flask(__name__)

    upload_folder = os.environ.get("AGROTECA_UPLOAD_DIR", "static/uploads")
    os.makedirs(upload_folder, exist_ok=True)
    app.config.update(
        UPLOAD_FOLDER=upload_folder,
        MAX_CONTENT_LENGTH=MAX_UPLOAD_BYTES,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("AGROTECA_COOKIE_SECURE", "0") == "1",
    )

    secret = os.environ.get("SECRET_KEY")
    if not secret:
        if os.environ.get("FLASK_ENV") == "production":
            raise RuntimeError("SECRET_KEY must be set in production")
        secret = secrets.token_hex(32)
        logging.warning("SECRET_KEY not set; using ephemeral key (sessions reset on restart).")
    app.secret_key = secret

    CSRFProtect(app)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    _register_routes(app)
    return app


# -------------------------
# AUTH HELPERS
# -------------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect("/login")
        if session.get("role") != ROLE_ADMIN:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated


# -------------------------
# INPUT HELPERS
# -------------------------

def _collect_fields(spec):
    """Validate a dict of {field_name: max_len}. Returns (values, error) where
    error is a user-facing message (or None on success)."""
    values = {}
    for name, max_len in spec.items():
        v = (request.form.get(name) or "").strip()
        if not v:
            return values, f"Preencha o campo \"{name}\"."
        if len(v) > max_len:
            return values, f"O campo \"{name}\" excede {max_len} caracteres."
        values[name] = v
    return values, None


def _safe_upload_name(original_name):
    """Return a collision-safe stored filename for an uploaded file, or None
    if the upload is empty/missing. Raises 400 on disallowed extensions."""
    if not original_name:
        return None
    if "." not in original_name:
        abort(400, "Arquivo sem extensão.")
    ext = original_name.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        abort(400, "Tipo de arquivo não permitido.")
    base = secure_filename(original_name.rsplit(".", 1)[0]) or "arquivo"
    return f"{base}-{secrets.token_hex(8)}.{ext}"


# -------------------------
# ROUTES
# -------------------------

def _register_routes(app):

    # ---- public ----

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/tecnicas")
    def tecnicas():
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM conteudos WHERE status = ? AND categoria = ?",
                (STATUS_APROVADO, "Técnica de plantio"),
            ).fetchall()
        return render_template("tecnicas.html", tecnicas=rows)

    @app.route("/videos")
    def videos():
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM conteudos WHERE status = ? AND tipo = ? ORDER BY id DESC",
                (STATUS_APROVADO, "Vídeo"),
            ).fetchall()
        return render_template("videos.html", videos=rows)

    @app.route("/cartilhas")
    def cartilhas():
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM conteudos WHERE status = ? AND categoria = ?",
                (STATUS_APROVADO, "Cartilha"),
            ).fetchall()
        return render_template("cartilhas.html", conteudos=rows)

    @app.route("/comunidade")
    def comunidade():
        return render_template("comunidade.html")

    @app.route("/conteudos")
    def conteudos():
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM conteudos WHERE status = ? ORDER BY id DESC",
                (STATUS_APROVADO,),
            ).fetchall()
        return render_template("conteudos.html", conteudos=rows)

    # ---- enviar ----

    @app.route("/enviar", methods=["GET", "POST"])
    @login_required
    def enviar():
        if request.method == "GET":
            return render_template("enviar.html")

        fields, erro = _collect_fields({
            "titulo": TITULO_MAX,
            "categoria": CATEGORIA_MAX,
            "tipo": TIPO_MAX,
            "descricao": DESCRICAO_MAX,
        })
        if erro:
            return render_template("enviar.html", erro=erro), 400
        titulo = fields["titulo"]
        categoria = fields["categoria"]
        tipo = fields["tipo"]
        descricao = fields["descricao"]
        autor = session["nome"]

        arquivo = request.files.get("arquivo")
        nome_arquivo = None
        if arquivo and arquivo.filename:
            try:
                nome_arquivo = _safe_upload_name(arquivo.filename)
            except Exception:
                return render_template("enviar.html", erro="Tipo de arquivo não permitido."), 400
            arquivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo))

        with get_db() as conn:
            conn.execute(
                """INSERT INTO conteudos
                   (titulo, descricao, categoria, tipo, autor, arquivo)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (titulo, descricao, categoria, tipo, autor, nome_arquivo),
            )

        return render_template("enviar.html", sucesso=True)

    # ---- admin ----

    @app.route("/admin")
    @admin_required
    def admin():
        aba = request.args.get("aba", STATUS_PENDENTE)
        if aba not in STATUS_VALIDOS:
            aba = STATUS_PENDENTE

        with get_db() as conn:
            counts = {
                s: conn.execute(
                    "SELECT COUNT(*) FROM conteudos WHERE status = ?", (s,)
                ).fetchone()[0]
                for s in STATUS_VALIDOS
            }
            conteudos = conn.execute(
                "SELECT * FROM conteudos WHERE status = ? ORDER BY id DESC", (aba,)
            ).fetchall()

        return render_template(
            "admin.html",
            conteudos=conteudos,
            aba=aba,
            total_pendente=counts[STATUS_PENDENTE],
            total_aprovado=counts[STATUS_APROVADO],
            total_rejeitado=counts[STATUS_REJEITADO],
        )

    def _set_status(content_id, new_status):
        with get_db() as conn:
            conn.execute(
                "UPDATE conteudos SET status = ? WHERE id = ?",
                (new_status, content_id),
            )

    @app.route("/aprovar/<int:id>", methods=["POST"])
    @admin_required
    def aprovar(id):
        _set_status(id, STATUS_APROVADO)
        return redirect("/admin")

    @app.route("/rejeitar/<int:id>", methods=["POST"])
    @admin_required
    def rejeitar(id):
        _set_status(id, STATUS_REJEITADO)
        return redirect("/admin")

    @app.route("/deletar/<int:id>", methods=["POST"])
    @admin_required
    def deletar(id):
        with get_db() as conn:
            row = conn.execute(
                "SELECT arquivo FROM conteudos WHERE id = ?", (id,)
            ).fetchone()
            if row and row["arquivo"]:
                caminho = os.path.join(app.config["UPLOAD_FOLDER"], row["arquivo"])
                # Confine deletion to the upload folder (defence in depth).
                upload_root = os.path.realpath(app.config["UPLOAD_FOLDER"])
                if os.path.realpath(caminho).startswith(upload_root + os.sep) \
                        and os.path.exists(caminho):
                    os.remove(caminho)
            conn.execute("DELETE FROM conteudos WHERE id = ?", (id,))
        return redirect("/admin")

    @app.route("/editar_conteudo/<int:id>", methods=["GET", "POST"])
    @admin_required
    def editar_conteudo(id):
        if request.method == "POST":
            fields, erro = _collect_fields({
                "titulo": TITULO_MAX,
                "categoria": CATEGORIA_MAX,
                "tipo": TIPO_MAX,
                "descricao": DESCRICAO_MAX,
                "autor": AUTOR_MAX,
            })
            if erro:
                with get_db() as conn:
                    conteudo = conn.execute(
                        "SELECT * FROM conteudos WHERE id = ?", (id,)
                    ).fetchone()
                return render_template("editar_conteudo.html", conteudo=conteudo, erro=erro), 400

            with get_db() as conn:
                conn.execute(
                    """UPDATE conteudos
                       SET titulo = ?, categoria = ?, tipo = ?, descricao = ?, autor = ?
                       WHERE id = ?""",
                    (fields["titulo"], fields["categoria"], fields["tipo"],
                     fields["descricao"], fields["autor"], id),
                )
            return redirect("/admin")

        with get_db() as conn:
            conteudo = conn.execute(
                "SELECT * FROM conteudos WHERE id = ?", (id,)
            ).fetchone()
        if not conteudo:
            abort(404)
        return render_template("editar_conteudo.html", conteudo=conteudo)

    # ---- auth ----

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if "usuario_id" in session:
            return redirect("/admin" if session.get("role") == ROLE_ADMIN else "/")

        if request.method == "POST":
            usuario = (request.form.get("usuario") or "").strip()
            senha = request.form.get("senha") or ""

            u = buscar_usuario(usuario) if usuario else None
            if u and check_password_hash(u["senha"], senha):
                session.clear()
                session["usuario_id"] = u["id"]
                session["nome"] = u["nome"]
                session["usuario"] = u["usuario"]
                session["role"] = u["role"]
                return redirect("/admin" if u["role"] == ROLE_ADMIN else "/")

            logging.info("Login falhou para usuário=%r", usuario)
            return render_template("login.html", erro="Usuário ou senha incorretos"), 401

        return render_template("login.html")

    @app.route("/registro", methods=["GET", "POST"])
    def registro():
        if "usuario_id" in session:
            return redirect("/")

        if request.method == "GET":
            return render_template("registro.html")

        nome = (request.form.get("nome") or "").strip()
        usuario = (request.form.get("usuario") or "").strip()
        senha = request.form.get("senha") or ""
        confirma = request.form.get("confirma") or ""

        if not nome or not usuario:
            return render_template("registro.html", erro="Informe nome e usuário."), 400
        if senha != confirma:
            return render_template("registro.html", erro="As senhas não coincidem."), 400
        if len(senha) < 6:
            return render_template("registro.html", erro="A senha deve ter pelo menos 6 caracteres."), 400
        if buscar_usuario(usuario):
            return render_template("registro.html", erro="Este nome de usuário já está em uso."), 409

        try:
            with get_db() as conn:
                conn.execute(
                    """INSERT INTO usuarios (nome, usuario, senha, role)
                       VALUES (?, ?, ?, ?)""",
                    (nome, usuario, generate_password_hash(senha), ROLE_ALUNO),
                )
        except Exception:
            # Almost always the UNIQUE(usuario) race; surface a friendly message
            # but log the real cause for ops.
            logging.exception("Falha ao registrar usuário=%r", usuario)
            return render_template("registro.html", erro="Erro ao criar conta. Tente outro nome de usuário."), 500

        return render_template("registro.html", sucesso=True)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/login")


app = create_app()


if __name__ == "__main__":
    criar_banco()
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    port = int(os.environ.get("PORT", "5001"))
    app.run(debug=debug, port=port)
