import sqlite3
import os

os.makedirs("data", exist_ok=True)

con = sqlite3.connect("data/financeiro.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS transacoes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    descricao TEXT,
    valor REAL,
    data TEXT
)
""")

con.commit()
con.close()

print("Banco e tabela criados com sucesso!")
