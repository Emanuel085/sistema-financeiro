from datetime import datetime

class Transacao:
    def __init__(self, tipo, descricao, valor, categoria=None, data=None):
        self.tipo = tipo
        self.descricao = descricao
        self.valor = float(valor)
        self.categoria= categoria
        self.data= data or datetime.now().strftime("%Y-%m-%d %H:%M%S")