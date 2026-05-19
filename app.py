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

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM precos
        ORDER BY data_atualizacao DESC
    """)

    precos = cursor.fetchall()

    ultima_data = precos[0][6] if precos else None

    conexao.close()

    return render_template(
        "precos.html",
        precos=precos,
        ultima_data=ultima_data
    )


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


@app.route("/admin/precos", methods=["GET", "POST"])
def admin_precos():

    if "logado" not in session:
        return redirect("/login")

    if request.method == "POST":
        produto = request.form["produto"]
        unidade = request.form["unidade"]
        preco_atual = request.form["preco_atual"]
        preco_anterior = request.form["preco_anterior"]
        fonte = request.form["fonte"]
        data_atualizacao = request.form["data_atualizacao"]

        preco_atual_float = float(preco_atual)
        preco_anterior_float = float(preco_anterior)

        if preco_atual_float > preco_anterior_float:
            tendencia = "subiu"
        elif preco_atual_float < preco_anterior_float:
            tendencia = "caiu"
        else:
            tendencia = "estavel"

        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO precos
            (produto, unidade, preco_atual, preco_anterior, fonte, data_atualizacao, tendencia)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            produto,
            unidade,
            preco_atual_float,
            preco_anterior_float,
            fonte,
            data_atualizacao,
            tendencia
        ))

        conexao.commit()
        conexao.close()

        return redirect("/admin/precos")

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM precos
        ORDER BY id DESC
    """)

    precos = cursor.fetchall()

    conexao.close()

    return render_template("admin_precos.html", precos=precos)


@app.route("/deletar_preco/<int:id>")
def deletar_preco(id):

    if "logado" not in session:
        return redirect("/login")

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM precos
        WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect("/admin/precos")


@app.route("/editar_preco/<int:id>", methods=["GET", "POST"])
def editar_preco(id):

    if "logado" not in session:
        return redirect("/login")

    conexao = conectar_banco()
    cursor = conexao.cursor()

    if request.method == "POST":
        produto = request.form["produto"]
        unidade = request.form["unidade"]
        preco_atual = float(request.form["preco_atual"])
        preco_anterior = float(request.form["preco_anterior"])
        fonte = request.form["fonte"]
        data_atualizacao = request.form["data_atualizacao"]

        if preco_atual > preco_anterior:
            tendencia = "subiu"
        elif preco_atual < preco_anterior:
            tendencia = "caiu"
        else:
            tendencia = "estavel"

        cursor.execute("""
            UPDATE precos
            SET produto = ?,
                unidade = ?,
                preco_atual = ?,
                preco_anterior = ?,
                fonte = ?,
                data_atualizacao = ?,
                tendencia = ?
            WHERE id = ?
        """, (
            produto,
            unidade,
            preco_atual,
            preco_anterior,
            fonte,
            data_atualizacao,
            tendencia,
            id
        ))

        conexao.commit()
        conexao.close()

        return redirect("/admin/precos")

    cursor.execute("""
        SELECT * FROM precos
        WHERE id = ?
    """, (id,))

    preco = cursor.fetchone()
    conexao.close()

    return render_template("editar_preco.html", preco=preco)


@app.route("/editar_conteudo/<int:id>", methods=["GET", "POST"])
def editar_conteudo(id):

    if "logado" not in session:
        return redirect("/login")

    conexao = conectar_banco()
    cursor = conexao.cursor()

    if request.method == "POST":
        titulo = request.form["titulo"]
        categoria = request.form["categoria"]
        tipo = request.form["tipo"]
        descricao = request.form["descricao"]
        autor = request.form["autor"]

        cursor.execute("""
            UPDATE conteudos
            SET titulo = ?,
                categoria = ?,
                tipo = ?,
                descricao = ?,
                autor = ?
            WHERE id = ?
        """, (
            titulo,
            categoria,
            tipo,
            descricao,
            autor,
            id
        ))

        conexao.commit()
        conexao.close()

        return redirect("/admin")

    cursor.execute("""
        SELECT * FROM conteudos
        WHERE id = ?
    """, (id,))

    conteudo = cursor.fetchone()
    conexao.close()

    return render_template("editar_conteudo.html", conteudo=conteudo)


# -------------------------
# INICIAR APP
# -------------------------
if __name__ == "__main__":

    criar_banco()

    app.run(debug=True)
