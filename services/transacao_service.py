from utils.db import conectar, criar_tabela
from models.transacao import Transacao
from colorama import Fore, Style

criar_tabela()

def adicionar_transacao(tipo, descricao, valor, categoria=None):
    transacao = Transacao(tipo, descricao, valor, categoria)
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO transacoes (tipo, descricao, valor, categoria, data)
        VALUES (?, ?, ?, ?, ?)
    """, (transacao.tipo, transacao.descricao, transacao.valor, transacao.categoria, transacao.data))
    
    conexao.commit()
    conexao.close()
    print("✅ Transação cadastrada com sucesso!")

def listar_transacoes():
    conexao = conectar()
    cursor= conexao.cursor()
    cursor.execute("SELECT tipo, descricao, valor, categoria, data FROM transacoes")
    transacoes = cursor.fetchall()
    conexao.close()

    if not transacoes:
        print("Nenhuma transação encontrada.")
        return
    
    for t in transacoes:
        tipo, descricao, valor, categoria, data = t
        tipo_nome = "Receita" if tipo == "receita" else "Despesa"
    try:
        valor = float(valor)
    except ValueError:
        valor = 0.0
    print(f"{tipo_nome} | {descricao} | R$ {valor:.2f} | {data} | Categoria: {categoria or '-'}")


def resumo_financeiro():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT SUM (valor) FROM transacoes WHERE tipo = 'receita'")
    receitas = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM (valor) FROM transacoes WHERE tipo = 'despesa'")
    despesas = cursor.fetchone()[0] or 0

    conexao.close()

    saldo = receitas - despesas

    print("\n" + "=" *45)
    print(f"{Fore.CYAN}{'RESUMO FINANCEIRO'.center(45)}{Style.RESET_ALL}")
    print("=" *45)

    print(f"{Fore.GREEN}Receitas: {Style.RESET_ALL}R$ {receitas:.2f}")
    print(f"{Fore.RED}Despesas: {Style.RESET_ALL} R$ {despesas:.2f}")

    cor_saldo = Fore.GREEN if saldo >= 0 else Fore.RED
    print(f"{cor_saldo}Saldo Final: R$ {saldo:.2f}{Style.RESET_ALL}")
    print("=" * 45+ "\n")