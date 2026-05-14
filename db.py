import sqlite3

def conectar_banco():
    return sqlite3.connect("database.db")

def criar_banco():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conteudos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            categoria TEXT NOT NULL,
            tipo TEXT,
            autor TEXT,
            arquivo TEXT,
            status TEXT DEFAULT 'pendente'
        )
    """)

    conexao.commit()
    conexao.close()