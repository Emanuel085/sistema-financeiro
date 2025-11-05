from services.transacao_service import adicionar_transacao, listar_transacoes, resumo_financeiro

def menu():
    print("""]
========= SISTEMA FINANCEIRO =========
1. Adicionar Receita
2. Adicionar Despesa
3. Listar Transações
4. Ver Resumo Financeiro
0. Sair
==============================================
""")
    
def main():
    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao =="1":
            descricao = input("Descrição: ")
            valor = float(input("Valor: ").replace(",", "."))
            categoria = input("Categoria: ")
            adicionar_transacao("receita", descricao, valor, categoria)

        elif opcao =="2":
            descricao = input("Descrição: ")
            valor = float(input("Valor: ").replace(",", "."))
            categoria = input("Categoria: ")
            adicionar_transacao("despesa", descricao, valor, categoria)

        elif opcao =="3":
            listar_transacoes()

        elif opcao=="4":
            resumo_financeiro()

        elif opcao=="0":
            print("Encerrando o sitema...")
            break
        
        else:
            print("Opção Inválida.")


if __name__ == "__main__":
    main()