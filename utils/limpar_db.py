import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'financeiro.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("DELETE FROM transacoes")
conn.commit()

conn.close()

print("Todas as transações foram apagadas. Saldo zerado.")
