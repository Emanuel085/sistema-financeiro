import sqlite3
import os

CAMINHO_DB = "data/financeiro.db"

def conectar():
    os.makedirs("data", exist_ok=True)
    conexao = sqlite3.connect(CAMINHO_DB)
    return conexao

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT,
            data TEXT NOT NULL
        );
""")

    conexao.commit()
    conexao.close()