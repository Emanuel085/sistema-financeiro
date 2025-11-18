import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#Conexão com o banco de dados

def conectar():
    return sqlite3.connect("data/financeiro.db")

def obter_saldo():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT tipo, valor FROM transacoes")
    transacoes = cursor.fetchall()
    conexao.close()

    saldo = 0
    for tipo, valor in transacoes:
        if tipo.lower() == "receita":
            saldo += valor
        else:
            saldo -= valor
    return saldo

#Funções principais

def salvar_transacao():
    tipo = tipo_var.get()
    descricao = descricao_entry.get()
    valor = valor_entry.get()

    if not descricao or not valor:
        messagebox.showwarning("Atenção," "Preencha todos os campos.")
        return
    
    try:
        valor = float(valor)
    except ValueError:
        messagebox.showwarning("Erro", "O valor precisa ser numérico.")
        return
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO transacoes (tipo, descricao, valor, data) VALUES (?, ?, ?, DATE('now'))",
        (tipo, descricao, valor))
    conexao.commit()
    conexao.close()


    descricao_entry.delete(0, tk.END)
    valor_entry.delete(0, tk.END)
    atualizar_lista()

def atualizar_lista():
    for i in tree.get_children():
        tree.delete(i)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT tipo, descricao, valor, data FROM transacoes ORDER BY data DESC")
    transacoes = cursor.fetchall()
    conexao.close()

    saldo = obter_saldo()
    saldo_label.config(text=f"Saldo atual: R$ {saldo:.2f}".replace(",", "X").replace("X", "."))

    for tipo, descricao, valor, data in transacoes:
        display_valor = f"- R$ {valor:.2f}" if tipo.lower() == "despesa" else f"R$ {valor:.2f}"
        tree.inset("", "end", values=(tipo.title(), descricao, display_valor, data))

def ver_resumo():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT tipo, SUM(valor) FROM transacoes GROUP BY tipo")
    dados = cursor.fetchall()
    conexao.close()

    receitas = sum(v for t, v in dados if t.lower() == "receita")
    despesas = sum(v for t, v in dados if t.lower() == "despesa")
    saldo_final = receitas - despesas

    resumo = ttk.Toplevel(root)
    resumo.title("Resumo Financeiro")
    resumo.geometry("400x400")
    resumo.resizable(False, False)

    ttk.Label(resumo, text=f"Receitas: R$ {receitas:.2f}", bootstyle="sucess", font=("Segoe UI", 11, "bold")).pack(pady=5)
    ttk.Label(resumo, text=f"Despesas: R$ {despesas:.2f}", bootstyle="danger", font=("Segoe UI", 11, "bold")).pack(pady=5)
    ttk.Label(resumo, text=f"Saldo Final: R$ {saldo_final:.2f}", bootstyle="info", font=("Segoe UI", 11, "bold")).pack(pady=10)

    #gráfico de pizza
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie([receitas, despesas], labels=["Receitas", "Despesas"], autopct="%1.1f%%", colors=["#28a745", "#dc3545"])
    ax.set_title("Distribuição Financeira")
    chart = FigureCanvasTkAgg(fig, resumo)
    chart.get_tk_widget().pack(pady=10)
    chart.draw()

def zerar_dados():
    confirmar = messagebox.askyesno("Confirmar", "Tem certeza que deseja apagar todas as transações?")
    if not confirmar:
        return
    conexao = conectar()
    cursor = conexao.cursor()
    cursor. execute("DELETE FROM transacoes")
    conexao.commit()
    conexao.close()
    atualizar_lista()
    messagebox.showinfo("Zerado", "Todos os dados foram apagados.")


def alternar_tema():
    tema_atual = app.style.theme.name
    if tema_atual == "flatly":
        app.style.theme_use("darkly")
    else:
        app.style.theme_use("flatly")


#Interface moderna (ttkbootstrap)

root = ttk.Window(themename="cyborg")
root.title("Sistema Financeiro 3.0")
root.geometry("750x550")
root.resizable(False, False)

#Cabeçalho

header = ttk.Label(root, text="Sistema Financeiro 3.0", font=("Segoe UI", 16, "bold"), bootstyle="primary")
header.pack(fill=X, pady=10)

saldo_label = ttk.Label(root, text=f"Saldo atual: R$ {obter_saldo():,.2f}", font=("Segoe UI", 12, "bold"), bootstyle="inverse-primary")
saldo_label.pack(pady=10)


#formulário

frame_top = ttk.Frame(root, padding=10, bootstyle="primary")
frame_top.pack(fill="x")

ttk.Label(
    frame_top,
    text="💰 Sistema Financeiro 2.0",
    font=("Segoe UI", 14, "bold"),
    foreground="white"
).pack(side="left", padx=10)

form_frame = ttk.Frame(root)
form_frame.pack(pady=10)

ttk.Label(form_frame, text="Tipo:").grid(row=0, column=0, padx=5, sticky="w")
tipo_var = ttk.StringVar(value="Receita")
tipo_combo = ttk.Combobox(form_frame, textvariable=tipo_var, values=["Receita", "Despesa"], width=15)
tipo_combo.grid(row=0, column=1, padx=5)

ttk.Label(form_frame, text="Descrição:").grid(row=1, column=0, padx=5, sticky="w")
descricao_entry = ttk.Entry(form_frame, width=40)
descricao_entry.grid(row=1, column=1, padx=5)

ttk.Label(form_frame, text="Valor (R$):").grid(row=2, column=0, padx=5, sticky="w")
valor_entry = ttk.Entry(form_frame, width=20)
valor_entry.grid(row=2, column=1, padx=5, sticky="w")

#Botões
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="💾 Salvar", bootstyle="success-outline", command=salvar_transacao).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="📊 Resumo", bootstyle="info-outline", command=ver_resumo).grid(row=0, column=2, padx=5)
ttk.Button(btn_frame, text="🗑️ Zerar", bootstyle="danger-outline", command=zerar_dados).grid(row=0, column=1, padx=5)
ttk.Button(frame_top, text="🌓 Tema", bootstyle="secondary-outline", command=alternar_tema).pack(side="right", padx=10)


#Lista de Transações
tree = ttk.Treeview(root, columns=("Tipo", "Descrição", "Valor (R$)", "Data"), show="headings", height=12)
for col in ("Tipo", "Descrição", "Valor (R$)", "Data"):
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True, padx=15, pady=10)


app = ttk.Window(themename="darkly")



#Inicializa
atualizar_lista()
root.mainloop()