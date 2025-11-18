import sqlite3

CAMINHO_DB = "data/financeiro.db"

con = sqlite3.connect(CAMINHO_DB)
cur = con.cursor()

cur.execute("UPDATE transacoes SET valor = ABS(valor)")
con.commit()

print("Banco corrigido: todos os valores agora estão positivos.")

con.close()