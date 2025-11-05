## Sistema Financeiro (Python + Sqlite)

Um sistema simples de controle financeiro para registrar receitas e despesas, com armazenamento no banco de dados SQLite

## Funcionalidades

- Adicionar receitas e despesas
- Listar Transações
- Resumo financeiro com saldo total
- Categoria de gastos
- Interface via terminal

## Tecnologias utilizadas

- Python
- SQLite
- Colorama (para cores no terminal)

## Como executar

1. Clone este repositório:
```bash
git clone https://github.com/Emanuel085/sistema-financeiro.git

2. Acesse a pasta cd/~/financeiro

3 Crie um ambiente virtual
python3 - m venv venv
source venv/bin/activate

4. Instale as dependências:

pip install colorama

5. Execute o sistema:

python 3 main.py

Estrutura de pastas

financeiro/
│
├── data/                # Banco de dados SQLite
├── models/              # Classes e modelos de dados
├── services/            # Lógica de negócio
├── utils/               # Funções utilitárias
├── main.py              # Ponto de entrada
└── README.md