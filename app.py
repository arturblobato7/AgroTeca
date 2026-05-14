from flask import Flask, render_template, request, redirect, session
from db import conectar_banco, criar_banco

app = Flask(__name__)

app.secret_key = "chave_secreta_biblioteca_jutaiteua"


# -------------------------
# CONEXÃO COM BANCO
# -------------------------


# -------------------------
# ROTAS
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/precos")
def precos():
    return render_template("precos.html")


@app.route("/tecnicas")
def tecnicas():

    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""

    SELECT * FROM conteudos

    WHERE status = 'aprovado'
    AND categoria = 'Técnica de plantio'

    """)

    tecnicas = cursor.fetchall()

    conexao.close()

    return render_template(
        "tecnicas.html",
        tecnicas=tecnicas
    )


@app.route("/videos")
def videos():
    return render_template("videos.html")


@app.route("/cartilhas")
def cartilhas():
    return render_template("cartilhas.html")


@app.route("/comunidade")
def comunidade():
    return render_template("comunidade.html")


@app.route("/enviar", methods=["GET", "POST"])
def enviar():

    if request.method == "POST":

        autor = request.form["autor"]
        titulo = request.form["titulo"]
        categoria = request.form["categoria"]
        tipo = request.form["tipo"]
        descricao = request.form["descricao"]

        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO conteudos
            (titulo, descricao, categoria, tipo, autor)
            VALUES (?, ?, ?, ?, ?)
        """, (titulo, descricao, categoria, tipo, autor))

        conexao.commit()
        conexao.close()

        return "Conteúdo enviado com sucesso!"

    return render_template("enviar.html")


@app.route("/admin")
def admin():

    if "logado" not in session:
        return redirect("/login")

    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""

    SELECT * FROM conteudos
    WHERE status = 'pendente'

    """)

    conteudos = cursor.fetchall()

    conexao.close()

    return render_template(
        "admin.html",
        conteudos=conteudos
    )


@app.route("/aprovar/<int:id>")
def aprovar(id):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE conteudos
        SET status = 'aprovado'
        WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect("/admin")


@app.route("/rejeitar/<int:id>")
def rejeitar(id):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE conteudos
        SET status = 'rejeitado'
        WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect("/admin")


@app.route("/conteudos")
def conteudos():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM conteudos
        WHERE status = 'aprovado'
        ORDER BY id DESC
    """)

    conteudos = cursor.fetchall()

    conexao.close()

    return render_template("conteudos.html", conteudos=conteudos)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == "curador" and senha == "1234":
            session["logado"] = True
            return redirect("/admin")
        else:
            return "Usuário ou senha incorretos"

    return render_template("login.html")


# -------------------------
# INICIAR APP
# -------------------------

if __name__ == "__main__":

    criar_banco()

    app.run(debug=True)
